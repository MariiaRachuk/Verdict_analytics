import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff


def main():
    page = st.sidebar.selectbox("Choose a page", ["ІПН", "НКС", "Таблицi"])

    if page == "ІПН":
        st.header("This is your data explorer.")
        st.write("Please select a page on the left.")
        df = pd.read_excel(r'\отчеты\\Звіт по іпн.xlsx',
                           sheet_name='Полотно_ІПН')
        values = ['INN', 'К-ть правильних ІПН', 'К-ть перевірених ІПН по безкоштовній перевірці',
                  'К-ть ІПН з майном по безкоштовній перевірці', ' К-ть ІПН з майном на Мирній Україні',
                  'К-ть в Донецька/Луганська обл', ' К-ть ІПН з платною перевіркою за адресою',
                  'К-ть завантажених ІПН з платною перевіркою за адресою', 'К-ть ІПН з майном',
                  'К-ть ІПН з майном в іпотеці',
                  'К-ть ІПН з додатковим майном']
        pivot = pd.pivot_table(df, index=['Сегмент боргу'], values=values, aggfunc={'INN': 'count',
                                         'К-ть правильних ІПН': 'sum',
                                         'К-ть перевірених ІПН по безкоштовній перевірці': 'sum',
                                         'К-ть ІПН з майном по безкоштовній перевірці': 'sum',
                                         ' К-ть ІПН з майном на Мирній Україні': 'sum',
                                         'К-ть в Донецька/Луганська обл': 'sum',
                                         ' К-ть ІПН з платною перевіркою за адресою': 'sum',
                                         'К-ть завантажених ІПН з платною перевіркою за адресою': 'sum',
                                         'К-ть ІПН з майном': 'sum',
                                         'К-ть ІПН з майном в іпотеці': 'sum',
                                         'К-ть ІПН з додатковим майном': 'sum'},
                               margins=True, dropna=True, margins_name='All', observed=False)

        all = st.sidebar.checkbox("Select all")
        if all:
            segment_borg = st.sidebar.container().multiselect('Сегмент боргу?',
                                                              df['Сегмент боргу'].unique(),
                                                              df['Сегмент боргу'].unique())

            right_ipn = st.sidebar.multiselect('К-ть правильних ІПН',
                                               df['К-ть правильних ІПН'].unique(),
                                               df['К-ть правильних ІПН'].unique())


        else:
            segment_borg = st.sidebar.container().multiselect('Сегмент боргу?',
                                                              df['Сегмент боргу'].unique())

            right_ipn = st.sidebar.multiselect('К-ть правильних ІПН',
                                               df['К-ть правильних ІПН'].unique())


        # Filter dataframe
        segment_rigt_right_ipn = df[(df['Сегмент боргу'].isin(segment_borg))
                                              & (df['К-ть правильних ІПН'].isin(right_ipn))]

        # write dataframe to screen

        # for i in segment_rigt_right_ipn['К-ть правильних ІПН']:
        #     print(i)
        # print(segment_rigt_right_ipn['К-ть правильних ІПН'].value_counts())
        # print(segment_rigt_right_ipn.groupby('К-ть правильних ІПН').count())
        # fig = go.Figure(
        #     data=[go.Pie(
        #         labels=segment_rigt_right_ipn['Сегмент боргу'],
        #         values=segment_rigt_right_ipn['К-ть правильних ІПН']
        #     )]
        # )
        # fig = fig.update_traces(
        #     hoverinfo='label',
        #     textinfo='value',
        #     textfont_size=15
        # )

        # create figure using plotly express
        st.markdown('Таблиця за параметрами Сегмент боргу i К-ть правильних ІПН')
        st.write(pivot)
        st.write(segment_rigt_right_ipn)
        #fig = px.histogram(segment_rigt_right_ipn, x='Сегмент боргу')
        #st.plotly_chart(fig)

        # df = input_sql.df.loc[input_sql.df['К-ть правильних ІПН']== 1]
        # fig = px.histogram(df, x='Сегмент боргу', y='К-ть правильних ІПН', text_auto=True)
        # st.plotly_chart(fig)

        # fig = go.Figure()
        # for col in df.columns:
        #     fig.add_trace(go.Bar(x=df['Сегмент боргу'], y=df['К-ть правильних ІПН'], text=df['К-ть правильних ІПН']))
        # st.plotly_chart(fig)


        # df2 = df.loc[df['К-ть правильних ІПН'] == 0]
        # pivot2 = df2.pivot_table(index=['Сегмент боргу'], values=['К-ть правильних ІПН'],
        #                          aggfunc='count')
        # fig = go.Figure()
        # for col in segment_rigt_right_ipn.columns:
        #     fig.add_trace(go.Scatter(x=segment_rigt_right_ipn.index,
        #                              y=segment_rigt_right_ipn[col].values, text=segment_rigt_right_ipn[col].values,
        #                              textposition='top right',
        #                              mode='markers+lines+text',
        #                              line=dict(shape='linear'),
        #                              connectgaps=True
        #                              )
        #                   )
        # st.plotly_chart(fig)

        df1 = df.loc[df['Сегмент боргу'].isin(segment_borg) & df['К-ть правильних ІПН'].isin(right_ipn)]
        pivot1 = df1.pivot_table(index=['Сегмент боргу'], values=['К-ть правильних ІПН'],
                                aggfunc='count')
        fig = go.Figure()
        # for col in pivot1.columns:
        #     fig.add_trace(go.Scatter(x=pivot1.index, y=pivot1[col].values, text=pivot1[col].values,
        #                              textposition='top right',
        #                              mode='markers+lines+text',
        #                              line=dict(shape='linear'),
        #                              connectgaps=True
        #                              )
        #                   )
        #
        # fig = go.Figure()
        for col in pivot1.columns:
            fig.add_trace(go.Bar(x=pivot1.index, y=pivot1[col].values, text=pivot1[col].values))

        st.plotly_chart(fig)


if __name__ == "__main__":
    main()
