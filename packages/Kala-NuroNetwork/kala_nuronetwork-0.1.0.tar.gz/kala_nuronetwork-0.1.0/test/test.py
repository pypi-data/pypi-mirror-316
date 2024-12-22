from KalaNeroNetwork import KalaNuroNetwork, KalaNuroTrainer
import torch
import torch.nn as nn
import torch.optim as optim

# Define hyperparameters
input_size = 2
n_qubits = 2
hidden_size = 128
output_size = 2
batch_size = 128
epochs = 10

# Generate synthetic dataset
def generate_large_data(num_samples, input_size):
    data = torch.rand(num_samples, input_size)
    labels = (data.sum(axis=1) > 1.0).long()  # Binary classification based on sum threshold
    return data, labels

num_samples = 10000
data, labels = generate_large_data(num_samples, input_size)
dataset = torch.utils.data.TensorDataset(data, labels)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Initialize model, optimizer, and criterion
model = KalaNuroNetwork(input_size, n_qubits, hidden_size, output_size)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Train and evaluate
trainer = KalaNuroTrainer(model, optimizer, criterion, device="cpu")

print("Starting training...")
trainer.train(data_loader, epochs)

print("Evaluating model...")
trainer.evaluate(data_loader)