import pandas as pd
import xlrd

from datetime import date, timedelta, datetime, time

from tempfile import NamedTemporaryFile
import shutil
import csv


def add_familia(archivo):
    print("Leyendo", archivo, "...")
    df = pd.read_excel(archivo, header=0, sheet_name='Hoja1')
    IRF_columns = ['Instrumento', 'Reaj',
                   'Duration', 'Monto', 'Fecha', 'Familia']
    df = df[IRF_columns]
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y-%m-%d")
    df['Fecha'] = df['Fecha'].dt.date

    fserie = pd.read_excel('series.xls', header=0, sheet_name='tbviewDataGrid')

    fields = ['V', 'OpV', 'C', 'OpC', 'Rte', 'Folio', 'Instrumento', 'Liq', 'D', 'Cantidad',
              'Reaj', 'Plazo', 'Duration', 'Precio', 'TIR', 'Monto', 'Hora', 'Fecha', 'Familia']

    print("Agrando columna Familia...")
    df['Familia'] = df['Familia'].astype(str)
    for row in df.itertuples():
        df.at[row.Index, 'Familia'] = fserie[fserie['Serie']
                                             == row.Instrumento]['Familia'].squeeze()

    df.to_excel(archivo, index=False)

    print("Archivo", archivo, "modificado.")
