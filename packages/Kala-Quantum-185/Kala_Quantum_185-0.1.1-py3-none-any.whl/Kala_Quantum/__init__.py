from .datasets import CodeDataset
from .models import CodeLanguageModel, HybridModel
from .quantum_core import QuantumState,hadamard,cnot,pauli_x,pauli_z,pauli_y,phase_gate,t_gate,s_gate,swap_gate,toffoli,fredkin
from .quantum_layer import QuantumLayer
from .tokenizer import SimpleTokenizer
from .train import train_model

# Explicitly declare the public API
__all__ = [
    "CodeDataset",
    "SimpleTokenizer",
    "CodeLanguageModel",
    "HybridModel",
    "train_model",
    "QuantumLayer",
    "QuantumState",
    "handamard",
    "cnot",
    "pauli_x",
    "pauli_z",
    "train_model_and_save",
    "hadamard",
    "pauli_y",
    "phase_gate",
    "t_gate",
    "s_gate",
    "swap_gate",
    "toffoli",
    "fredkin"
]

__version__ = "0.1.1"


