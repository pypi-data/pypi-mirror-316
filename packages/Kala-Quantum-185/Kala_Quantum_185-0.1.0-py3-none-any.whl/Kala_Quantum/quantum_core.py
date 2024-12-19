import numpy as np

class QuantumState:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1  # Initialize to |0...0>

    def apply_gate(self, gate, qubit):
        """Applies a single-qubit gate to the specified qubit."""
        full_gate = np.eye(1)
        for i in range(self.num_qubits):
            if i == qubit:
                full_gate = np.kron(full_gate, gate)
            else:
                full_gate = np.kron(full_gate, np.eye(2))
        self.state = np.dot(full_gate, self.state)
        self._normalize_state()

    def apply_cnot(self, control, target):
        """Applies a CNOT gate to control and target qubits."""
        num_states = 2**self.num_qubits
        full_gate = np.eye(num_states, dtype=complex)  # Identity matrix

        for i in range(num_states):
            binary = format(i, f"0{self.num_qubits}b")
            if binary[control] == '1':
                target_state = list(binary)
                target_state[target] = '1' if binary[target] == '0' else '0'
                j = int("".join(target_state), 2)
                full_gate[i, i] = 0
                full_gate[i, j] = 1
            else:
                full_gate[i, i] = 1

        self.state = np.dot(full_gate, self.state)
        self._normalize_state()

    def measure(self):
        """Simulates a measurement in the computational basis."""
        probabilities = np.abs(self.state)**2
        outcome = np.random.choice(len(probabilities), p=probabilities)
        print(f"Measurement outcome: |{bin(outcome)[2:].zfill(self.num_qubits)}>")
        return outcome

    def print_state(self):
        """Prints the current quantum state."""
        print("Quantum State:")
        for i, amplitude in enumerate(self.state):
            print(f"|{bin(i)[2:].zfill(self.num_qubits)}> : {amplitude:.4f}")

    def _normalize_state(self):
        """Normalizes the quantum state."""
        norm = np.linalg.norm(self.state)
        if norm != 0:
            self.state /= norm

def hadamard():
    return np.array([[1, 1], [1, -1]]) / np.sqrt(2)

def pauli_x():
    return np.array([[0, 1], [1, 0]])

def pauli_z():
    return np.array([[1, 0], [0, -1]])

def cnot():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])

# Example usage
if __name__ == "__main__":
    qs = QuantumState(num_qubits=2)

    print("Initial State:")
    qs.print_state()

    qs.apply_gate(hadamard(), qubit=0)
    print("\nAfter Hadamard on Qubit 0:")
    qs.print_state()

    qs.apply_cnot(control=0, target=1)
    print("\nAfter CNOT (Control: Qubit 0, Target: Qubit 1):")
    qs.print_state()

    qs.measure()
