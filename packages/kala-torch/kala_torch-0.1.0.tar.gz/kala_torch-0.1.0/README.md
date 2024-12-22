# Kala Torch

Kala Torch Module is a comprehensive PyTorch-based utility module designed to simplify and enhance deep learning workflows. It provides utilities for tensor operations, neural network layers, multiprocessing, data handling, and more.

## Features

- Tensor operations
- Default settings management
- TorchScript utilities
- Neural network (nn) module creation
- Multiprocessing utilities
- DataLoader utilities
- Custom gradient functions

## Installation

```bash
pip install kala_torch
```

## Usage

Here are some examples of how to use the `Kala_torch` module.

### Tensor Operations

```python
from Kala_torch.Kala_torch import Kala_torch

kala = Kala_torch()
tensor = kala.tensor([1, 2, 3])
print("Is Tensor:", kala.is_tensor(tensor))
```

### Default Dtype

```python
default_dtype = kala.get_default_dtype()
print("Default dtype:", default_dtype)
```

### DataLoader Example

```python
from torch.utils.data import DataLoader, TensorDataset

data = TensorDataset(kala.arange(10), kala.arange(10))
data_loader = kala.data_loader(data, batch_size=2, shuffle=True)

for batch in data_loader:
    print(batch[0])
```

### TorchScript Example

```python
def example_function(x):
    return x ** 2

scripted_function = kala.script(example_function)
print("TorchScript scripted output:", scripted_function(5))
```

### Neural Network Example

Below is an example of creating and training a neural network using `Kala_torch`:

```python
from Kala_torch.Kala_torch import Kala_torch
import torch
import torch.nn as nn

def main():
    # Initialize the Kala_torch utility
    kala = Kala_torch()

    # Define a simple neural network
    class SimpleNN(nn.Module):
        def __init__(self):
            super(SimpleNN, self).__init__()
            # Using Kala_torch to create layers
            self.fc1 = kala.linear(in_features=4, out_features=128)
            self.relu = kala.relu()  # Activation function
            self.fc2 = kala.linear(in_features=128, out_features=3)
        
        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x

    # Create the model, loss function, and optimizer
    model = SimpleNN()
    criterion = kala.cross_entropy_loss()  # Loss function
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)  # Optimizer

    # Example dataset: Randomly generated data (replace with real data)
    inputs = torch.rand(10, 4)  # 10 samples, each with 4 features
    targets = torch.randint(0, 3, (10,))  # Random labels for 3 classes

    # Training loop
    for epoch in range(20):  # Number of epochs
        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # Backward pass
        optimizer.zero_grad()  # Clear gradients
        kala.backward(loss)  # Compute gradients
        optimizer.step()  # Update weights

        # Print epoch information
        print(f"Epoch [{epoch + 1}/20], Loss: {loss.item():.4f}")

    # Test the model with an example input
    test_input = torch.rand(1, 4)  # Single test sample
    predicted = model(test_input)
    print(f"Test input: {test_input}")
    print(f"Predicted output: {predicted}")

if __name__ == "__main__":
    main()
```

### Multiprocessing Example

```python
def train_process(rank):
    print(f"Training on process {rank}")

kala.spawn_processes(train_process, nprocs=2)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- [PyTorch](https://pytorch.org/)
- The open-source community

