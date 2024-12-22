# Kala Torch 

Kala Torch Module is a comprehensive PyTorch-based utility module designed to streamline and enhance deep learning workflows. It provides an abstraction over common PyTorch functionalities, making development faster and more intuitive.

## Features

- **Tensor Operations**
  - Supports a wide range of tensor manipulations, including creation, slicing, and memory management.
  - Check tensor types, perform tensor transformations, and handle complex tensors seamlessly.

- **Default Settings Management**
  - Easily set and retrieve default data types and tensor configurations.
  - Configure default tensor types for consistent operations across your codebase.

- **TorchScript Utilities**
  - Simplify scripting and tracing models for deployment in production environments.
  - Enable optimization and execution of models in non-Python setups, like mobile or embedded systems.
  - Save and load scripted modules for reproducibility and deployment.

- **Neural Network (nn) Module Creation**
  - Streamline the creation of common layers like Linear, Convolutional, ReLU, BatchNorm, and Dropout.
  - Build complex architectures, including Transformers, LSTMs, and GRUs, with minimal effort.
  - Define custom activation functions and loss functions to suit your specific needs.

- **Generative Adversarial Networks (GANs)**
  - Easily create and train GANs with pre-defined Generator and Discriminator architectures.
  - Train DCGAN models with minimal code using integrated utility functions.
  - Generate high-quality images and visualize results with built-in sample generation.

- **Multiprocessing Utilities**
  - Facilitate distributed training with tools for parallel processing.
  - Utilize efficient tensor sharing strategies to optimize memory usage in multiprocessing environments.
  - Easily spawn and manage worker processes for model training or data processing.

- **DataLoader Utilities**
  - Seamlessly handle batching, shuffling, and multi-worker setups for datasets.
  - Support for both map-style and iterable-style datasets, with custom collation functions.
  - Enable memory pinning for faster GPU transfers and efficient data loading pipelines.

- **Custom Gradient Functions**
  - Design and implement advanced gradient operations tailored for specific backpropagation needs.
  - Customize both forward and backward passes for unique computational requirements.

- **Advanced Model Deployment**
  - Utilize TorchScript and multiprocessing for efficient deployment in various environments.
  - Enable GPU acceleration and optimize models for inference.

## Installation

Install the module using pip:

```bash
pip install kala-torch
```

## Usage

### Example: Neural Network Creation and Training

```python
import torch
import torch.nn as nn
from Kala_torch.Kala_torch import Kala_torch

# Initialize Kala Torch utility
kala = Kala_torch()

# Define a simple neural network using Kala Torch
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = kala.linear(10, 50)  # Linear layer
        self.relu = kala.relu()         # ReLU activation
        self.fc2 = kala.linear(50, 1)   # Output layer

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Create the model
model = SimpleNN()

# Define loss and optimizer
criterion = kala.cross_entropy_loss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Example input
inputs = torch.randn(32, 10)
targets = torch.randint(0, 2, (32, 1), dtype=torch.float)

# Training step
outputs = model(inputs)
loss = criterion(outputs, targets)
kala.backward(loss)  # Perform backpropagation
optimizer.step()
```

### Example: Generative Adversarial Networks (GANs)

Kala Torch includes an easy-to-use interface for creating and training GANs.

```python
import torch
from torchvision.datasets import CIFAR10
from torchvision.transforms import Compose, ToTensor, Normalize, Resize
from torch.utils.data import DataLoader
from Kala_torch.Kala_torch import Kala_torch

# Initialize Kala Torch utility
kala = Kala_torch()
gan = kala.KalaGAN(latent_dim=100, image_channels=3, image_size=64)

# Define transformation for CIFAR10 dataset
transform = Compose([
    Resize(64),
    ToTensor(),
    Normalize([0.5], [0.5])  # Normalize to [-1, 1]
])

# Load dataset
dataset = CIFAR10(root="./data", train=True, download=True, transform=transform)
data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
gan.generator.to(device)
gan.discriminator.to(device)

# Training loop
num_epochs = 5
for epoch in range(num_epochs):
    for i, (images, _) in enumerate(data_loader):
        images = images.to(device)
        losses = gan.train_step(images, device)  # Pass the `device` argument here

        if i % 100 == 0:
            print(f"Epoch [{epoch + 1}/{num_epochs}], Step [{i + 1}/{len(data_loader)}], "
                  f"D Loss: {losses['d_loss']:.4f}, G Loss: {losses['g_loss']:.4f}")

    # Save generated samples
    gan.generate_samples(num_samples=64, save_path=f"samples_epoch_{epoch + 1}.png", device=device)

```

### Example: DataLoader with Multiprocessing

```python
from torch.utils.data import DataLoader, TensorDataset

# Sample dataset
data = torch.randn(100, 10)
targets = torch.randint(0, 2, (100,))
dataset = TensorDataset(data, targets)

# Create DataLoader
loader = kala.data_loader(dataset, batch_size=16, shuffle=True, num_workers=4)

# Iterate through DataLoader
for batch_idx, (inputs, labels) in enumerate(loader):
    print(f"Batch {batch_idx}: {inputs.shape}, {labels.shape}")
```

### Example: TorchScript for Model Deployment

```python
# Convert model to TorchScript
scripted_model = kala.script(model)

# Save the scripted model
kala.save_script_module(scripted_model, "model_scripted.pt")

# Load the scripted model
loaded_model = kala.load_script_module("model_scripted.pt")

# Perform inference
example_input = torch.randn(1, 10)
output = loaded_model(example_input)
print("Scripted model output:", output)
```

## Contributing

Contributions are welcome! If you encounter issues or have feature requests, please open an issue or submit a pull request on the [GitHub repository](https://github.com/Kalasaikamesh944/Kala-torch).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

