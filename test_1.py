import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Read data from .xlsx files
data1 = pd.read_excel('/home/chiara/SP_lab3/test_1cal.xlsx')
data2 = pd.read_excel('/home/chiara/SP_lab3/test_1exp.xlsx')

# Extract x and y data
x1 = data1.iloc[1:4, 0].astype(float)
y1 = data1.iloc[1:4, 1].astype(float)
errx1 = data1.iloc[1:4, 2].astype(float)
erry1 = data1.iloc[1:4, 3].astype(float)

x2 = data2.iloc[1:4, 0].astype(float)
y2 = data2.iloc[1:4, 1].astype(float)
errx2 = data2.iloc[1:4, 2].astype(float)
erry2 = data2.iloc[1:4, 3].astype(float)

# Define functions to fit
def linear_func(x, a, b):
    return a * x + b

def exponential_func(x, c, d):
    return c * np.exp(d * x)

# Perform the linear fit
params1, covariance1 = curve_fit(linear_func, x1, y1, sigma=erry1, absolute_sigma=True)

# Perform the exponential fit
params2, covariance2 = curve_fit(exponential_func, x2, y2, sigma=erry2, absolute_sigma=True, p0=(1, 0.1))

# Extract fit parameters
a, b = params1
errors1 = np.sqrt(np.diag(covariance1))

c, d = params2
errors2 = np.sqrt(np.diag(covariance2))

# Check for infinite errors
if np.any(np.isinf(errors1)):
    print("Warning: Infinite errors in linear fit parameters")
if np.any(np.isinf(errors2)):
    print("Warning: Infinite errors in exponential fit parameters")

# Print the results
print(f"Linear fit parameter a: {a} ± {errors1[0]}")
print(f"Linear fit parameter b: {b} ± {errors1[1]}")
print(f"Exponential fit parameter c: {c} ± {errors2[0]}")
print(f"Exponential fit parameter d: {d} ± {errors2[1]}")

# Create the plot for the linear fit
fig1, ax1 = plt.subplots()
ax1.errorbar(x1, y1, xerr=errx1, yerr=erry1, fmt='o', label='Dati')
ax1.plot(x1, linear_func(x1, *params1), color='red', label='Retta di calibrazione')
ax1.set_xlabel('Multimetro')
ax1.set_ylabel('Oscilloscopio')
ax1.set_title('Retta di calibrazione')
ax1.legend()

# Save the linear fit plot as a PNG file
fig1.savefig('Calibration.png')

# Create the plot for the exponential fit
fig2, ax2 = plt.subplots()
ax2.errorbar(x2, y2, xerr=errx2, yerr=erry2, fmt='o', label='Dati')
ax2.plot(x2, exponential_func(x2, *params2), color='red', label='Caratteristica I-V')
ax2.set_xlabel('Multimetro')
ax2.set_ylabel('Oscilloscopio')
ax2.set_title('Caratteristica I-V')
ax2.legend()

# Save the exponential fit plot as a PNG file
fig2.savefig('I-V.png')

# Show the plots
plt.show()