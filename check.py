import pandas as pd
import numpy as np

x = np.linspace(0.1, 5, 25)
y = 20 * np.exp(-x)

data = pd.DataFrame({'x': x, 'y': y})
data.to_csv('/home/daniel/PycharmProjects/PythonProject6/exp_test.csv', index=False)