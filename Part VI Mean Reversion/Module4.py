import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
import numpy as np

def simulate_acf_illusion():
    """
    Demonstrates why visual ACF plots fail to distinguish 
    between unit root and highly autoregressive stationary processes.
    """
    np.random.seed(42)
    n = 500
    errors = np.random.normal(0, 1, n)
    
    stationary_strong = np.zeros(n)
    stationary_weak = np.zeros(n)
    random_walk = np.zeros(n)
    
    for t in range(1, n):
        stationary_strong[t] = 0.5 * stationary_strong[t-1] + errors[t]
        stationary_weak[t] = 0.98 * stationary_weak[t-1] + errors[t]
        random_walk[t] = 1.0 * random_walk[t-1] + errors[t]
        
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    plot_acf(stationary_strong, ax=axes[0], lags=40, title="Strong Stationary")
    plot_acf(random_walk, ax=axes[1], lags=40, title="Random Walk")
    plot_acf(stationary_weak, ax=axes[2], lags=40, title="Weak Stationary")
    plt.show()

simulate_acf_illusion