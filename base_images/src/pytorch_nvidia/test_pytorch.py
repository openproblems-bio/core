import torch
import tempfile

## VIASH START
meta = {
    "temp_dir": tempfile.gettempdir(),
}
## VIASH END

print(f"Using PyTorch version: {torch.__version__}", flush=True)

# Check for GPU (CUDA) availability and set the device for the test
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Found GPU: {torch.cuda.get_device_name(0)}", flush=True)
    print("PyTorch will use the GPU.", flush=True)
else:
    device = torch.device("cpu")
    print("No GPU found. PyTorch will use the CPU.", flush=True)

print("\n--- Running core functionality test ---", flush=True)

# Define tensors for a simple operation on the selected device
w = torch.tensor(5.0, requires_grad=True, device=device)
x = torch.tensor(2.0, device=device)

# Perform a computation
y = w * x

# Use autograd to calculate gradients
y.backward()

actual_gradient = w.grad

# Assert that the gradient is mathematically correct
expected_gradient = x

print(f"Device used: {device}")
print(f"Function: y = w * x")
print(f" -> y = {w.item():.1f} * {x.item():.1f} = {y.item():.1f}")
print(f"Expected gradient (dy/dw): {expected_gradient.item():.1f}")
print(f"Actual gradient (dy/dw):   {actual_gradient.item():.1f}")

assert torch.equal(actual_gradient, expected_gradient)

print("\nPyTorch test passed!", flush=True)
