import torch

# Example or inference. This model returns a 1-dim tensor multiplied by 2
ts = torch.jit.load('models/doubleit_model.zip')
sample_tensor = torch.tensor([1, 2, 3, 4])
result = ts(sample_tensor)

print(result)  # <- tensor([2, 4, 6, 8])