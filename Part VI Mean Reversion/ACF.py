import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

# 1. Generate Sample Data (500 data points)
np.random.seed(42)
n = 500
errors = np.random.normal(0, 1, n)

# A. Stationary Process (AR(1) with coefficient 0.5 - strong mean reversion)
stationary = np.zeros(n)
for t in range(1, n):
    stationary[t] = 0.5 * stationary[t-1] + errors[t]

# B. Non-Stationary Process (Random Walk / Unit Root with coefficient 1.0)
random_walk = np.zeros(n)
for t in range(1, n):
    random_walk[t] = 1.0 * random_walk[t-1] + errors[t]

# C. Near-Unit Root Process (Stationary but coefficient is 0.98 - very weak mean reversion)
near_unit_root = np.zeros(n)
for t in range(1, n):
    near_unit_root[t] = 0.98 * near_unit_root[t-1] + errors[t]

# 2. Plot the ACF Charts Side-by-Side
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

plot_acf(stationary, ax=axes[0], lags=40, title="1. Strongly Stationary (AR=0.5)\nFast Exponential Decay")
plot_acf(random_walk, ax=axes[1], lags=40, title="2. Non-Stationary (Random Walk, AR=1.0)\nVery Slow Sample Decay")
plot_acf(near_unit_root, ax=axes[2], lags=40, title="3. Near-Unit Root (Stationary, AR=0.98)\nAlmost Identical to Random Walk")

plt.tight_layout()
plt.show()