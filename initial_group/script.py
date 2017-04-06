import pandas as pd
import numpy as np

validation = pd.read_csv("validation.csv")

optimalCTR = 0
budget = 25000
np.random.seed(123)

print(validation.shape[0])
print(validation.shape[0]-1)
print(validation.iloc[[validation.shape[0]-1]])
print(validation.iloc[[validation.shape[0]]])
