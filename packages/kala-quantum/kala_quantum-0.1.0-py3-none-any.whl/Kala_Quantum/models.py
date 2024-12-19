import torch
import torch.nn as nn
from .quantum_layer import QuantumLayer
import numpy as np

class CodeLanguageModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim=128, hidden_dim=256, num_layers=2):
        super(CodeLanguageModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        self.softmax = nn.LogSoftmax(dim=-1)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        output = self.fc(lstm_out)
        return self.softmax(output)

import torch.nn.functional as F
import torch
import torch.nn as nn
import torch.nn.functional as F
from .quantum_layer import QuantumLayer
import numpy as np

class HybridModel(nn.Module):
    def __init__(self, classical_model, num_qubits):
        super(HybridModel, self).__init__()
        self.classical_model = classical_model
        self.quantum_layer = QuantumLayer(num_qubits)
        self.num_qubits = num_qubits

    def forward(self, x):
        # Classical computation
        classical_output = self.classical_model(x)  # Shape: (batch_size, seq_len, vocab_size)
        batch_size, seq_len, vocab_size = classical_output.size()

        # Convert classical output to quantum input
        quantum_input = torch.sigmoid(classical_output).detach().cpu().numpy()  # Scale to [0, 1]

        # Quantum computation
        quantum_output = []
        for sample in quantum_input:
            self.quantum_layer.reset()  # Reset quantum state
            quantum_seq = []
            for timestep in sample:
                quantum_seq.append(self.quantum_layer.forward(timestep[:self.num_qubits]))  # Use first `num_qubits`
            quantum_output.append(quantum_seq)

        # Convert quantum output to tensor
        quantum_output = torch.tensor(quantum_output, dtype=torch.float32, device=classical_output.device)
        quantum_output = quantum_output.requires_grad_(True)  # Ensure gradients are tracked

        # Match dimensions of quantum_output to classical_output
        if quantum_output.size(-1) < vocab_size:
            repeats = vocab_size // quantum_output.size(-1)
            quantum_output = quantum_output.repeat(1, 1, repeats)

        # Trim excess dimensions if repeated too much
        quantum_output = quantum_output[:, :, :vocab_size]

        # Combine outputs
        combined_output = classical_output + quantum_output

        # Apply LogSoftmax for final output
        return F.log_softmax(combined_output, dim=-1)
