import pandas as pd
import xlrd

from datetime import date, timedelta, datetime, time

from tempfile import NamedTemporaryFile
import shutil
import csv


df = pd.read_csv('BDirf.csv', delimiter=',')
IRF_columns = ['Instrumento', 'Reaj', 'Duration', 'Monto', 'Fecha', 'Familia']
df = df[IRF_columns]
df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y-%m-%d")
df['Fecha'] = df['Fecha'].dt.date
#df = df[df['Fecha'] >= date(2020, 1, 1)]
df.to_csv('BDirf_filter.csv', index=False)
fserie = pd.read_excel('series.xls', header=0, sheet_name='tbviewDataGrid')
filename = 'BDirf.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)

fields = ['V', 'OpV', 'C', 'OpC', 'Rte', 'Folio', 'Instrumento', 'Liq', 'D', 'Cantidad',
          'Reaj', 'Plazo', 'Duration', 'Precio', 'TIR', 'Monto', 'Hora', 'Fecha', 'Familia']

i = 0
with open(filename, 'r') as csvfile, tempfile:
    reader = csv.DictReader(csvfile, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields)
    for row in reader:
        if i > 0:
            row['Familia'] = fserie[fserie['Serie'] ==
                                    row['Instrumento']]['Familia'].squeeze()
        writer.writerow(row)
        i = i+1

shutil.move(tempfile.name, filename)
