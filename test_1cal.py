from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

# Creare un nuovo workbook e selezionare il foglio attivo
wb = Workbook()
ws = wb.active

# Aggiungere i dati alla tabella
data = [
    ["Oscilloscopio", "Multimetro"],
    [4, 8],
    [10, 20],
    [13, 26]
]

for row in data:
    ws.append(row)

# Definire l'intervallo della tabella
tab = Table(displayName="Tabella1", ref="A1:B4")

# Aggiungere uno stile alla tabella
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=True)
tab.tableStyleInfo = style

# Aggiungere la tabella al foglio
ws.add_table(tab)

# Salvare il file
wb.save("test_1cal.xlsx")