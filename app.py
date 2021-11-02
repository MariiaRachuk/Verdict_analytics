import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import input_sql
pivot = (input_sql.table)
df = st.cache(pd.read_excel)(r'\Users\MRachuk\PycharmProjects\proectExcel\fileTable.xlsx', 0)

clubs = st.sidebar.multiselect('Сегмент боргу?', df['Сегмент боргу'].unique())
nationalities = st.sidebar.multiselect('К-ть перевірених ІПН по безкоштовній перевірці?',
                                       df['К-ть перевірених ІПН по безкоштовній перевірці'].unique())
# Filter dataframe
new_df = df[(df['Сегмент боргу'].isin(clubs))
                         & (df['К-ть перевірених ІПН по безкоштовній перевірці'].isin(nationalities))]
# write dataframe to screen
st.write(pivot)

st.write(df)

# create figure using plotly express
fig = px.histogram(new_df, x='Сегмент боргу')
st.plotly_chart(fig)
