import Kala_Quantum as kq
import torch
from Kala_torch.Kala_torch import Kala_torch
import torch.nn as nn
import time

class QuantumLayer(nn.Module):
    def __init__(self, n_qubits):
        super(QuantumLayer, self).__init__()
        self.n_qubits = n_qubits
        self.circuit = kq.QuantumState(n_qubits)

    def forward(self, x):
        batch_size = x.shape[0]
        outputs = []

        for _ in range(batch_size):
            # Reset the circuit for each input
            self.circuit = kq.QuantumState(self.n_qubits)

            # Apply quantum gates (can be customized)
            for qubit in range(self.n_qubits):
                self.circuit.apply_gate(kq.hadamard(), qubit)
            self.circuit.apply_gate(kq.cnot(), qubit=[0, 1])

            # Simulate measurement
            measured_output = self.circuit.measure()

            # Convert measurement result to numerical format
            if isinstance(measured_output, str):
                output_as_array = [int(bit) for bit in measured_output.strip('|>')]
            else:
                output_as_array = [int(bit) for bit in bin(measured_output)[2:].zfill(self.n_qubits)]
            outputs.append(output_as_array)

        # Return batch of outputs
        return torch.tensor(outputs, dtype=torch.float32)

class KalaNuroNetwork(nn.Module):
    def __init__(self, input_size, n_qubits, hidden_size, output_size):
        super(KalaNuroNetwork, self).__init__()
        self.quantum_layer = QuantumLayer(n_qubits)
        self.fc1 = Kala_torch().linear(n_qubits, hidden_size)
        self.fc2 = Kala_torch().linear(hidden_size, output_size)

    def forward(self, x):
        # Quantum processing
        x_quantum = self.quantum_layer(x)

        # Process each quantum output into classical values
        x_classical = torch.stack([torch.tensor([abs(v) ** 2 for v in sample], dtype=torch.float32) for sample in x_quantum])

        # Classical processing
        x_classical = torch.relu(self.fc1(x_classical))
        return torch.softmax(self.fc2(x_classical), dim=1)

class KalaNuroTrainer:
    def __init__(self, model, optimizer, criterion, device="cpu"):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device

    def train(self, data_loader, epochs):
        self.model.train()
        for epoch in range(epochs):
            epoch_loss = 0
            for batch_data, batch_labels in data_loader:
                batch_data = batch_data.to(self.device)
                batch_labels = batch_labels.to(self.device)

                # Forward pass
                outputs = self.model(batch_data)
                loss = self.criterion(outputs, batch_labels)

                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item()

            print(f"Epoch {epoch + 1}, Loss: {epoch_loss / len(data_loader)}")

    def evaluate(self, data_loader):
        self.model.eval()
        total, correct = 0, 0
        with torch.no_grad():
            for batch_data, batch_labels in data_loader:
                batch_data = batch_data.to(self.device)
                batch_labels = batch_labels.to(self.device)

                outputs = self.model(batch_data)
                _, predicted = torch.max(outputs, 1)
                total += batch_labels.size(0)
                correct += (predicted == batch_labels).sum().item()

        accuracy = 100 * correct / total
        print(f"Accuracy: {accuracy:.2f}%")
        return accuracy

# Utility to generate large datasets
def generate_large_data(num_samples, input_size):
    data = torch.rand(num_samples, input_size)
    labels = (data.sum(axis=1) > 1.0).long()  # Sum threshold for binary classification
    return data, labels
