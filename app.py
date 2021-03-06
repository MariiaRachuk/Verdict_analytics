import streamlit as st
import pandas as pd
import plotly.express as px


df = st.cache(pd.read_excel)(r'fileTable.xlsx', 0)

clubs = st.sidebar.multiselect('Сегмент боргу?', df['Сегмент боргу'].unique())
nationalities = st.sidebar.multiselect('К-ть перевірених ІПН по безкоштовній перевірці?',
                                       df['К-ть перевірених ІПН по безкоштовній перевірці'].unique())
# Filter dataframe
new_df = df[(df['Сегмент боргу'].isin(clubs))
                         & (df['К-ть перевірених ІПН по безкоштовній перевірці'].isin(nationalities))]
# write dataframe to screen

st.write(df)

# create figure using plotly express
fig = px.histogram(new_df, x='Сегмент боргу')
st.plotly_chart(fig)
