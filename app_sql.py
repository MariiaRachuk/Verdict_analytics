import streamlit as st
import plotly.express as px
import input_sql

pivot_segment = input_sql.pivot_segment
#pivot_active_vd = input_sql.pivot_active_vd
pivot_changed_vd = input_sql.pivot_changed_vd
pivot_active_asvp = input_sql.pivot_active_asvp
pivot_type_vp = input_sql.pivot_type_vp
#df = st.cache(pd.read_excel)(r'fileTable.xlsx', 0)

segment = st.sidebar.multiselect('Сегмент боргу?', input_sql.df['Сегмент боргу'].unique())
right_ipn = st.sidebar.multiselect('К-ть правильних ІПН',
                                       input_sql.df['К-ть правильних ІПН'].unique())
active_vd = st.sidebar.multiselect('К-ть ІПН з діючим ВД', input_sql.df['К-ть ІПН з діючим ВД'].unique())
active_vd_changed = st.sidebar.multiselect('К-ть ІПН з  діючим ВД та заміненою стороною',
                                   input_sql.df['К-ть ІПН з  діючим ВД та заміненою стороною'].unique())
active_asvp = st.sidebar.multiselect('Активне АСВП',
                                   input_sql.df['Активне АСВП'].unique())
vp_type = st.sidebar.multiselect('Тип ВП',
                                   input_sql.df['Тип ВП'].unique())


segment_rightipn_table = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment))
                                & (input_sql.df['К-ть правильних ІПН'].isin(right_ipn))]
segment_activevd_table = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment))
                      & (input_sql.df['К-ть ІПН з діючим ВД'].isin(active_vd))]

segment_changedvd_table = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment))
                      & (input_sql.df['К-ть ІПН з  діючим ВД та заміненою стороною'].isin(active_vd_changed))]

segment_asvp_table = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment))
                      & (input_sql.df['Активне АСВП'].isin(active_asvp))]
segment_typevp_table = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment))
                      & (input_sql.df['Тип ВП'].isin(vp_type))]
# write dataframe to screen

# create figure using plotly express
def figure_use(nameTable, pivot, dff):
    st.markdown(nameTable)
    st.write(pivot)
    st.write(dff)
    fig = px.histogram(dff, x='Сегмент боргу')
    return st.plotly_chart(fig)
pivot_segment['sum'] = pivot_segment.sum(axis=1)

pivot_segment['sum'].fillna(0, inplace=True)
# figure_use('Таблиця за параметрами Сегмент боргу i К-ть правильних ІПН', pivot, new_df)
# figure_use('Таблиця за параметрами Сегмент боргу i К-ть ІПН з діючим ВД', pivot2, new_df1)
# figure_use('Таблиця за параметрами Сегмент боргу i К-ть ІПН з  діючим ВД та заміненою стороною', pivot3, new_df2)
# figure_use('Таблиця за параметрами Сегмент боргу i Активне АСВП', pivot4, new_df3)
# figure_use('Таблиця за параметрами Сегмент боргу i Активне АСВП', pivot4, new_df3)
# # figure_use('Таблиця за параметрами Сегмент боргу i Активне АСВП', pivot5, new_df4)

fig = px.histogram(input_sql.df, x='Сегмент боргу',
                   y=['К-ть ІПН з діючим ВД', 'К-ть ІПН з  діючим ВД та заміненою стороною'], barmode="group")
st.plotly_chart(fig)
