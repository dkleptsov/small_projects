import torch
import torch.nn as nn
import torch.optim as optim

# Tensors
example_tensor = torch.Tensor([[[1, 2], [3, 4]],
                               [[5, 6], [7, 8]],
                               [[9, 0], [1, 2]]])
new_tensor = example_tensor.to('cuda')
print(example_tensor.device)
print(new_tensor.device)
print(torch.ones_like(example_tensor))
print(torch.zeros_like(example_tensor))
print(torch.rand_like(example_tensor))
print(torch.randn(7, 7, device='cuda'))
print(torch.randn(7, 7).device)
print(torch.randn(7, 7) * torch.randn(7, 7))
print(example_tensor / 2)
print(example_tensor)
print(example_tensor.mean())
print(example_tensor.std())
print(example_tensor.mean(0))
# Equivalently, you could also write:
# example_tensor.mean(dim=0)
# example_tensor.mean(axis=0)
# torch.mean(example_tensor, 0)
# torch.mean(example_tensor, dim=0)
# torch.mean(example_tensor, axis=0)

# Sinle layers
example_input = torch.randn(3, 10)  # Number of examples, number of features

linear = nn.Linear(10, 2) # Create one linear layer
example_output = linear(example_input)
print(f'Output after linear layer: \n{example_output}')

relu = nn.ReLU()  # Create ReLU activation
relu_output = relu(example_output)
print(f'Output after ReLU activation: \n{relu_output}')

batchnorm = nn.BatchNorm1d(2) # Create batch normalization
batchnorm_output = batchnorm(relu_output)
print(f'Output after batch normalization: \n{batchnorm_output}')

# Sequential
mlp_layer = nn.Sequential(nn.Linear(5, 2),
                          nn.BatchNorm1d(2),
                          nn.ReLU())  # Creates single operation

test_example = torch.randn(5,5) + 1
print(f"Input: \n{test_example}")
print(f"Output: \n{mlp_layer(test_example)}")

# Optimization
adam_opt = optim.Adam(mlp_layer.parameters(), lr=1e-1)
adam_opt.zero_grad()
train_example = torch.randn(100,5) + 1

for i in range(12):
    cur_loss = torch.abs(1 - mlp_layer(train_example)).mean()  # Custom loss function
    cur_loss.backward()
    adam_opt.step()
    print(f"Loss at epoch {i+1}: {cur_loss}")

# New nn clases
class ExampleModule(nn.Module):
    def __init__(self, input_dims, output_dims):
        super(ExampleModule, self).__init__()
        self.linear = nn.Linear(input_dims, output_dims)
        self.exponent = nn.Parameter(torch.tensor(1.))

    def forward(self, x):
        x = self.linear(x)

        # This is the notation for element-wise exponentiation, 
        # which matches python in general
        x = x ** self.exponent 
        
        return x

example_model = ExampleModule(10, 2)
print(f"Parameters: \n{list(example_model.parameters())}")
print(f"Named parameters: \n{list(example_model.named_parameters())}")
print(f"Example output: \n{example_model(torch.randn(2,10))}")


