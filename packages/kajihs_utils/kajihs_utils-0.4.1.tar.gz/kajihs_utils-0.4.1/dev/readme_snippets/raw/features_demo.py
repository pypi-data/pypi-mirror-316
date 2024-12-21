from kajihs_utils import batch, get_first
from kajihs_utils.loguru import prompt, setup_logging
from kajihs_utils.numpy_utils import find_closest

# Get first key existing in a dict:
d = {"a": 1, "b": 2, "c": 3}
print(get_first(d, ["x", "a", "b"]))

# Batch a sequence:
seq = list(range(10))
print(list(batch(seq, 3)))

# === Loguru features ===
# Better logged and formatted prompts
prompt("Enter a number")  # snippet: no-exec

# Simply setup well formatted logging in files and console
setup_logging(prefix="app", log_dir="logs")

# === Numpy features ===
import numpy as np

x = np.array([[0, 0], [10, 10], [20, 20]])
print(find_closest(x, [[-1, 2], [15, 12]]))
