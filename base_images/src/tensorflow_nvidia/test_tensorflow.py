import tensorflow as tf
import numpy as np
import tempfile
import os

# Suppress TensorFlow informational messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

## VIASH START
meta = {
    "temp_dir": tempfile.gettempdir(),
}
## VIASH END

print(f"Using TensorFlow version: {tf.__version__}", flush=True)

# Check for and list available physical devices (CPU/GPU)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"Found {len(gpus)} GPU(s):", flush=True)
    for gpu in gpus:
        print(f"  - {gpu}", flush=True)
else:
    print("No GPU found. TensorFlow will use the CPU.", flush=True)

print("\n--- Running core functionality test ---", flush=True)

# Define a variable and a constant for a simple operation
w = tf.Variable(5.0, name="weight")
x = tf.constant(2.0, name="input")

# Perform a computation within a GradientTape context
with tf.GradientTape() as tape:
  y = w * x

# Calculate the gradient of y with respect to w
grad = tape.gradient(y, w)

# Assert that the gradient is mathematically correct
expected_gradient = x.numpy()
actual_gradient = grad.numpy()

print(f"Function: y = w * x")
print(f" -> y = {w.numpy()} * {x.numpy()} = {y.numpy()}")
print(f"Expected gradient (dy/dw): {expected_gradient}")
print(f"Actual gradient (dy/dw):   {actual_gradient}")

assert np.isclose(actual_gradient, expected_gradient)

print("\nTensorFlow test passed!", flush=True)
