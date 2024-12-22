# tasks.py
from typing import Callable, Literal, Optional, Set, Union
import numpy as np

import torch
from torch import Tensor
import torch.nn as nn
import torch.nn.functional as F

import lightning.pytorch as pl
from lightning.pytorch.utilities import grad_norm

import torchmetrics as tm

from modelgenerator.lr_schedulers import LazyLRScheduler
from modelgenerator.backbones import (
    HFSequenceBackbone,
    HFSequenceBackbone,
    DefaultConfig,
    LegacyAdapterType,
    aido_dna_dummy,
)
from modelgenerator.adapters import (
    SequenceAdapter,
    TokenAdapter,
    ConditionalGenerationAdapter,
    LinearAdapter,
    LinearCLSAdapter,
    LinearTransformerAdapter,
    ConditionalLMAdapter,
    MLPPoolAdapter,
)
from modelgenerator.metrics import TopLAcc, AUROC, AUPRC
from modelgenerator.tasks.base import *


class MLM(TaskInterface):
    """Task for continuing pretraining on a masked language model. This task is used to fine-tune a model on a downstream task by continuing pretraining on a dataset with masked sequences.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the adapter from the backbone. Defaults to False.
            Will be deprecated once the new adapter API is fully verified.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        use_legacy_adapter: bool = True,
        **kwargs,
    ):
        if not use_legacy_adapter:
            raise ValueError("MLM must use the adapter from the backbone.")
        super().__init__(use_legacy_adapter=True, **kwargs)
        if self.__class__ is MLM:
            self.save_hyperparameters()
        self.backbone = None
        self.adapter = None
        self.backbone_fn = backbone
        self.loss = nn.CrossEntropyLoss()
        for stage in ["train", "val", "test"]:
            self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                {
                    "accuracy": tm.MeanMetric(),
                }
            )
        self.metrics_to_pbar = {"accuracy"}

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        self.backbone = self.backbone_fn(LegacyAdapterType.MASKED_LM, None)
        self.adapter = self.backbone.get_decoder()

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences and target_sequences
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with input_ids, attention_mask, and target_ids
        """
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            batch["sequences"]
        )
        target_ids = None
        if batch.get("target_sequences", None) is not None:
            target_ids, _, _ = self.backbone.tokenize(batch["target_sequences"])
            target_ids = torch.tensor(target_ids, dtype=torch.long).to(self.device)
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "target_ids": target_ids,
            "special_tokens_mask": special_tokens_mask,
        }

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data from collate

        Returns:
            Tensor: The decoder logits
        """
        encoder_hidden = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )
        decoder_logits = self.adapter(encoder_hidden)
        return decoder_logits

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions from forward against the ground truth labels.

        Args:
            logits (Tensor): The token-wise predicted logits
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing target_ids
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            Tensor: The loss.
        """
        target_ids = collated_batch["target_ids"]
        loss = self.loss(logits.permute(0, 2, 1).contiguous(), target_ids)
        if loss_only:
            return {"loss": loss}
        preds = logits.argmax(-1)
        metrics = self.get_metrics_by_stage(stage)
        self.call_or_update_metric(
            stage, metrics["accuracy"], (preds == target_ids).float().mean()
        )
        return {"loss": loss}


class Inference(MLM):
    """Task for performing inference of token probabilities with a pre-trained backbone

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the adapter from the backbone. Defaults to False.
            Will be deprecated once the new adapter API is fully verified.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences (and optionally ids)
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with input_ids, attention_mask, and target_ids
        """
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            batch["sequences"]
        )
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        batch.update(
            {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "special_tokens_mask": special_tokens_mask,
            }
        )
        return batch


class SequenceClassification(TaskInterface):
    """Task for fine-tuning a model on a sequence classification task. Inherits from TaskInterface.

    Note:
        Supports binary, multiclass, and multi-label classification tasks.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int], SequenceAdapter], optional): The callable that returns an adapter. Defaults to LinearCLSAdapter.
        n_classes (int, optional): The number of classes in the classification task. Defaults to 2.
        multilabel (bool, optional): Indicate whether it is a multilabel classification task. If True, the n_classes should be set to the number of targets. Defaults to False.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the adapter from the backbone. Defaults to False.
            Will be deprecated once the new adapter API is fully verified.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    legacy_adapter_type = LegacyAdapterType.SEQ_CLS

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        adapter: Optional[Callable[[int, int], SequenceAdapter]] = LinearCLSAdapter,
        n_classes: int = 2,
        multilabel: bool = False,
        **kwargs,
    ):
        if n_classes < 2:
            raise ValueError(
                "n_classes must be greater than 1. Set n_classes=2 for binary classification."
            )
        super().__init__(**kwargs)
        if self.__class__ is SequenceClassification:
            self.save_hyperparameters()
        self.backbone_fn = backbone
        self.backbone = None
        self.adapter = None
        self.adapter_fn = adapter
        self.n_classes = n_classes
        self.multilabel = multilabel

        if not multilabel:
            # input: (bs, C), target: (bs,)
            self.loss = nn.CrossEntropyLoss()
        else:
            # input: (bs, C), target: (bs, C)
            self.loss = nn.BCEWithLogitsLoss()

        for stage in ["train", "val", "test"]:
            if not multilabel:
                task = "binary" if n_classes == 2 else "multiclass"
                self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                    {
                        # Note: `average` need to be set explicity for accuracy and f1
                        # see https://github.com/Lightning-AI/torchmetrics/issues/2280
                        "accuracy": tm.Accuracy(
                            task, num_classes=n_classes, average="micro"
                        ),
                        "f1": tm.F1Score(task, num_classes=n_classes, average="macro"),
                        "mcc": tm.MatthewsCorrCoef(task, num_classes=n_classes),
                        "auroc": tm.AUROC(task, num_classes=n_classes),
                    }
                )
            else:
                self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                    {
                        "accuracy": tm.Accuracy(
                            "multilabel", num_labels=n_classes, average="macro"
                        ),
                        "f1": tm.F1Score(
                            "multilabel", num_labels=n_classes, average="macro"
                        ),
                        "mcc": tm.MatthewsCorrCoef("multilabel", num_labels=n_classes),
                        "auroc": tm.AUROC(
                            "multilabel", num_labels=n_classes, average="macro"
                        ),
                    }
                )
                if stage == "test":
                    # calculates score for each label
                    label_wise_acc = nn.ModuleDict(
                        {
                            "accuracy_" + str(i): tm.Accuracy("binary")
                            for i in range(n_classes)
                        }
                    )
                    label_wise_f1 = nn.ModuleDict(
                        {"f1_" + str(i): tm.F1Score("binary") for i in range(n_classes)}
                    )
                    label_wise_mcc = nn.ModuleDict(
                        {
                            "mcc_" + str(i): tm.MatthewsCorrCoef("binary")
                            for i in range(n_classes)
                        }
                    )
                    label_wise_auroc = nn.ModuleDict(
                        {
                            "auroc_" + str(i): tm.AUROC("binary")
                            for i in range(n_classes)
                        }
                    )
                    self.metrics[f"{stage}_metrics"].update(label_wise_acc)
                    self.metrics[f"{stage}_metrics"].update(label_wise_f1)
                    self.metrics[f"{stage}_metrics"].update(label_wise_mcc)
                    self.metrics[f"{stage}_metrics"].update(label_wise_auroc)

        self.metrics_to_pbar = set(self.metrics["train_metrics"].keys())

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        if self.use_legacy_adapter:
            self.backbone = self.backbone_fn(
                self.legacy_adapter_type,
                DefaultConfig(config_overwrites={"num_labels": self.n_classes}),
            )
            self.adapter = self.backbone.get_decoder()
        else:
            self.backbone = self.backbone_fn(None, None)
            self.adapter = self.adapter_fn(
                self.backbone.get_embedding_size(), self.n_classes
            )

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data into a format that can be passed to the forward and evaluate methods.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data containing sequences and labels
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch containing input_ids, attention_mask, and labels
        """
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            batch["sequences"]
        )
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        if batch.get("labels", None) is not None:
            if isinstance(batch["labels"], torch.Tensor):
                labels = batch["labels"].to(self.device, dtype=torch.long)
            else:
                labels = torch.tensor(batch["labels"], dtype=torch.long).to(self.device)
        else:
            labels = None
        return {
            "sequences": batch["sequences"],
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "special_tokens_mask": special_tokens_mask,
            "labels": labels,
        }

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): A collated batch of data containing input_ids and attention_mask

        Returns:
            Tensor: The classifier logits
        """
        hidden_states = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )
        logits = self.adapter(hidden_states, collated_batch["attention_mask"])
        return logits

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions against the ground truth labels.

        Args:
            logits (Tensor): The sequence-level model predictions
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing labels
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            Tensor: The loss.
        """
        labels = collated_batch["labels"]
        if not self.multilabel:
            labels = labels.view(-1)  # (bs,)
            loss = self.loss(logits.view(-1, self.n_classes), labels)
        else:
            # Note: BCEWithLogitsLoss requires the labels to be float instead of int
            # TODO: to float should behandled in collate
            loss = self.loss(logits, labels.float())
        if loss_only:
            return {"loss": loss}
        metrics = self.get_metrics_by_stage(stage)
        if not self.multilabel:
            preds = torch.softmax(logits, dim=-1)  # probs of shape (bs, C)
            if self.n_classes == 2:
                preds = preds[:, 1]  # probs of shape (bs,)
        else:
            preds = torch.sigmoid(logits)  # probs of shape (bs, C)
        if self.multilabel and stage == "test":
            binary_metrics = []
            for name, metric in metrics.items():
                if len(name.split("_")) == 1:
                    self.call_or_update_metric(stage, metric, preds, labels)
                else:
                    binary_metrics.append(metric)
            for i, metric in enumerate(binary_metrics):
                j = i % self.n_classes
                self.call_or_update_metric(stage, metric, preds[:, j], labels[:, j])
        else:
            for metric in metrics.values():
                self.call_or_update_metric(stage, metric, preds, labels)
        return {"loss": loss}


class TokenClassification(SequenceClassification):
    """Task for fine-tuning a model on a token classification task.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int], TokenAdapter], optional): The callable that returns an adapter. Defaults to LinearAdapter.
        n_classes (int, optional): The number of classes in the classification task. Defaults to 2.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the adapter from the backbone. Defaults to False.
            Will be deprecated once the new adapter API is fully verified.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    legacy_adapter_type = LegacyAdapterType.TOKEN_CLS

    def __init__(
        self,
        adapter: Optional[Callable[[int, int], TokenAdapter]] = LinearAdapter,
        **kwargs,
    ):
        # TODO: multi-label can be supported once token classification dataset
        # supports it and padding values are handled correctly
        super().__init__(adapter=adapter, multilabel=False, **kwargs)
        if self.__class__ is TokenClassification:
            self.save_hyperparameters()

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): A collated batch of data containing input_ids and attention_mask

        Returns:
            Tensor: The classifier logits
        """
        hidden_states = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )  # (bs, seq_len, hidden_size)
        logits = self.adapter(hidden_states)
        return logits

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions against the ground truth labels.

        Args:
            logits (Tensor): The sequence-level model predictions
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing labels
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            Tensor: The loss.
        """
        padded_labels = collated_batch["labels"]
        collated_batch["labels"] = padded_labels[padded_labels != -100].view(-1)
        special_tokens_mask = torch.logical_not(collated_batch["special_tokens_mask"])
        logits = logits[special_tokens_mask].view(-1, self.n_classes)
        return super().evaluate(logits, collated_batch, stage, loss_only)


class PairwiseTokenClassification(SequenceClassification):
    """Task for fine-tuning a model on a pairwise token classification task.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int], TokenAdapter], optional): The callable that returns an adapter. Defaults to LinearAdapter.
        n_classes (int, optional): The number of classes in the classification task. Defaults to 2.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the adapter from the backbone. Defaults to False.
            Will be deprecated once the new adapter API is fully verified.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    legacy_adapter_type = LegacyAdapterType.TOKEN_CLS

    def __init__(
        self,
        adapter: Optional[Callable[[int, int], TokenAdapter]] = LinearAdapter,
        n_classes: int = 2,
        **kwargs,
    ):
        # TODO: multi-class support in evaluate
        if n_classes != 2:
            raise ValueError(
                "PairwiseTokenClassification currenlty only supports binary classification"
            )
        super().__init__(
            adapter=adapter, n_classes=n_classes, multilabel=False, **kwargs
        )
        if self.__class__ is PairwiseTokenClassification:
            self.save_hyperparameters()
        for stage in ["train", "val", "test"]:
            self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                {"top_L_acc": TopLAcc(k=1)}
            )
            self.metrics[f"{stage}_metrics"].update(
                {f"top_L{k}_acc": TopLAcc(k=k) for k in [2, 5, 10]}
            )
        self.metrics_to_pbar = {"top_L5_acc"}

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        if self.use_legacy_adapter:
            self.backbone = self.backbone_fn(
                self.legacy_adapter_type,
                DefaultConfig(config_overwrites={"num_labels": self.n_classes}),
            )
            self.adapter = self.backbone.get_decoder()
        else:
            self.backbone = self.backbone_fn(None, None)
            self.adapter = self.adapter_fn(
                self.backbone.get_embedding_size() * 2,
                self.n_classes,
            )

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): A collated batch of data containing input_ids and attention_mask

        Returns:
            Tensor: The classifier logits
        """
        hidden_states = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )
        if self.use_legacy_adapter:
            logits = self.adapter(hidden_states)
        else:
            x = self.outer_concat(hidden_states)
            logits = self.adapter(x)
        return logits

    def outer_concat(self, x):
        """Taken directly from FM4BioContactHead"""
        batch_size, seq_len, features = x.shape

        # Permute to [batch_size, features, seq_len]
        x = x.permute(0, 2, 1)

        # Introduce new dimensions for broadcasting
        x_1 = x[:, None, :, :, None]  # [batch_size, 1, features, seq_len, 1]
        x_2 = x[:, None, :, None, :]  # [batch_size, 1, features, 1, seq_len]

        # Repeat along new dimensions
        x_1 = x_1.repeat(
            1, 1, 1, 1, seq_len
        )  # [batch_size, 1, features, seq_len, seq_len]
        x_2 = x_2.repeat(
            1, 1, 1, seq_len, 1
        )  # [batch_size, 1, features, seq_len, seq_len]

        # Concatenate along the second dimension
        x = torch.cat((x_1, x_2), dim=1)  # [batch_size, 2, features, seq_len, seq_len]

        # Get lower triangular indices
        I, J = torch.tril_indices(seq_len, seq_len, -1)

        # Symmetrize
        x[:, :, :, I, J] = x[:, :, :, J, I]

        # Permute to desired shape and make contiguous
        x = x.permute(
            0, 3, 4, 2, 1
        ).contiguous()  # [batch_size, seq_len, seq_len, features, 2]

        # Reshape to combine the last two dimensions
        x = x.view(
            batch_size, seq_len, seq_len, features * 2
        )  # [batch_size, seq_len, seq_len, features * 2]

        return x

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions against the ground truth labels.

        Args:
            logits (Tensor): The sequence-level model predictions
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing labels
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            Tensor: The loss.
        """
        padded_labels = collated_batch["labels"]  # (1, seq_len-1, seq_len-1)
        labels = padded_labels[
            padded_labels != -100
        ]  # vector: (seq_len-1) * (seq_len-1)
        special_tokens_mask = torch.logical_not(collated_batch["special_tokens_mask"])
        # (bs, seq_len) -> (bs, seq_len, seq_len) by batch wise outer product
        special_tokens_mask_expanded = torch.einsum(
            "bp, bq -> bpq", special_tokens_mask, special_tokens_mask
        )
        logits = logits[special_tokens_mask_expanded]  # (labels.shape[0], n_classes)
        loss = self.loss(logits, labels)
        if loss_only:
            return {"loss": loss}
        metrics = self.get_metrics_by_stage(stage)
        logits = logits[..., -1]  # P(x=1)
        indices = torch.argsort(-logits)
        L = special_tokens_mask.sum().item()
        for acc in metrics.values():
            self.call_or_update_metric(stage, acc, logits, labels, indices, L)
        return {"loss": loss}


class Diffusion(TaskInterface):
    """Task Masked Diffusion Language Modeling training and denoising on sequences (https://arxiv.org/abs/2406.07524). Inherits from TaskInterface.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int], TokenAdapter], optional): The callable that returns an adapter. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the legacy adapter. Defaults to True.
            Will be deprecated once the new adapter API is fully verified.
        sample_seq (bool, optional): Whether to sample tokens during denoising. Defaults to False.
        num_denoise_steps (int, optional): The number of denoising steps to take. Defaults to 4.
        sampling_temperature (float, optional): The temperature for sampling tokens. Defaults to 1.0.
        normalize_posterior_weights (bool, optional): Whether to normalize posterior weights. Defaults to False.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the adapter from the backbone. Defaults to False.
            Will be deprecated once the new adapter API is fully verified.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        adapter: Optional[Callable[[int, int], TokenAdapter]] = None,
        use_legacy_adapter: bool = True,
        sample_seq: bool = False,
        num_denoise_steps: int = 4,
        sampling_temperature: float = 1.0,
        normalize_posterior_weights: bool = False,
        verbose: bool = False,
        **kwargs,
    ):
        super().__init__(use_legacy_adapter=use_legacy_adapter, **kwargs)
        if self.__class__ is Diffusion:
            self.save_hyperparameters()
        self.backbone = None
        self.adapter = None
        self.mask_id = None
        self.backbone_fn = backbone
        self.adapter_fn = adapter
        self.sample_seq = sample_seq
        self.num_denoise_steps = num_denoise_steps
        self.sampling_temperature = sampling_temperature
        self.normalize_posterior_weights = normalize_posterior_weights
        self.verbose = verbose
        self.loss = nn.CrossEntropyLoss(
            reduction="none", label_smoothing=0.05
        )  ## NOTE: "label_smoothing" taken from gRNAde codebase
        self.mask_id = None
        for stage in ["train", "val", "test"]:
            self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                {
                    "accuracy": tm.MeanMetric(),
                }
            )
        self.metrics_to_pbar = {"accuracy"}

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        if self.use_legacy_adapter:
            self.backbone = self.backbone_fn(LegacyAdapterType.MASKED_LM, None)
            self.adapter = self.backbone.get_decoder()
        else:
            self.backbone = self.backbone_fn(None, None)
            self.adapter = self.adapter_fn(
                self.backbone.get_embedding_size(), self.backbone.get_vocab_size()
            )
        self.mask_id = self.backbone.get_token_id("[MASK]")

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences, target_sequences, and posterior_weights
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with input_ids, input_seqs, input_masks, attention_mask, target_ids, target_masks, target_seqs, and posterior_weights
        """
        # Each sample in a batch is a list of noised sequences at various noise levels. Stack them for easy training.
        input_seqs = [seq for seqs in batch["sequences"] for seq in seqs]
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            input_seqs
        )
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        input_mask = torch.where(input_ids == self.mask_id, 1, 0)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        target_seqs = None
        target_ids = None
        target_mask = None
        posterior_weights = None
        if batch.get("target_sequences", None) is not None:
            target_seqs = [seq for seqs in batch["target_sequences"] for seq in seqs]
            target_ids, _, _ = self.backbone.tokenize(target_seqs)
            target_ids = torch.tensor(target_ids, dtype=torch.long).to(self.device)
            target_mask = torch.where(target_ids == self.mask_id, 1, 0)
        if batch.get("posterior_weights", None) is not None:
            posterior_weights = torch.tensor(
                [weight for weights in batch["posterior_weights"] for weight in weights]
            ).to(self.device)
            if self.normalize_posterior_weights:
                # Experimental! Normalizing posterior weights for stable training
                posterior_weights = posterior_weights / posterior_weights.sum()
                posterior_weights = posterior_weights.view(-1)
        return {
            "input_ids": input_ids,
            "input_masks": input_mask,
            "input_seqs": input_seqs,
            "attention_mask": attention_mask,
            "special_tokens_mask": special_tokens_mask,
            "target_ids": target_ids,
            "target_masks": target_mask,
            "target_seqs": target_seqs,
            "posterior_weights": posterior_weights,
        }

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data with input_ids and attention_mask

        Returns:
            Tensor: The decoder logits
        """
        encoder_hidden = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )
        decoder_logits = self.adapter(encoder_hidden)
        return decoder_logits

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions against the ground truth labels.

        Args:
            logits (Tensor): The token-wise predicted logits
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing target_ids, posterior_weights, input_masks, and target_masks
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            Tensor: The loss on tokens with input mask and not target mask
        """
        target_ids = collated_batch["target_ids"]
        posterior_weight = collated_batch["posterior_weights"]
        # Evaluate loss and accuracy on all tokens with input mask and not target mask. Ignore any samples with no input mask.
        eval_mask = collated_batch["input_masks"] * (1 - collated_batch["target_masks"])
        eval_mask_count = eval_mask.sum(-1)
        good_samples = eval_mask_count > 0
        if not good_samples.any():
            # If we have no samples to evaluate, return a loss of 0
            return {"loss": torch.tensor(0.0).to(self.device)}
        # Avoid division by zero. These samples will have zero loss, but be ignored in the final average over good samples.
        eval_mask_count[eval_mask_count == 0] = 1
        # Get loss only on [MASK] tokens, scaled by posterior_weight / total masks
        loss = self.loss(logits.permute(0, 2, 1).contiguous(), target_ids) * eval_mask
        # If we've unmasked everything, eval_mask will be all zeros. Make sure this isn't nan when we have no loss to evaluate.
        # Loss for each timestep is a posterior-weighted sum of avg-unmasked-token-loss
        loss = posterior_weight * loss.sum(-1) / eval_mask_count
        # Total loss is an average over both timesteps and samples in a batch (stacked together in collate)
        loss = loss.sum() / good_samples.sum()
        if loss_only:
            return {"loss": loss}
        pred_tokens = logits.argmax(-1).detach()
        acc = ((pred_tokens == target_ids) * eval_mask).sum(-1) / eval_mask_count
        avg_acc = acc.sum() / good_samples.sum()
        metrics = self.get_metrics_by_stage(stage)
        self.call_or_update_metric(stage, metrics["accuracy"], avg_acc.item())
        return {"loss": loss}

    def _iterative_denoise(
        self, collated_batch: dict[str, Union[list, Tensor]]
    ) -> tuple[dict[str, Union[list, Tensor]], float]:
        """Denoises input sequences iteratively by predicting tokens at masked positions and unmasking the highest probability tokens.

        Note:
            Denoises wherever there are masks, but only evaluates loss where we have no labeled target
            With num_denoise_steps == 1, this is equivalent to the one-step inference used for training
            The loss is the unweighted average of BCE losses for each masked token across all denoising step.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing input_ids, input_masks, and target_masks

        Returns:
            tuple[dict[str, Union[list, Tensor]], float]: The denoised batch with no masks and the loss from the denoising process
        """
        # Keep track of original target masks since we use target masks to specify loss evaluation
        target_masks_init = collated_batch["target_masks"].clone()
        # Do denoise on all input masks. Only evaluate loss where input is mask and target is not
        unmask_counts = (
            collated_batch["input_masks"].sum(-1) // self.num_denoise_steps + 1
        )
        # Run reverse process of diffusion
        denoise_step = 0
        denoise_loss = 0
        while True:
            if (
                collated_batch["input_masks"].sum() == 0
                or denoise_step == self.num_denoise_steps
            ):
                # Check if we're finished denoising
                break
            # Predict tokens
            logits = self(collated_batch)
            probs = F.softmax(logits / self.sampling_temperature, dim=-1)
            if self.sample_seq:
                # Make flat on batch x seq length dim for sampling
                pred_tokens = torch.multinomial(
                    probs.view(-1, probs.size(-1)), 1, replacement=True
                ).squeeze(-1)
                # Reshape back to batch x seq length
                pred_tokens = pred_tokens.view(probs.size(0), -1)
            else:
                # Take maximum probability tokens
                pred_tokens = logits.argmax(-1).squeeze(-1)
            # Unmask highest probability unmask_count tokens from the masked entries
            # Unmasked tokens remain the same
            probs = probs * collated_batch["input_masks"].unsqueeze(-1)
            input_mask_new = collated_batch["input_masks"].clone()
            for i in range(len(collated_batch["input_ids"])):
                unmask_count = min(
                    unmask_counts[i], collated_batch["input_masks"][i].sum().item()
                )
                top_probs = probs[i].max(-1).values
                unmask_indices = top_probs.argsort(descending=True)[:unmask_count]
                collated_batch["input_ids"][i, unmask_indices] = pred_tokens[
                    i, unmask_indices
                ]
                input_mask_new[i, unmask_indices] = 0
                # Specify target masks for loss evaluation
                collated_batch["target_masks"][i] = torch.ones_like(
                    collated_batch["target_masks"][i]
                )
                collated_batch["target_masks"][i, unmask_indices] = 0
            # Still never evaluate loss where we have no labeled target, even though we denoise
            collated_batch["target_masks"] = (
                collated_batch["target_masks"] * target_masks_init
            )
            # Get metrics on unmasked tokens and update the mask to reflect unmasking
            loss = self.evaluate(logits, collated_batch, loss_only=True)
            collated_batch["input_masks"] = input_mask_new
            # Loss averaged over tokens before averaging over samples, so sum over iters should be propto sum of token-wise loss at unmasked tokens with logits from masks at each iter
            denoise_loss += loss["loss"]
            denoise_step += 1
            if self.verbose:
                clean = (
                    lambda s: s.replace("[MASK]", ".")
                    .replace("[CLS]", "")
                    .replace("[SEP]", "")
                    .replace("[PAD]", "")
                    .replace(" ", "")
                )
                pred_strings = self.backbone.decode_tokens(collated_batch["input_ids"])
                pred_strings = [clean(s) for s in pred_strings]
                print(pred_strings)
        # Reset the target mask, since we used this during denoising to specify loss evaluation
        collated_batch["target_masks"] = target_masks_init
        return collated_batch, denoise_loss

    def _val_test_step(
        self,
        batch: dict[str, Union[list, Tensor]],
        split: str,
        batch_idx: Optional[int] = None,
    ) -> Tensor:
        """Runs a validation or test step on a batch of data.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader
            split (str): The split to run the step on (val or test)
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            Tensor: The loss from the validation or test step
        """
        # TODO: this function might need to be merged into evaluate as it now
        #       has a reason to take in "stage" as an argument.
        collated_batch = self.transform(batch, batch_idx)
        input_mask_init = collated_batch["input_masks"].clone()
        collated_batch, denoise_loss = self._iterative_denoise(collated_batch)
        eval_mask = input_mask_init * (1 - collated_batch["target_masks"])
        acc = (
            (collated_batch["input_ids"] == collated_batch["target_ids"]) * eval_mask
        ).sum(-1) / eval_mask.sum(-1)
        avg_acc = acc.mean().item()
        metrics = self.get_metrics_by_stage(split)
        metrics["accuracy"](avg_acc)
        return {"loss": denoise_loss}

    def validation_step(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> Tensor:
        """Runs a validation step on a batch of data.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            Tensor: The loss from the validation step
        """
        loss = self._val_test_step(batch, "val", batch_idx)
        self.log_loss_and_metrics(loss["loss"], "val")
        return loss

    def test_step(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> Tensor:
        """Runs a test step on a batch of data.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            Tensor: The loss from the test step
        """
        loss = self._val_test_step(batch, "test", batch_idx)
        self.log_loss_and_metrics(loss["loss"], "test")
        return loss

    def predict_step(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> Tensor:
        """Infers predictions from a batch of data. Calls collate and forward methods in order.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            Tensor: The model predictions
        """
        collated_batch = self.transform(batch, batch_idx)
        collated_batch, _ = self._iterative_denoise(collated_batch)
        pred_strings = self.backbone.decode_tokens(collated_batch["input_ids"])
        clean = (
            lambda s: s.replace("[MASK]", ".")
            .replace("[CLS]", "")
            .replace("[SEP]", "")
            .replace("[PAD]", "")
            .replace(" ", "")
        )
        collated_batch.update(
            {
                "predictions": [clean(s) for s in pred_strings],
                "sequences": [clean(s) for s in collated_batch["target_seqs"]],
            }
        )
        return collated_batch

    def on_before_optimizer_step(self, optimizer: torch.optim.Optimizer) -> None:
        """Runs before each optimizer step to compute the 2-norm of the gradients.

        Note:
            If using mixed precision, the gradients are already unscaled here

        Args:
            optimizer (torch.optim.Optimizer): The optimizer
            optimizer_idx (int): The index of the optimizer
        """
        norms = grad_norm(self.adapter, norm_type=2)
        if "grad_2.0_norm_total" in norms:
            self.log(f"grad_norm", norms["grad_2.0_norm_total"], prog_bar=True)


class ConditionalMLM(TaskInterface):
    """Task for Conditional Masked Language Modeling training and denoising on sequences. Inherits from TaskInterface.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int, int, nn.Module], ConditionalGenerationAdapter], optional): The callable that returns an adapter. Defaults to ConditionalLMAdapter.
        use_legacy_adapter (bool, optional):
            Whether to use the pre-trained legacy adapter within the conditional decoder. Defaults to True.
        condition_dim (int, optional): The dimension of the condition. Defaults to 1.
        use_pretrained_decoder_head (bool, optional): Whether to use a pretrained decoder head in the condition adapter. Defaults to True.
        sample_seq (bool, optional): Whether to sample tokens during denoising. Defaults to False.
        num_denoise_steps (int, optional): The number of denoising steps to take. Defaults to 4.
        sampling_temperature (float, optional): The temperature for sampling tokens. Defaults to 1.0.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        adapter: Optional[
            Callable[[int, int, int, nn.Module], ConditionalGenerationAdapter]
        ] = ConditionalLMAdapter,
        use_legacy_adapter: bool = True,
        condition_dim: int = 1,
        **kwargs,
    ):
        super().__init__(use_legacy_adapter=use_legacy_adapter, **kwargs)
        if self.__class__ is ConditionalMLM:
            self.save_hyperparameters()
        self.backbone = None
        self.adapter = None
        self.backbone_fn = backbone
        self.adapter_fn = adapter
        self.condition_dim = condition_dim
        self.loss = nn.CrossEntropyLoss()
        for stage in ["train", "val", "test"]:
            self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                {
                    "accuracy": tm.MeanMetric(),
                }
            )
        self.metrics_to_pbar = {"accuracy"}

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        if self.use_legacy_adapter:
            self.backbone = self.backbone_fn(LegacyAdapterType.MASKED_LM, None)
        else:
            self.backbone = self.backbone_fn(None, None)
        self.adapter = self.adapter_fn(
            self.backbone.get_embedding_size(),
            self.condition_dim,
            self.backbone.get_vocab_size(),
            self.backbone.get_decoder() if self.use_legacy_adapter else None,
        )
        self.mask_id = self.backbone.get_token_id("[MASK]")

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences, target_sequences, and labels
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with input_ids, attention_mask, target_ids, and labels
        """
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            batch["sequences"]
        )
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        target_ids = None
        if batch.get("target_sequences", None) is not None:
            target_ids, _, _ = self.backbone.tokenize(batch["target_sequences"])
            target_ids = torch.tensor(target_ids, dtype=torch.long).to(self.device)
        labels = batch["labels"].type(self.dtype)
        if len(batch["labels"].shape) == 1:
            labels = labels.unsqueeze(-1)
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "special_tokens_mask": special_tokens_mask,
            "target_ids": target_ids,
            "labels": labels,
        }

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): A collated batch of data containing input_ids, attention_mask, and labels.

        Returns:
            Tensor: The decoder logits
        """
        encoder_hidden = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )
        logits = self.adapter(encoder_hidden, collated_batch["labels"])
        return logits

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions from forward against the ground truth labels.

        Args:
            logits (Tensor): The token-wise predicted logits
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing target_ids
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            Tensor: The loss.
        """
        target_ids = collated_batch["target_ids"]
        loss = self.loss(logits.permute(0, 2, 1).contiguous(), target_ids)
        if loss_only:
            return {"loss": loss}
        preds = logits.argmax(-1)
        metrics = self.get_metrics_by_stage(stage)
        self.call_or_update_metric(
            stage, metrics["accuracy"], (preds == target_ids).float().mean()
        )
        return {"loss": loss}


class ConditionalDiffusion(Diffusion):
    """Task for Conditional Diffusion Language Modeling training and denoising on sequences (https://arxiv.org/abs/2406.07524). Inherits from Diffusion.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int, int, nn.Module], ConditionalGenerationAdapter], optional): The callable that returns an adapter. Defaults to ConditionalLMAdapter.
        use_legacy_adapter (bool, optional):
            Whether to use the pre-trained legacy adapter within the conditional decoder. Defaults to True.
        condition_dim (int, optional): The dimension of the condition. Defaults to 1.
        sample_seq (bool, optional): Whether to sample tokens during denoising. Defaults to False.
        num_denoise_steps (int, optional): The number of denoising steps to take. Defaults to 4.
        sampling_temperature (float, optional): The temperature for sampling tokens. Defaults to 1.0.
        normalize_posterior_weights (bool, optional): Whether to normalize posterior weights. Defaults to False.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        use_legacy_adapter (bool, optional):
            Whether to use the adapter from the backbone. Defaults to False.
            Will be deprecated once the new adapter API is fully verified.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    def __init__(
        self,
        adapter: Optional[
            Callable[[int, int, int, nn.Module], ConditionalGenerationAdapter]
        ] = ConditionalLMAdapter,
        use_legacy_adapter: bool = True,
        condition_dim: int = 1,
        **kwargs,
    ):
        super().__init__(use_legacy_adapter=use_legacy_adapter, **kwargs)
        if self.__class__ is ConditionalDiffusion:
            self.save_hyperparameters()
        self.adapter = None
        self.adapter_fn = adapter
        self.condition_dim = condition_dim

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        if self.use_legacy_adapter:
            self.backbone = self.backbone_fn(LegacyAdapterType.MASKED_LM, None)
        else:
            self.backbone = self.backbone_fn(None, None)
        self.adapter = self.adapter_fn(
            self.backbone.get_embedding_size(),
            self.condition_dim,
            self.backbone.get_vocab_size(),
            self.backbone.get_decoder() if self.use_legacy_adapter else None,
        )
        self.mask_id = self.backbone.get_token_id("[MASK]")

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences, target_sequences, posterior_weights, and labels
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with input_ids, input_masks, attention_mask, target_ids, target_masks, posterior_weights, and labels
        """
        collated_batch = super().transform(batch, batch_idx)
        labels = torch.cat(batch["labels"]).type(self.dtype)
        if len(labels.shape) == 1:
            labels = labels.unsqueeze(-1)
        collated_batch.update({"labels": labels})
        return collated_batch

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): A collated batch of data containing input_ids and attention_mask

        Returns:
            Tensor: The decoder logits
        """
        encoder_hidden = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )
        logits = self.adapter(encoder_hidden, collated_batch["labels"])
        return logits


class SequenceRegression(TaskInterface):
    """Task for fine-tuning a model on a regression task.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int], SequenceAdapter], optional): The callable that returns an adapter. Defaults to LinearCLSAdapter.
        num_outputs (int, optional): The number of outputs in the regression task. Defaults to 1.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        adapter: Optional[Callable[[int, int], SequenceAdapter]] = LinearCLSAdapter,
        num_outputs: int = 1,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if self.__class__ is SequenceRegression:
            self.save_hyperparameters()
        self.backbone_fn = backbone
        self.adapter_fn = adapter
        self.num_outputs = num_outputs
        self.backbone = None
        self.adapter = None
        self.loss = nn.MSELoss()
        for stage in ["train", "val", "test"]:
            self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                {
                    "pearson": tm.PearsonCorrCoef(num_outputs=num_outputs),
                    "spearman": tm.SpearmanCorrCoef(num_outputs=num_outputs),
                    "mae": tm.MeanAbsoluteError(num_outputs=num_outputs),
                    "r2": tm.R2Score(),
                    "mse": tm.MeanSquaredError(num_outputs=num_outputs),
                }
            )
        self.metrics_to_pbar = set(self.metrics["train_metrics"].keys())

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        if self.use_legacy_adapter:
            self.backbone = self.backbone_fn(
                LegacyAdapterType.SEQ_CLS,
                DefaultConfig(
                    config_overwrites={
                        "problem_type": "regression",
                        "num_labels": self.num_outputs,
                    }
                ),
            )
            self.adapter = self.backbone.get_decoder()
        else:
            self.backbone = self.backbone_fn(None, None)
            self.adapter = self.adapter_fn(
                self.backbone.get_embedding_size(), self.num_outputs
            )

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data into a format that can be passed to the forward and evaluate methods.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data containing sequences and labels
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch containing sequences, input_ids, attention_mask, and labels
        """
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            batch["sequences"]
        )
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        labels = None
        if batch.get("labels") is not None:
            labels = batch["labels"].to(self.device, dtype=self.dtype)
        return {
            "sequences": batch["sequences"],
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "special_tokens_mask": special_tokens_mask,
            "labels": labels,
        }

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): A collated batch of data containing input_ids and attention_mask.

        Returns:
            Tensor: The regression predictions
        """
        hidden_states = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )  # (bs, seq_len, dim)
        preds = self.adapter(hidden_states, collated_batch["attention_mask"])
        return preds

    def evaluate(
        self,
        preds: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions against the ground truth labels.

        Args:
            logits (Tensor): The model predictions
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing labels
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            dict[str, Union[Tensor, float]]: A dictionary of metrics containing loss and mse
        """
        labels = collated_batch["labels"]
        loss = self.loss(preds, labels)
        if loss_only:
            return {"loss": loss}
        metrics = self.get_metrics_by_stage(stage)
        for metric in metrics.values():
            self.call_or_update_metric(stage, metric, preds, labels)
        return {"loss": loss}


class SequenceRegressionWithScaling(SequenceRegression):
    """Task for fine-tuning a model on a regression task with scaling, where the label is scaled with dynamically adjusted mean and standard derivation.

    Note:
        Does not tolerate legacy adapters.

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        adapter (Callable[[int, int], SequenceAdapter], optional): The callable that returns an adapter. Defaults to LinearCLSAdapter.
        num_outputs (int, optional): The number of outputs in the regression task. Defaults to 1.
        optimizer (OptimizerCallable, optional): The optimizer to use for training. Defaults to torch.optim.AdamW.
        lr_scheduler (LRSchedulerCallable, optional): The learning rate scheduler to use for training. Defaults to None.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
        reset_optimizer_states (bool, optional): Whether to reset the optimizer states. Defaults to False.
            Set it to True if you want to replace the adapter (e.g. for continue pretraining).
    """

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        adapter: Optional[Callable[[int, int], SequenceAdapter]] = LinearCLSAdapter,
        num_outputs: int = 1,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if self.__class__ is SequenceRegressionWithScaling:
            self.save_hyperparameters()
        self.backbone_fn = backbone
        self.adapter_fn = adapter
        self.num_outputs = num_outputs
        self.backbone = None
        self.adapter = None
        self.loss = nn.MSELoss()
        self.scaler = (
            self.StandardScaler()
        )  ## Adapted from https://github.com/lbcb-sci/RiNALMo/blob/main/train_ribosome_loading.py
        for stage in ["train", "val", "test"]:
            self.metrics[f"{stage}_metrics"] = nn.ModuleDict(
                {
                    # "pearson": tm.PearsonCorrCoef(num_outputs=num_outputs),
                    # "spearman": tm.SpearmanCorrCoef(num_outputs=num_outputs),
                    # "mae": tm.MeanAbsoluteError(num_outputs=num_outputs),
                    "r2": tm.R2Score(),
                    # "mse": tm.MeanSquaredError(num_outputs=num_outputs),
                }
            )
        self.metrics_to_pbar = set(self.metrics["train_metrics"].keys())

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): A collated batch of data containing input_ids and attention_mask.

        Returns:
            Tensor: The regression predictions
        """
        ## Adapted from https://github.com/lbcb-sci/RiNALMo/blob/main/train_ribosome_loading.py

        hidden_states = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )  # (bs, seq_len, dim)

        tokens = collated_batch["input_ids"]

        # Nullify padding token representations
        padding_mask = ~collated_batch[
            "attention_mask"
        ]  # padding_mask = tokens.eq(self.pad_idx)
        hidden_states[padding_mask, :] = 0.0
        hidden_states = hidden_states[:, 1:-1, :]
        padding_mask = padding_mask[:, 1:-1]

        preds = self.adapter(hidden_states, padding_mask)
        return preds

    def evaluate(
        self,
        preds: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["train", "val", "test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions against the ground truth labels.

        Args:
            logits (Tensor): The model predictions
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing labels
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        Returns:
            dict[str, Union[Tensor, float]]: A dictionary of metrics containing loss and mse
        """
        labels = collated_batch["labels"]
        scaled_labels = self.scaler.transform(labels)  # "Scale" labels
        loss = self.loss(preds, scaled_labels)

        preds = self.scaler.inverse_transform(preds).clamp(
            min=0.0
        )  # "Unscale" predictions

        if loss_only:
            return {"loss": loss}
        metrics = self.get_metrics_by_stage(stage)
        for metric in metrics.values():
            self.call_or_update_metric(stage, metric, preds, labels)
        return {"loss": loss}

    def training_step(self, collated_batch, batch_idx):
        if batch_idx == 0:
            trainable_param = sum(
                p.numel() for p in self.parameters() if p.requires_grad
            )
            self.log("TrPara", trainable_param, prog_bar=True)
        if self.current_epoch == 0:
            return self.scaler.partial_fit(collated_batch["labels"])

        return super().training_step(collated_batch, batch_idx)

    class StandardScaler(nn.Module):
        # Adapted from https://github.com/lbcb-sci/RiNALMo/blob/main/rinalmo/utils/scaler.py
        # Inspired by https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
        def __init__(self) -> None:
            super().__init__()

            self.register_buffer("_mean", torch.tensor([0.0]))
            self.register_buffer("_std", torch.tensor([1.0]))

            self._seen_samples = []

            self._need_update = False

        def _update_mean_and_std(self) -> None:
            self._mean[0] = np.mean(self._seen_samples)
            self._std[0] = np.std(self._seen_samples)

        def partial_fit(self, x: torch.Tensor) -> None:
            self._need_update = True
            self._seen_samples.extend(x.cpu().view(-1).tolist())

            self._update_mean_and_std()

        def transform(self, x: torch.Tensor) -> torch.Tensor:
            return (x - self._mean) / self._std

        def inverse_transform(self, scaled_x: torch.Tensor) -> torch.Tensor:
            return scaled_x * self._std + self._mean


class Embed(TaskInterface):
    """Task for getting embeddings from a backbone. This task is used only for inference.

    Note:
        Must be used with modelgenerator.callbacks.PredictionWriter. Embeddings are stored under "predictions".

    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        batch_size (int, optional): The batch size to use for training. Defaults to None.
        strict_loading (bool, optional): Whether to strictly load the model. Defaults to True.
            Set it to False if you want to replace the adapter (e.g. for continue pretraining)
    """

    def __init__(self, backbone: BackboneCallable = aido_dna_dummy, **kwargs):
        super().__init__(use_legacy_adapter=False, **kwargs)
        if self.__class__ is Embed:
            self.save_hyperparameters()
        self.backbone = None
        self.adapter = None
        self.backbone_fn = backbone

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        self.backbone = self.backbone_fn(LegacyAdapterType.MASKED_LM, None)

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with sequences, input_ids, and attention_mask
        """
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            batch["sequences"]
        )
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        return {
            "sequences": batch["sequences"],
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "special_tokens_mask": special_tokens_mask,
        }

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data from collate containing input_ids and attention_mask.

        Returns:
            Tensor: The decoder logits
        """
        encoder_hidden = self.backbone(
            collated_batch["input_ids"], collated_batch["attention_mask"]
        )
        return encoder_hidden


class ZeroshotPredictionDiff(TaskInterface):
    """Task for zero-shot prediction on masked languange model. This task is used to evaluate the embeddings of pretrained model
       The evaluation metrics are AUROC and AUPRC, which compute the log-likelihood difference between probability of ref and alt at the mutated position
    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
    """

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        use_legacy_adapter: bool = True,
        **kwargs,
    ):
        if self.__class__ is ZeroshotPredictionDiff:
            self.save_hyperparameters()
        super().__init__(use_legacy_adapter=True, **kwargs)
        self.backbone = None
        self.adapter = None
        self.backbone_fn = backbone
        self.metrics[f"test_metrics"] = nn.ModuleDict(
            {"AUROC": AUROC(), "AUPRC": AUPRC()}
        )
        self.metrics_to_pbar = {"AUROC", "AUPRC"}

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        self.backbone = self.backbone_fn(LegacyAdapterType.MASKED_LM, None)
        self.adapter = self.backbone.get_decoder()

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences and target_sequences
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with input_ids, attention_mask, and target_ids
        """
        input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
            batch["sequences"]
        )
        labels = None
        ref_ids = None
        mutation_ids = None
        if batch.get("labels") is not None:
            labels = batch["labels"]
        if batch.get("refs") is not None:
            ref_ids, _, _ = self.backbone.tokenize(
                batch["refs"], add_special_tokens=False
            )
            ref_ids = torch.tensor(ref_ids, dtype=torch.long, device=self.device)
        if batch.get("mutations") is not None:
            mutation_ids, _, _ = self.backbone.tokenize(
                batch["mutations"], add_special_tokens=False
            )
            mutation_ids = torch.tensor(
                mutation_ids, dtype=torch.long, device=self.device
            )
        input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(self.device)
        return {
            "input_ids": input_ids,
            "ref_ids": ref_ids,
            "mutation_ids": mutation_ids,
            "labels": labels,
            "special_tokens_mask": special_tokens_mask,
        }

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data from collate

        Returns:
            Tensor: The decoder logits
        """
        encoder_hidden = self.backbone(collated_batch["input_ids"], attention_mask=None)
        decoder_logits = self.adapter(encoder_hidden)
        b, l, d = decoder_logits.shape
        # remove special token before computing zeroshot score
        special_tokens_mask = collated_batch["special_tokens_mask"]
        decoder_logits = decoder_logits[torch.logical_not(special_tokens_mask)].view(
            b, -1, d
        )
        return decoder_logits

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions from forward against the ground truth labels.

        Args:
            logits (Tensor): The token-wise predicted logits
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing ref_ids, mutation_ids
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        """
        outputs = {}
        ref_ids = collated_batch["ref_ids"]
        mutation_ids = collated_batch["mutation_ids"]
        snp_location = logits.shape[1] // 2
        probs = F.softmax(logits, dim=2)
        snp_probs = probs[:, snp_location, :]

        ref_probs = torch.gather(snp_probs, 1, ref_ids)
        mutate_probs = torch.gather(snp_probs, 1, mutation_ids)

        log_ratios = torch.log(mutate_probs / ref_probs)
        metrics = self.get_metrics_by_stage(stage)
        for acc in metrics.values():
            self.call_or_update_metric(
                stage, acc, log_ratios.view(-1), collated_batch["labels"]
            )
        outputs["score"] = log_ratios.view(-1).cpu().tolist()
        outputs["label"] = collated_batch["labels"].cpu().tolist()
        outputs["loss"] = -1
        return outputs


class ZeroshotPredictionDistance(TaskInterface):
    """Task for zero-shot prediction on masked languange model. This task is used to evaluate the embeddings of pretrained model
       The evaluation metric is L1, L2 distance between reference and alt sequence embeddings extracted from every layer
    Args:
        backbone (BackboneCallable, optional): The callable that returns a backbone. Defaults to aido_dna_dummy.
        use_legacy_adapter (bool): Whether we use adapter in huggingface model
    """

    def __init__(
        self,
        backbone: BackboneCallable = aido_dna_dummy,
        use_legacy_adapter: bool = True,
        **kwargs,
    ):
        if self.__class__ is ZeroshotPredictionDistance:
            self.save_hyperparameters()
        super().__init__(use_legacy_adapter=True, **kwargs)
        self.backbone = None
        self.adapter = None
        self.backbone_fn = backbone

    def configure_model(self) -> None:
        if self.backbone is not None:
            return
        self.backbone = self.backbone_fn(LegacyAdapterType.MASKED_LM, None)
        self.adapter = self.backbone.get_decoder()
        self.n_layers = self.backbone.get_num_layer()
        metrics_dict = {}
        for i in range(self.n_layers):
            metrics_dict.update(
                {
                    f"L1_AUROC_layer_{i+1}": AUROC(),
                    f"L1_AUPRC_layer_{i+1}": AUPRC(),
                    f"L2_AUROC_layer_{i+1}": AUROC(),
                    f"L2_AUPRC_layer_{i+1}": AUPRC(),
                }
            )
        self.metrics[f"test_metrics"] = nn.ModuleDict(metrics_dict)
        self.metrics_to_pbar = set()
        for i in range(self.n_layers):
            self.metrics_to_pbar.update(
                {
                    f"L1_AUROC_layer_{i+1}",
                    f"L1_AUPRC_layer_{i+1}",
                    f"L2_AUROC_layer_{i+1}",
                    f"L2_AUPRC_layer_{i+1}",
                }
            )

    def transform(
        self, batch: dict[str, Union[list, Tensor]], batch_idx: Optional[int] = None
    ) -> dict[str, Union[list, Tensor]]:
        """Collates a batch of data for forward and evaluate.

        Args:
            batch (dict[str, Union[list, Tensor]]): A batch of data from the DataLoader containing sequences and target_sequences
            batch_idx (int, optional): The index of the current batch in the DataLoader

        Returns:
            dict[str, Union[list, Tensor]]: The collated batch with ref_ids,mutation_id and labels
        """
        processed_batch = {}
        for key in batch.keys():
            if "sequences" in key:  # tokenize sequence
                # Note: previous version, add_special_token = False
                input_ids, attention_mask, special_tokens_mask = self.backbone.tokenize(
                    batch[key]
                )
                input_ids = torch.tensor(input_ids, dtype=torch.long).to(self.device)
                attention_mask = torch.tensor(attention_mask, dtype=torch.long).to(
                    self.device
                )
                processed_batch[key.replace("sequences", "input_ids")] = input_ids
                processed_batch["special_tokens_mask"] = special_tokens_mask
            else:
                processed_batch[key] = batch[key]
        return processed_batch

    def forward(self, collated_batch: dict[str, Union[list, Tensor]]) -> Tensor:
        """Runs a forward pass of the model.

        Args:
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data from collate

        Returns:
            Tensor: The decoder logits
        """
        ref_encoder_hidden = torch.stack(
            self.backbone(
                collated_batch["ref_input_ids"],
                attention_mask=None,
                all_hidden_states=True,
            )[1:]
        )
        mutation_encoder_hidden = torch.stack(
            self.backbone(
                collated_batch["mutation_input_ids"],
                attention_mask=None,
                all_hidden_states=True,
            )[1:]
        )
        # remove special token before computing zeroshot score
        n, b, s, d = ref_encoder_hidden.shape
        ref_encoder_hidden = ref_encoder_hidden[
            :, torch.logical_not(collated_batch["special_tokens_mask"])
        ].view(n, b, -1, d)
        mutation_encoder_hidden = mutation_encoder_hidden[
            :, torch.logical_not(collated_batch["special_tokens_mask"])
        ].view(n, b, -1, d)
        return torch.stack([ref_encoder_hidden, mutation_encoder_hidden])

    def evaluate(
        self,
        logits: Tensor,
        collated_batch: dict[str, Union[list, Tensor]],
        stage: Optional[Literal["test"]] = None,
        loss_only: bool = False,
    ) -> dict[str, Union[Tensor, float]]:
        """Evaluates the model predictions from forward against the ground truth labels.

        Args:
            logits (Tensor): list of ref_hidden_states and mutation_hidden_states
            collated_batch (dict[str, Union[list, Tensor]]): The collated batch of data containing ref_ids, mutation_ids
            stage (Optional[str], optional): The stage of training (train, val, test). Required if loss_only is False.
            loss_only (bool, optional): Whether to only return the loss. Defaults to False.

        """
        ref_hidden_states = logits[0]
        mutation_hidden_states = logits[1]
        prediction_dict = {
            key: [] for key in collated_batch.keys() if "sequences" not in key
        }
        # add score related keys
        prediction_dict["norm_type"] = []
        prediction_dict["score"] = []
        prediction_dict["num_layer"] = []
        metrics = self.get_metrics_by_stage(stage)
        batch_size = ref_hidden_states.shape[1]
        # update metrics of each layer embedding
        for key in metrics.keys():
            index = int(key.split("_")[-1]) - 1
            norm_type = key.split("_")[0]
            score = self._compute_norm_score(
                norm_type, ref_hidden_states[index], mutation_hidden_states[index]
            )
            self.call_or_update_metric(
                stage, metrics[key], score, collated_batch["labels"]
            )
        # prepare prediction score to be saved to a tsv file
        for i in range(self.n_layers):
            for norm_type in ["L1", "L2"]:
                score = self._compute_norm_score(
                    norm_type, ref_hidden_states[index], mutation_hidden_states[index]
                )
                prediction_dict["score"].extend(score.cpu().tolist())
                prediction_dict["norm_type"].extend([norm_type] * batch_size)
                prediction_dict["num_layer"].extend([index] * batch_size)
                for key in collated_batch.keys():
                    if "sequences" not in key:
                        try:
                            prediction_dict[key].extend(
                                collated_batch[key].cpu().tolist()
                            )
                        except:
                            prediction_dict[key].extend(collated_batch[key])
        prediction_dict.update({"loss": -1})
        outputs = prediction_dict
        return outputs

    def _compute_norm_score(self, norm_type, ref_hidden_state, mutation_hidden_state):
        """Compute norm score between reference and mutation embeddings from one layer

        Args:
            norm_type (str): norm type. Options are 'L1' and 'L2'
            ref_hidden_state (Tensor): Reference sequence embeddings of one layer
            mutation_hidden_state (Tensor): Variant sequence embeddings of one layer
        Returns:
            score (Tensor): norm distance score

        """
        if norm_type == "L1":
            score = torch.abs(
                ref_hidden_state.mean(dim=-2) - mutation_hidden_state.mean(dim=-2)
            ).sum(dim=1)
        else:
            score = torch.norm(
                ref_hidden_state.mean(dim=-2) - mutation_hidden_state.mean(dim=-2),
                p=2,
                dim=1,
            )
        return score
