import os
from modelgenerator.backbones.backbones import *
from modelgenerator.backbones.base import *


aido_rna_1m_mars = type(
    "aido_rna_1m_mars",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.RNA-1M-MARS",
    },
)
aido_rna_25m_mars = type(
    "aido_rna_25m_mars",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.RNA-25M-MARS",
    },
)
aido_rna_300m_mars = type(
    "aido_rna_300m_mars",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.RNA-300M-MARS",
    },
)
aido_rna_650m = type(
    "aido_rna_650m",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.RNA-650M",
    },
)
aido_rna_650m_cds = type(
    "aido_rna_650m_cds",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.RNA-650M-CDS",
    },
)
aido_rna_1b600m = type(
    "aido_rna_1b600m",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.RNA-1.6B",
    },
)
aido_rna_1b600m_cds = type(
    "aido_rna_1b600m_cds",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.RNA-1.6B-CDS",
    },
)
aido_dna_dummy = type(
    "aido_dna_dummy",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.DNA-dummy",
    },
)
aido_dna_300m = type(
    "aido_dna_300m",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.DNA-300M",
    },
)
aido_dna_7b = type(
    "aido_dna_7b",
    (GenBioBERT,),
    {
        "model_path": "genbio-ai/AIDO.DNA-7B",
    },
)
aido_protein_16b = type(
    "aido_protein_16b",
    (GenBioFM,),
    {
        "model_path": "genbio-ai/AIDO.Protein-16B",
    },
)

aido_protein_16b_v1 = type(
    "aido_protein_16b_v1",
    (GenBioFM,),
    {
        "model_path": "genbio-ai/AIDO.Protein-16B-v1",
    },
)

aido_protein2structoken_16b = type(
    "aido_protein2structoken_16b",
    (GenBioFM,),
    {
        "model_path": "genbio-ai/AIDO.Protein2StructureToken-16B",
    },
)


class aido_protein_debug(GenBioFM):
    """
    A small protein mixture-of-experts transformer model created from scratch for debugging purposes only
    """

    def __init__(self, *args, **kwargs):
        config_overwrites = {
            "hidden_size": 64,
            "num_hidden_layers": 2,
            "num_attention_heads": 4,
            "intermediate_size": 128,
            "num_experts": 2,
        }
        super().__init__(
            *args, from_scratch=True, config_overwrites=config_overwrites, **kwargs
        )


class aido_dna_debug(GenBioBERT):
    """
    A small dna dense transformer model created from scratch for debugging purposes only
    """

    def __init__(self, *args, **kwargs):
        config_overwrites = {
            "hidden_size": 64,
            "num_hidden_layers": 2,
            "num_attention_heads": 4,
            "intermediate_size": 128,
        }
        super().__init__(
            *args, from_scratch=True, config_overwrites=config_overwrites, **kwargs
        )


dna_onehot = type(
    "onehot",
    (Onehot,),
    {
        "vocab_file": os.path.join(
            Path(__file__).resolve().parent.parent.parent,
            "modelgenerator/huggingface_models/rnabert/vocab.txt",
        ),
    },
)

protein_onehot = type(
    "onehot",
    (Onehot,),
    {
        "vocab_file": os.path.join(
            Path(__file__).resolve().parent.parent.parent,
            "modelgenerator/huggingface_models/fm4bio/vocab_protein.txt",
        ),
    },
)

aido_cell_3m = type(
    "aido_cell_3m",
    (GenBioCellFoundation,),
    {"model_path": "genbio-ai/AIDO.Cell-3M"},
)

aido_cell_10m = type(
    "aido_cell_10m",
    (GenBioCellFoundation,),
    {"model_path": "genbio-ai/AIDO.Cell-10M"},
)

aido_cell_100m = type(
    "aido_cell_100m",
    (GenBioCellFoundation,),
    {"model_path": "genbio-ai/AIDO.Cell-100M"},
)
