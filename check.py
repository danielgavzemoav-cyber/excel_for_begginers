import numpy as np
import pandas as pd

np.random.seed(42)
n = 100

# normal data - linear relationship
x = np.linspace(0, 10, n)
y = 2 * x + 1 + np.random.normal(0, 0.5, n)

# add 10% anomalies
n_anomalies = int(n * 0.1)
anomaly_idx = np.random.choice(n, n_anomalies, replace=False)
y[anomaly_idx] = y[anomaly_idx] + np.random.uniform(10, 20, n_anomalies)

data = pd.DataFrame({'x': x, 'y': y})
data.to_csv('anomaly_test.csv', index=False)
print(f'Created {n} points with {n_anomalies} anomalies at indices: {anomaly_idx}')