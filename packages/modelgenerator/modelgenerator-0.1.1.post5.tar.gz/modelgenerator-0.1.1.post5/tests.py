import unittest
from modelgenerator.backbones import (
    aido_dna_debug,
    aido_protein_debug,
    dna_onehot,
    protein_onehot,
)
from modelgenerator.data import *
from modelgenerator.tasks import *
from functools import partial
from lightning import Trainer


class TestDatasets(unittest.TestCase):

    def setUp(self):
        self.sequence_adapter_partial = partial(LinearCLSAdapter)
        self.token_adapter_partial = partial(LinearAdapter)
        self.conditional_generation_adapter_partial = partial(ConditionalLMAdapter)
        self.trainer = Trainer(fast_dev_run=True)

    def _test(self, task, data):
        trainer = Trainer(fast_dev_run=True)
        trainer.fit(task, data)
        trainer.test(task, data)

    def test_NTClassification(self):
        data = NTClassification()
        task = SequenceClassification(
            backbone=aido_dna_debug,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_GUEClassification(self):
        data = GUEClassification()
        task = SequenceClassification(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_MLMDataModule(self):
        data = MLMDataModule(
            path="InstaDeepAI/nucleotide_transformer_downstream_tasks",
            config_name="enhancers",
        )
        task = MLM(
            backbone=aido_dna_debug,
        )
        self._test(task, data)

    def test_TranslationEfficiency(self):
        data = TranslationEfficiency(normalize=False)
        task = SequenceRegression(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_ExpressionLevel(self):
        data = ExpressionLevel(normalize=False)
        task = SequenceRegression(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_TranscriptAbundance(self):
        data = TranscriptAbundance(normalize=False)
        task = SequenceRegression(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_ProteinAbundance(self):
        data = ProteinAbundance(normalize=False)
        task = SequenceRegression(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_NcrnaFamilyClassification(self):
        data = NcrnaFamilyClassification()
        task = SequenceClassification(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
            n_classes=88,
        )
        self._test(task, data)

    def test_SpliceSitePrediction(self):
        data = SpliceSitePrediction()
        task = SequenceClassification(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_ModificationSitePrediction(self):
        data = ModificationSitePrediction()
        task = SequenceClassification(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
            n_classes=12,
            multilabel=True,
        )
        self._test(task, data)

    def test_PromoterExpressionRegression(self):
        data = PromoterExpressionRegression(
            train_split_files=["test.tsv"],  # Make it go fast
            test_split_files=["test.tsv"],
            normalize=False,
        )
        task = SequenceRegression(
            backbone=dna_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_PromoterExpressionGeneration(self):
        data = PromoterExpressionGeneration(
            train_split_files=["test.tsv"],  # Make it go fast
            test_split_files=["test.tsv"],
            normalize=False,
        )
        task = ConditionalDiffusion(
            backbone=aido_dna_debug,
            adapter=self.conditional_generation_adapter_partial,
            use_legacy_adapter=True,
        )
        self._test(task, data)

    def test_DMSFitnessPrediction(self):
        data = DMSFitnessPrediction(normalize=False)
        task = SequenceRegression(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_Embed(self):
        data = NTClassification()
        task = Embed(
            backbone=dna_onehot,
        )
        self.trainer.predict(task, data)

    def test_Inference(self):
        data = NTClassification()
        task = Inference(
            backbone=dna_onehot,
        )
        self.trainer.predict(task, data)

    def test_ContactPredictionBinary(self):
        data = ContactPredictionBinary()
        task = PairwiseTokenClassification(
            backbone=protein_onehot,
            adapter=self.token_adapter_partial,
        )
        self._test(task, data)

    def test_SspQ3(self):
        data = SspQ3()
        task = TokenClassification(
            backbone=protein_onehot, adapter=self.token_adapter_partial, n_classes=3
        )
        self._test(task, data)

    def test_FoldPrediction(self):
        data = FoldPrediction()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
            n_classes=1195,
        )
        self._test(task, data)

    def test_LocalizationPrediction(self):
        data = LocalizationPrediction()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
            n_classes=10,
        )
        self._test(task, data)

    def test_MetalIonBinding(self):
        data = MetalIonBinding()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_SolubilityPrediction(self):
        data = SolubilityPrediction()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_AntibioticResistance(self):
        data = AntibioticResistance()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
            n_classes=19,
        )
        self._test(task, data)

    def test_CloningClf(self):
        data = CloningClf()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_MaterialProduction(self):
        data = MaterialProduction()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_TcrPmhcAffinity(self):
        data = TcrPmhcAffinity()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_PeptideHlaMhcAffinity(self):
        data = PeptideHlaMhcAffinity()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_TemperatureStability(self):
        data = TemperatureStability()
        task = SequenceClassification(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_DiffusionDataModule(self):
        data = DiffusionDataModule(
            path="InstaDeepAI/nucleotide_transformer_downstream_tasks",
            config_name="enhancers",
        )
        task = Diffusion(
            backbone=dna_onehot,
            adapter=self.token_adapter_partial,
            use_legacy_adapter=False,
        )
        self._test(task, data)

    def test_ClassDiffusionDataModule(self):
        data = ClassDiffusionDataModule(
            path="InstaDeepAI/nucleotide_transformer_downstream_tasks",
            config_name="enhancers",
            class_filter=1,
        )
        task = Diffusion(
            backbone=dna_onehot,
            adapter=self.token_adapter_partial,
            use_legacy_adapter=False,
        )
        self._test(task, data)

    def test_FluorescencePrediction(self):
        data = FluorescencePrediction(normalize=False)
        task = SequenceRegression(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_FitnessPrediction(self):
        data = FitnessPrediction(normalize=False)
        task = SequenceRegression(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_StabilityPrediction(self):
        data = StabilityPrediction(normalize=False)
        task = SequenceRegression(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_EnzymeCatalyticEfficiencyPrediction(self):
        data = EnzymeCatalyticEfficiencyPrediction(normalize=False)
        task = SequenceRegression(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_OptimalTemperaturePrediction(self):
        data = OptimalTemperaturePrediction(normalize=False)
        task = SequenceRegression(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)

    def test_OptimalPhPrediction(self):
        data = OptimalPhPrediction(normalize=False)
        task = SequenceRegression(
            backbone=protein_onehot,
            adapter=self.sequence_adapter_partial,
        )
        self._test(task, data)


if __name__ == "__main__":
    unittest.main()
