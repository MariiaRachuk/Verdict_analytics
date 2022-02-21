import pyodbc
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
import plotly.express as px


@st.cache(allow_output_mutation=True)
def getConnection(server='10.1.32.56', database='Collect',username='sqlbot',password='''9"BgB4J2'''):
    connection = pyodbc.connect('Driver={SQL Server};'f'Server=' + server + ';DATABASE=' + database
                                + ';UID=' + username + ';PWD=' + password)
    return connection


def dbCursor():
    dbCursor = getConnection().cursor()

    return dbCursor


def adding_to_table(table, nameColumn, fileAdd):
    table[nameColumn] = pd.Series(fileAdd)
    return table


def addingfromExcel(file, sheetName, column):
    excel_data_df = pd.read_excel(file, sheet_name=sheetName)
    list_inn = excel_data_df[column].tolist()
    return list_inn


def plot(nameCol, table):
    table.plot(
        kind='bar',
        figsize=(10, 7),
        title=nameCol)
    plt.show()


def to_excel(table, filename):
    excelfile = table.to_excel(filename)
    print('File written')
    return excelfile


def figure_use(nameTable, pivott, table, name_column):
    st.markdown(nameTable)
    st.write(pivott)
    st.write(table)
    fig = px.histogram(table, x=name_column)
    return st.plotly_chart(fig)
