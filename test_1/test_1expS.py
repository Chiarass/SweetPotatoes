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
    [0.42, 27*10**-3, 0.03, 0.003],
    [0.44, 39*10**-3, 0.03, 0.003],
    [0.46, 61*10**-3, 0.03, 0.003],
    [0.48, 92*10**-3, 0.01, 0.003],
    [0.50, 134*10**-3, 0.03, 0.004],
    [0.52, 214*10**-3, 0.01, 0.004],
    [0.54, 315*10**-3, 0.03, 0.005],
    [0.56, 491*10**-3, 0.03, 0.007],
    [0.58, 743*10**-3, 0.03, 0.008],
    [0.60, 1136*10**-3, 0.03, 0.011],
    [0.62, 1733*10**-3, 0.03, 0.015],
    [0.64, 2400*10**-3, 0.03, 0.019]
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
wb.save('/home/chiara/SP_lab3/test_1/xslx/test_1expS.xlsx')

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Create a figure and a table
fig, ax = plt.subplots(figsize=(8, 4))  # set size frame
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Save the table as a PNG file
plt.savefig('/home/chiara/SP_lab3/test_1/png/I-V_tabS.png')

# Save the data to a text file
with open('/home/chiara/SP_lab3/test_1/txt/test_1expS.txt', 'w') as f:
    f.write('\t'.join(data[0]) + '\n')
    for row in data[1:]:
        f.write('\t'.join(map(str, row)) + '\n')

# Show the plot (optional)
# plt.show()