import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit

# Read data from .xslx file
data = pd.read_excel('/home/chiara/SP_lab3/test_1cal.xlsx')

# Extract x and y data
x = data.iloc[1:4, 0].astype(float)
y = data.iloc[1:4, 1].astype(float)

# Define the function to fit
def linear_func(x, a, b):
    return a * x + b

# Execute the fit
params, covariance = curve_fit(linear_func, x, y)

# Extract fit parameters
a, b = params
errors = np.sqrt(np.diag(covariance))

# Print the results
print(f"Parametro a: {a} ± {errors[0]}")
print(f"Parametro b: {b} ± {errors[1]}")

# Create the plot
plt.scatter(x, y, label='Dati')

# Add the fit line
plt.plot(x, linear_func(x, *params), color='red', label='Retta di calibrazione')

# Add labels and legend
plt.xlabel('Multimetro')
plt.ylabel('Oscilloscopio')
plt.title('Grafico di calibrazione')
plt.legend()

# Show the plot
plt.show()