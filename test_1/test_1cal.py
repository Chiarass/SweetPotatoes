from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Creare un nuovo workbook e selezionare il foglio attivo
wb = Workbook()
ws = wb.active

# Aggiungere i dati alla tabella
data = [
    ["Oscilloscopio", "Multimetro", "Errore oscilloscopio", "Errore multimetro"],
    [0.1, 0.0983, 0.001, 0.001],
    [0.22, 0.2167, 0.001, 0.001],
    [0.32, 0.3105, 0.001, 0.001],
    [0.4, 0.389, 0.001, 0.001],
    [0.5, 0.487, 0.001, 0.001],
    [0.6, 0.589, 0.001, 0.001],
    [0.7, 0.678, 0.001, 0.001],
    [0.8, 0.777, 0.001, 0.001]
]

for row in data:
    ws.append(row)

# Definire l'intervallo della tabella
tab = Table(displayName="Tabella1", ref="A1:D5")

# Aggiungere uno stile alla tabella
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=True)
tab.tableStyleInfo = style

# Aggiungere la tabella al foglio
ws.add_table(tab)

# Salvare il file
wb.save('/home/chiara/SP_lab3/test_1/test_1cal.xlsx')

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Create a figure and a table
fig, ax = plt.subplots(figsize=(8, 4))  # set size frame
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Save the table as a PNG file
plt.savefig('/home/chiara/SP_lab3/test_1/png/Calibration_tab.png')

# Show the plot (optional)
# plt.show()