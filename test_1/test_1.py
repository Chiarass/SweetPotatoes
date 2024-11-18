import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Read data from .xlsx files
data1 = pd.read_excel('/home/chiara/SP_lab3/test_1/test_1cal.xlsx')
data2 = pd.read_excel('/home/chiara/SP_lab3/test_1/test_1expG.xlsx')
data3 = pd.read_excel('/home/chiara/SP_lab3/test_1/test_1expS.xlsx')

# Extract x and y data
x1 = data1.iloc[0:9, 0].astype(float)
y1 = data1.iloc[0:9, 1].astype(float)
errx1 = data1.iloc[0:9, 2].astype(float)
erry1 = data1.iloc[0:9, 3].astype(float)

x2 = data2.iloc[0:13, 0].astype(float)
y2 = data2.iloc[0:13, 1].astype(float)
errx2 = data2.iloc[0:13, 2].astype(float)
erry2 = data2.iloc[0:13, 3].astype(float)

x3 = data3.iloc[0:13, 0].astype(float)
y3 = data3.iloc[0:13, 1].astype(float)
errx3 = data3.iloc[0:13, 2].astype(float)
erry3 = data3.iloc[0:13, 3].astype(float)

# Define functions to fit
def linear_func(x, a, b):
    return a * x + b

def exponential_func(x, c, d):
    return c * np.exp(x/d)

# Perform the linear fit
params1, covariance1 = curve_fit(linear_func, x1, y1, sigma=erry1, absolute_sigma=True)

# Perform the exponential fit
params2, covariance2 = curve_fit(exponential_func, x2, y2, sigma=erry2, absolute_sigma=True, p0=(1, 0.1))

# Perform the exponential fit
params3, covariance3 = curve_fit(exponential_func, x3, y3, sigma=erry3, absolute_sigma=True, p0=(1, 0.1))

# Extract fit parameters
a, b = params1
errors1 = np.sqrt(np.diag(covariance1))

c, d = params2
errors2 = np.sqrt(np.diag(covariance2))

e, f = params3
errors3 = np.sqrt(np.diag(covariance3))

# Check for infinite errors
if np.any(np.isinf(errors1)):
    print("Warning: Infinite errors in linear fit parameters")
if np.any(np.isinf(errors2)):
    print("Warning: Infinite errors in exponential fit parameters")
if np.any(np.isinf(errors3)):
    print("Warning: Infinite errors in exponential fit parameters")

# Print the results
print(f"Linear fit parameter a: {a} ± {errors1[0]}")
print(f"Linear fit parameter b: {b} ± {errors1[1]}")
print(f"Exponential fit parameter Germanium c: {c} ± {errors2[0]}")
print(f"Exponential fit parameter Germanium d: {d} ± {errors2[1]}")
print(f"Exponential fit parameter Silicium e: {c} ± {errors3[0]}")
print(f"Exponential fit parameter Silicium f: {d} ± {errors3[1]}")

# Create the plot for the linear fit
fig1, ax1 = plt.subplots()
ax1.errorbar(x1, y1, xerr=errx1, yerr=erry1, fmt='o', label='Dati')
ax1.plot(x1, linear_func(x1, *params1), color='red', label='Retta di calibrazione')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_xlabel('Multimetro')
ax1.set_ylabel('Oscilloscopio')
ax1.set_title('Retta di calibrazione')
ax1.legend()

# Save the linear fit plot as a PNG file
fig1.savefig('/home/chiara/SP_lab3/test_1/png/Calibration.png')

# Create the plot for the exponential fit (Germanium)
fig2, ax2 = plt.subplots()
ax2.errorbar(x2, y2, xerr=errx2, yerr=erry2, fmt='o', label='Dati')
ax2.plot(x2, exponential_func(x2, *params2), color='red', label='Caratteristica I-V')
ax2.set_xlabel('Tensione (V)')
ax2.set_ylabel('Corrente (mA)')
ax2.set_yscale('log')
ax2.set_title('Caratteristica I-V del diodo al Germanio')
ax2.legend()

# Save the exponential fit plot as a PNG file (Germanium)
fig2.savefig('/home/chiara/SP_lab3/test_1/png/I-V_curveG.png')

# Create the plot for the exponential fit (Silicium)
fig3, ax3 = plt.subplots()
ax3.errorbar(x3, y3, xerr=errx3, yerr=erry3, fmt='o', label='Dati')
ax3.plot(x3, exponential_func(x3, *params3), color='red', label='Caratteristica I-V')
ax3.set_xlabel('Tensione (V)')
ax3.set_ylabel('Corrente (mA)')
ax3.set_yscale('log')
ax3.set_title('Caratteristica I-V del diodo al Silicio')
ax3.legend()

# Save the exponential fit plot as a PNG file (Silicium)
fig3.savefig('/home/chiara/SP_lab3/test_1/png/I-V_curveS.png')

# Show the plots
plt.show()