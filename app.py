import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import input_sql

# Чекбокс
# df = pd.read_excel('\отчеты\input1.xlsx', 0)
# if st.checkbox('Show dataframe'):
#    st.write(df)
# Выпадающий список

df = st.cache(pd.read_excel)(r'\Users\MRachuk\PycharmProjects\proectExcel\fileTable.xlsx', 0)
# option = st.selectbox(
#    'Сегмент боргу?',
#     df['Сегмент боргу'].unique())
# 'You selected: ', option

# Выбор нескольких значений
# options = st.multiselect(
# 'Сегмент боргу?', df['Сегмент боргу'].unique())
# st.write('You selected:', options)

clubs = st.sidebar.multiselect('Сегмент боргу?', input_sql.table['Сегмент боргу'].unique())
nationalities = st.sidebar.multiselect('К-ть перевірених ІПН по безкоштовній перевірці?',
                                       input_sql.table['К-ть перевірених ІПН по безкоштовній перевірці'].unique())
# Filter dataframe
new_df = input_sql.table[(input_sql.table['Сегмент боргу'].isin(clubs))
                         & (input_sql.table['К-ть перевірених ІПН по безкоштовній перевірці'].isin(nationalities))]
# write dataframe to screen
st.write(new_df)

# create figure using plotly express
fig = px.histogram(new_df, x='Сегмент боргу')
st.plotly_chart(fig)
