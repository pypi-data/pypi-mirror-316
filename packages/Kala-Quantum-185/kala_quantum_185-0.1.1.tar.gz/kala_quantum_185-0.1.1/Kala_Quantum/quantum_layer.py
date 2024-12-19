import numpy as np
from .quantum_core import QuantumState, hadamard, pauli_x, pauli_z, cnot

class QuantumLayer:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state = QuantumState(num_qubits)

    def forward(self, inputs):
        """
        Applies quantum operations based on input values.
        - `inputs` is a numpy array of real numbers, scaled to the range [0, 1].
        """
        # Ensure inputs are 1D (flattened)
        inputs = np.asarray(inputs).flatten()

        if len(inputs) < self.num_qubits:
            raise ValueError(f"Expected at least {self.num_qubits} input values, got {len(inputs)}")

        for i in range(self.num_qubits):  # Iterate over the first num_qubits elements
            val = inputs[i]
            if val > 0.5:  # Scalar comparison
                self.state.apply_gate(hadamard(), i)
            else:
                self.state.apply_gate(pauli_x(), i)
        
        # Measure the final state
        measurement = self.state.measure()
        return np.array([int(x) for x in format(measurement, f'0{self.num_qubits}b')])

    def reset(self):
        """Resets the quantum state."""
        self.state = QuantumState(self.num_qubits)
