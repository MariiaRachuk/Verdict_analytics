import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
import inputing
import input_nks

# df1 = st.cache(pd.read_excel)(r'\\10.1.32.250\Documents repository DOP'
#                                                        r'\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
#                               sheet_name='Полотно НКС')
# pivot = input_nks.table
# pivot2 = input_nks.table2
# pivot3 = input_nks.table3
# pivot4 = input_nks.table4
# pivot5 = input_nks.table5

# ff = inputing.addingfromExcel(file=r'\\10.1.32.250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
#                               sheetName='Полотно НКС', column='Тип ВП')
#
# vp_type = [str(row) for row in ff]
# inputing.adding_to_table(df1, 'Тип ВП', vp_type)

busines = st.sidebar.multiselect('Бізнес?', input_nks.Initialisation_nsk.load_database()['Бізнес'].unique())
borg30k = st.sidebar.multiselect('К-ть НКС з боргом від 30к грн',
                                       input_nks.Initialisation_nsk.load_database()['К-ть НКС з боргом від 30к грн'].unique())
# active_vd = st.sidebar.multiselect('К-ть ІПН з діючим ВД', df1['К-ть ІПН з діючим ВД'].unique())
# active_vd_changed = st.sidebar.multiselect('К-ть ІПН з  діючим ВД та заміненою стороною',
#                                            df1['К-ть ІПН з  діючим ВД та заміненою стороною'].unique())
# active_asvp = st.sidebar.multiselect('Активне АСВП', df1['Активне АСВП'].unique())
# vp_type = st.sidebar.multiselect('Тип ВП', df1['Тип ВП'].unique())

# Filter dataframe
busines_borg30_table = input_nks.Initialisation_nsk.load_database()[(input_nks.Initialisation_nsk.load_database()['Бізнес'].isin(busines))
                       & (input_nks.Initialisation_nsk.load_database()['К-ть НКС з боргом від 30к грн'].isin(borg30k))]

# borg30_activevd_table = df1[(df1['Бізнес'].isin(busines))
#                         & (df1['К-ть НКС з боргом від 30к грн'].isin(borg30k))
#               & (df1['К-ть ІПН з діючим ВД'].isin(active_vd))]
# borg30_changedvd_table = df1[(df1['Бізнес'].isin(busines))
#                         & (df1['К-ть НКС з боргом від 30к грн'].isin(borg30k))
#               & (df1['К-ть ІПН з  діючим ВД та заміненою стороною'].isin(active_vd_changed))]
# borg30_asvp_table = df1[(df1['Бізнес'].isin(busines))
#                         & (df1['К-ть НКС з боргом від 30к грн'].isin(borg30k))
#               & (df1['Активне АСВП'].isin(active_asvp))]
# busines_typevp_table = df1[(df1['Бізнес'].isin(busines))
#               & (df1['Тип ВП'].isin(vp_type))]
# write dataframe to screen

# create figure using plotly express
st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн')
#st.write(pivot)
st.write(busines_borg30_table)
fig = px.histogram(busines_borg30_table, x='Бізнес')
st.plotly_chart(fig)

# st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн, i К-ть ІПН з діючим ВД')
# #st.write(pivot2)
# st.write(borg30_activevd_table)
# fig = px.histogram(borg30_activevd_table, x='Бізнес')
# st.plotly_chart(fig)
#
# st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн, i К-ть ІПН з  діючим ВД та заміненою стороною')
# #st.write(pivot3)
# st.write(borg30_changedvd_table)
# fig = px.histogram(borg30_changedvd_table, x='Бізнес')
# st.plotly_chart(fig)
#
# st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн, i Активне АСВП')
# #st.write(pivot4)
# st.write(borg30_asvp_table)
# fig = px.histogram(borg30_asvp_table, x='Бізнес')
# st.plotly_chart(fig)
#
# st.markdown('Таблиця за параметрами Бізнес i Тип ВП')
# #st.write(pivot5)
# st.write(busines_typevp_table)
# fig = px.histogram(busines_typevp_table, x='Бізнес')
# st.plotly_chart(fig)