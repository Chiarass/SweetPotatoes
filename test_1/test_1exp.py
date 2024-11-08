from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create a new workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Add data for the table
data = [
    ["Tensione", "Corrente", "Errore tensione", "Errore corrente"],
    [0, 1, 0.1, 0.1],
    [0.5, np.e**0.5, 0.1, 0.1],
    [1, np.e, 0.1, 0.1],
    [2, np.e**2, 0.1, 0.1],
    [3, np.e**3, 0.1, 0.1]
]

for row in data:
    ws.append(row)

# Define the range for the table
tab = Table(displayName="Tabella1", ref="A1:D6")

# Add a style to the table
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=True)
tab.tableStyleInfo = style

# Add the table to the sheet
ws.add_table(tab)

# Save the workbook
wb.save('/home/chiara/SP_lab3/test_1/test_1exp.xlsx')

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Create a figure and a table
fig, ax = plt.subplots(figsize=(8, 4))  # set size frame
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Save the table as a PNG file
plt.savefig('/home/chiara/SP_lab3/test_1/png/I-V_tab.png')

# Show the plot (optional)
# plt.show()