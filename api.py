import pandas as pd
import numpy as np

from datetime import date, timedelta, datetime, time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from pandas.tseries.offsets import BDay


# Conexión base de datos
# <>dependencia con psycopg2
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Column, String, DateTime, Integer, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# conectarse a la base de datos
# cambiar esto por un log in con input de usuario

# engine://user:password@host:5432/database

database = create_engine(
    'postgres://ywbhjstvlwwguj:4169cd9bb75716133a084e53deb4481699ec6cdc5c2d253af098ffb00fc77457@ec2-18-211-48-247.compute-1.amazonaws.com:5432/dc69t4t9dl57ao')
base = declarative_base()

# ORM entidades de la bd


class IRF(base):
    __tablename__ = 'irf'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Instrumento = Column(String)
    Reaj = Column(String)
    Duration = Column(Float)
    Monto = Column(Float)
    Fecha = Column(DateTime)
    Familia = Column(String)


class IIF(base):
    __tablename__ = 'iif'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Rescate = Column(Float)
    Moneda = Column(String)
    Tasa = Column(Float)
    Captacion = Column(Float)
    TipoEmisor = Column(String)
    Fecha = Column(DateTime)


class USDCLP(base):
    __tablename__ = 'usdclp'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Precio = Column(Float)


# create session
Session = sessionmaker(database)
session = Session()

base.metadata.create_all(database)
# se va a quejar si lo corres más de una vez^


# OPERCIONES QUE MODIFICAN LA BD

# delete rows by date
def delete_by_date(table, fecha):
    # estos son mensuales
    if table == 'IRF':
        input_rows = session.query(IRF).filter(IRF.Fecha == fecha).delete()
    elif table == 'IIF':
        input_rows = session.query(IIF).filter(IIF.Fecha == fecha).delete()

    session.commit()

# UPLOAD DATA


def upload_to_sql_iif():
    ##### IIF #####
    print("Preparando data IIF...")
    df_iif = pd.read_excel('iif.xls', header=0, sheet_name='tradesTable')
    IIF_columns = ['Rescate', 'Moneda',
                   'Tasa', 'Captación', 'Tipo Emisor', 'Fecha']
    df_iif = df_iif[IIF_columns]
    df_iif.columns = ['Rescate', 'Moneda',
                      'Tasa', 'Captacion', 'TipoEmisor', 'Fecha']
    df_iif['Fecha'] = pd.to_datetime(df_iif['Fecha'], format="%Y-%m-%d")
    df_iif['Fecha'] = df_iif['Fecha'].dt.date

    #df = df[(df['Fecha'] > date(2020, 2, 28))]

    start_date = min(df_iif['Fecha'])
    end_date = max(df_iif['Fecha'])

    dates = list(rrule(DAILY, dtstart=start_date, until=end_date))
    print("Empezando upload...")
    for i in range(len(dates)):
        df_i = df_iif[df_iif['Fecha'] == dates[i].date()]
        if not df_i.empty:
            delete_by_date('IIF', dates[i])
            df_i.to_sql("iif",
                        database,
                        if_exists='append',
                        schema='public',
                        index=False,
                        chunksize=500,
                        dtype={
                            "Rescate": Float,
                            "Moneda": String,
                            "Tasa": Float,
                            "Captacion": Float,
                            "TipoEmisor": String,
                            "Fecha": DateTime}
                        )
            session.commit()
            print("Data subida hasta", dates[i])
        else:
            print("No data reportada en:", dates[i])


def upload_to_sql_irf(archivo):  # start_date,end_date = None):
    ##### IRF #####
    print("Preparando data IRF...")
    df_irf = pd.read_csv(archivo, delimiter=',')
    IRF_columns = ['Instrumento', 'Reaj',
                   'Duration', 'Monto', 'Fecha', 'Familia']
    df_irf = df_irf[IRF_columns]
    df_irf['Fecha'] = pd.to_datetime(df_irf['Fecha'], format="%Y-%m-%d")
    df_irf['Fecha'] = df_irf['Fecha'].dt.date

    #df = df[(df['Fecha'] > date(2020, 2, 28))]

    start_date = min(df_irf['Fecha'])
    end_date = max(df_irf['Fecha'])

    dates = list(rrule(DAILY, dtstart=start_date, until=end_date))
    print("Empezando upload...")
    for i in range(len(dates)):
        df_i = df_irf[df_irf['Fecha'] == dates[i].date()]
        if not df_i.empty:
            delete_by_date('IRF', dates[i])
            df_i.to_sql("irf",
                        database,
                        if_exists='append',
                        schema='public',
                        index=False,
                        chunksize=500,
                        dtype={
                            "Instrumento": String,
                            "Reaj": String,
                            "Duration": Float,
                            "Monto": Float,
                            "Fecha": DateTime,
                            "Familia": String}
                        )
            session.commit()
            print("Data subida hasta", dates[i])
        else:
            print("No data reportada en:", dates[i])


# READ
def query_by_daterange(label, start_date, end_date):
    # elegir tabla
    if label == 'irf':
        input_rows = session.query(IRF).filter(
            IRF.Fecha.between(start_date, end_date))
    elif label == 'iif':
        input_rows = session.query(IIF).filter(
            IIF.Fecha.between(start_date, end_date))
    elif label == 'usdclp':
        input_rows = session.query(USDCLP).filter(
            USDCLP.Fecha.between(start_date, end_date))
    else:
        return None

    df = pd.read_sql(input_rows.statement, input_rows.session.bind)
    df = df.drop(columns='index')

    return df
