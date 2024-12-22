import torch.multiprocessing as mp
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.utils import make_grid, save_image
from  tqdm import tqdm

class Kala_torch:
    def __init__(self):
        pass

    # Tensor operations
    def is_tensor(self, tensor):
        # Check if the given object is a tensor
        return torch.is_tensor(tensor)

    def is_storage(self, obj):
        # Check if the given object is a storage object
        return torch.is_storage(obj)

    def is_memory_format(self, memory_format):
        # Check if the input is a valid memory format
        return isinstance(memory_format, torch.memory_format)

    def is_floating_point_tensor(self, tensor):
        # Check if the tensor is of floating point type
        return torch.is_floating_point(tensor)

    def is_complex(self, input_complex):
        # Check if the input is a complex tensor
        return torch.is_complex(input_complex)

    def is_conj(self, input_conj):
        # Compute the conjugate of the input tensor
        return torch.conj(input_conj)

    def is_nonzero(self, input_tensor):
        # Check if the input tensor has a nonzero value
        return torch.is_nonzero(input_tensor)

    def clone(self, tensor):
        # Clone a tensor
        return tensor.clone()

    def cat(self, tensors, dim=0):
        # Concatenate a sequence of tensors along a specified dimension
        return torch.cat(tensors, dim)

    def stack(self, tensors, dim=0):
        # Stack tensors along a new dimension
        return torch.stack(tensors, dim)

    # Default settings
    def set_default_dtype(self, input_dtype):
        # Set the default data type for tensors
        torch.set_default_dtype(input_dtype)

    def get_default_dtype(self):
        # Get the current default data type for tensors
        return torch.get_default_dtype()

    def set_default_tensor_type(self, tensor_type):
        # Set the default tensor type
        torch.set_default_tensor_type(tensor_type)

    # Tensor creation
    def tensor(self, tensor):
        # Create a tensor with the default data type
        return torch.tensor(tensor, dtype=torch.get_default_dtype())

    def zeros(self, *size, dtype=None, requires_grad=False):
        # Create a tensor filled with zeros
        return torch.zeros(*size, dtype=dtype, requires_grad=requires_grad)

    def ones(self, *size, dtype=None, requires_grad=False):
        # Create a tensor filled with ones
        return torch.ones(*size, dtype=dtype, requires_grad=requires_grad)

    def arange(self, start, end, step=1, dtype=None):
        # Create a 1D tensor with values from start to end with a given step
        return torch.arange(start, end, step, dtype=dtype)

    # Print options
    def set_printoptions(self, threshold=None, linewidth=None):
        # Configure print options for tensors
        torch.set_printoptions(threshold=threshold, linewidth=linewidth)

    # Autograd operations
    def backward(self, tensor, gradient=None, retain_graph=None, create_graph=False):
        # Perform backpropagation on the tensor
        tensor.backward(gradient=gradient, retain_graph=retain_graph, create_graph=create_graph)

    def grad(self, outputs, inputs, grad_outputs=None, retain_graph=None, create_graph=False, allow_unused=False):
        # Compute gradients of outputs with respect to inputs
        return torch.autograd.grad(outputs, inputs, grad_outputs=grad_outputs, retain_graph=retain_graph, create_graph=create_graph, allow_unused=allow_unused)

    def no_grad(self):
        # Context manager to disable gradient calculations
        return torch.no_grad()

    def enable_grad(self):
        # Context manager to enable gradient calculations
        return torch.enable_grad()

    # TorchScript utilities
    def script(self, func):
        # Convert a function to TorchScript using scripting
        return torch.jit.script(func)

    def trace(self, func, example_inputs):
        # Convert a function to TorchScript using tracing
        return torch.jit.trace(func, example_inputs)

    def save_script_module(self, module, path):
        # Save a TorchScript module to the specified path
        module.save(path)

    def load_script_module(self, path):
        # Load a TorchScript module from the specified path
        return torch.jit.load(path)

    # nn Modules
    def linear(self, in_features, out_features, bias=True):
        # Create a linear layer
        return nn.Linear(in_features, out_features, bias=bias)

    def conv2d(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        # Create a 2D convolutional layer
        return nn.Conv2d(in_channels, out_channels, kernel_size, stride=stride, padding=padding)

    def relu(self,input_):
        # Create a ReLU activation function
        return nn.ReLU(input_)

    def softmax(self, dim=None):
        # Create a softmax activation function
        return nn.Softmax(dim=dim)

    def gelu(self):
        # Create a GELU activation function
        return nn.GELU()

    def dropout(self, p=0.5):
        # Create a Dropout layer
        return nn.Dropout(p=p)

    def batch_norm(self, num_features):
        # Create a 1D batch normalization layer
        return nn.BatchNorm1d(num_features)

    def lstm(self, input_size, hidden_size, num_layers=1, bias=True, batch_first=False, dropout=0, bidirectional=False):
        # Create an LSTM layer
        return nn.LSTM(input_size, hidden_size, num_layers=num_layers, bias=bias, batch_first=batch_first, dropout=dropout, bidirectional=bidirectional)

    def transformer(self, d_model, nhead, num_encoder_layers=6, num_decoder_layers=6, dim_feedforward=2048, dropout=0.1):
        # Create a Transformer model
        return nn.Transformer(d_model=d_model, nhead=nhead, num_encoder_layers=num_encoder_layers, num_decoder_layers=num_decoder_layers, dim_feedforward=dim_feedforward, dropout=dropout)

    def cross_entropy_loss(self):
        # Create a cross-entropy loss function
        return nn.CrossEntropyLoss()

    def mse_loss(self):
        # Create a mean squared error loss function
        return nn.MSELoss()

    def real(self,quantum_data):
        # Convert complex amplitudes to probabilities
        return torch.tensor([abs(v) ** 2 for v in quantum_data], dtype=torch.float32)

    # Multiprocessing utilities
    def get_all_sharing_strategies(self):
        # Get all available sharing strategies for tensors
        return mp.get_all_sharing_strategies()

    def get_sharing_strategy(self):
        # Get the current sharing strategy for tensors
        return mp.get_sharing_strategy()

    def set_sharing_strategy(self, strategy):
        # Set the sharing strategy for tensors
        mp.set_sharing_strategy(strategy)

    def spawn_processes(self, fn, args=(), nprocs=1, join=True, daemon=False):
        # Spawn multiple processes to execute a function
        return mp.spawn(fn, args=args, nprocs=nprocs, join=join, daemon=daemon)

    def share_memory(self, tensor):
        # Move a tensor to shared memory
        tensor.share_memory_()

    # Data utilities
    def data_loader(self, dataset, batch_size=1, shuffle=False, num_workers=0, pin_memory=False):
        # Create a DataLoader for a dataset
        return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers, pin_memory=pin_memory)

    def random_split(self, dataset, lengths):
        # Randomly split a dataset into multiple subsets
        return torch.utils.data.random_split(dataset, lengths)

    def sequential_sampler(self, dataset):
        # Create a sequential sampler for a dataset
        return torch.utils.data.SequentialSampler(dataset)

    def random_sampler(self, dataset, replacement=False, num_samples=None):
        # Create a random sampler for a dataset
        return torch.utils.data.RandomSampler(dataset, replacement=replacement, num_samples=num_samples)

    class CustomFunction(torch.autograd.Function):
        @staticmethod
        def forward(ctx, *args):
            # Define the forward pass for the custom function
            raise NotImplementedError("Forward method must be implemented.")

        @staticmethod
        def backward(ctx, *grad_outputs):
            # Define the backward pass for the custom function
            raise NotImplementedError("Backward method must be implemented.")

    import os
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torchvision import datasets, transforms
    from torchvision.utils import save_image, make_grid
    from tqdm import tqdm

    class KalaGAN:
        def __init__(self, latent_dim=100, image_channels=3, image_size=64, lr=0.0002, beta1=0.5, beta2=0.999):
            """
            KalaGAN class encapsulates the Generator and Discriminator for training GANs.
            Args:
                latent_dim (int): Size of the latent vector (z).
                image_channels (int): Number of channels in the images (e.g., 3 for RGB).
                image_size (int): Size of the images (e.g., 64x64).
                lr (float): Learning rate for Adam optimizer.
                beta1 (float): Beta1 for Adam optimizer.
                beta2 (float): Beta2 for Adam optimizer.
            """
            self.latent_dim = latent_dim
            self.image_channels = image_channels
            self.image_size = image_size

            # Initialize Generator and Discriminator
            self.generator = self.build_generator()
            self.discriminator = self.build_discriminator()

            # Loss and optimizers
            self.criterion = nn.BCELoss()
            self.optimizer_g = optim.Adam(self.generator.parameters(), lr=lr, betas=(beta1, beta2))
            self.optimizer_d = optim.Adam(self.discriminator.parameters(), lr=lr, betas=(beta1, beta2))

        def build_generator(self):
            """Builds the generator network."""
            return nn.Sequential(
                nn.ConvTranspose2d(100, 512, 4, 1, 0, bias=False),
                nn.BatchNorm2d(512),
                nn.ReLU(True),

                nn.ConvTranspose2d(512, 256, 4, 2, 1, bias=False),
                nn.BatchNorm2d(256),
                nn.ReLU(True),

                nn.ConvTranspose2d(256, 128, 4, 2, 1, bias=False),
                nn.BatchNorm2d(128),
                nn.ReLU(True),

                nn.ConvTranspose2d(128, 64, 4, 2, 1, bias=False),
                nn.BatchNorm2d(64),
                nn.ReLU(True),

                nn.ConvTranspose2d(64, 3, 4, 2, 1, bias=False),
                nn.Tanh()
            )

        def build_discriminator(self):
            """Builds the discriminator network."""
            return nn.Sequential(
                nn.Conv2d(3, 64, 4, 2, 1, bias=False),
                nn.LeakyReLU(0.2, inplace=True),

                nn.Conv2d(64, 128, 4, 2, 1, bias=False),
                nn.BatchNorm2d(128),
                nn.LeakyReLU(0.2, inplace=True),

                nn.Conv2d(128, 256, 4, 2, 1, bias=False),
                nn.BatchNorm2d(256),
                nn.LeakyReLU(0.2, inplace=True),

                nn.Conv2d(256, 512, 4, 2, 1, bias=False),
                nn.BatchNorm2d(512),
                nn.LeakyReLU(0.2, inplace=True),

                nn.Conv2d(512, 1, 4, 1, 0, bias=False),
                nn.Sigmoid()
            )

        def train_step(self, real_images, device):
            """Performs a single training step."""
            batch_size = real_images.size(0)
            real_images = real_images.to(device)

            # Real and fake labels
            real_labels = torch.ones(batch_size, device=device)
            fake_labels = torch.zeros(batch_size, device=device)

            # ---------------------
            # Train Discriminator
            # ---------------------
            self.discriminator.zero_grad()
            real_output = self.discriminator(real_images).view(-1)
            real_loss = self.criterion(real_output, real_labels)

            noise = torch.randn(batch_size, self.latent_dim, 1, 1, device=device)
            fake_images = self.generator(noise)
            fake_output = self.discriminator(fake_images.detach()).view(-1)
            fake_loss = self.criterion(fake_output, fake_labels)

            d_loss = real_loss + fake_loss
            d_loss.backward()
            self.optimizer_d.step()

            # -----------------
            # Train Generator
            # -----------------
            self.generator.zero_grad()
            fake_output = self.discriminator(fake_images).view(-1)
            g_loss = self.criterion(fake_output, real_labels)
            g_loss.backward()
            self.optimizer_g.step()

            return {"d_loss": d_loss.item(), "g_loss": g_loss.item()}

        def generate_samples(self, num_samples, save_path=None, device=torch.device("cpu")):
            """Generates and saves sample images."""
            noise = torch.randn(num_samples, self.latent_dim, 1, 1, device=device)
            with torch.no_grad():
                fake_images = self.generator(noise).cpu()
            grid = make_grid(fake_images, normalize=True, nrow=8)
            if save_path:
                save_image(grid, save_path)
            return grid
