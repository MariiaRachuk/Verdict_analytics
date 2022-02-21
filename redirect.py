import streamlit as st
import plotly.express as px
import input_sql
import input_nks
import pivot_tables
import plotly.graph_objects as go


def main():
    page = st.sidebar.selectbox("Choose a page", ["ІПН", "НКС", "Таблицi"])

    if page == "ІПН":
        st.header("This is your data explorer.")
        st.write("Please select a page on the left.")
        pivot = pivot_tables.pivot_segment
        pivot2 = pivot_tables.pivot_active_vd
        pivot3 = pivot_tables.pivot_changed_vd
        pivot4 = pivot_tables.pivot_active_asvp
        pivot5 = pivot_tables.pivot_type_vp

        all = st.sidebar.checkbox("Select all")
        if all:
            segment_borg = st.sidebar.container().multiselect('Сегмент боргу?',
                                                              input_sql.df['Сегмент боргу'].unique(),
                                                              input_sql.df['Сегмент боргу'].unique())

            right_ipn = st.sidebar.multiselect('К-ть правильних ІПН',
                                               input_sql.df['К-ть правильних ІПН'].unique(),
                                               input_sql.df['К-ть правильних ІПН'].unique())

            active_vd = st.sidebar.multiselect('К-ть ІПН з діючим ВД',
                                               input_sql.df['К-ть ІПН з діючим ВД'].unique(),
                                               input_sql.df['К-ть ІПН з діючим ВД'].unique())

            active_vd_changed = st.sidebar.multiselect('К-ть ІПН з  діючим ВД та заміненою стороною',
                                                       input_sql.df[
                                                           'К-ть ІПН з  діючим ВД та заміненою стороною'].unique(),
                                                       input_sql.df[
                                                           'К-ть ІПН з  діючим ВД та заміненою стороною'].unique())

            active_asvp = st.sidebar.multiselect('Активне АСВП',
                                                 input_sql.df['Активне АСВП'].unique(),
                                                 input_sql.df['Активне АСВП'].unique())

            vp_type = st.sidebar.multiselect('Тип ВП',
                                             input_sql.df['Тип ВП'].unique(),
                                             input_sql.df['Тип ВП'].unique())

        else:
            segment_borg = st.sidebar.container().multiselect('Сегмент боргу?',
                                                              input_sql.df['Сегмент боргу'].unique())

            right_ipn = st.sidebar.multiselect('К-ть правильних ІПН',
                                               input_sql.df['К-ть правильних ІПН'].unique())

            active_vd = st.sidebar.multiselect('К-ть ІПН з діючим ВД',
                                               input_sql.df['К-ть ІПН з діючим ВД'].unique())

            active_vd_changed = st.sidebar.multiselect('К-ть ІПН з  діючим ВД та заміненою стороною',
                                                       input_sql.df[
                                                           'К-ть ІПН з  діючим ВД та заміненою стороною'].unique())

            active_asvp = st.sidebar.multiselect('Активне АСВП',
                                                 input_sql.df['Активне АСВП'].unique())

            vp_type = st.sidebar.multiselect('Тип ВП',
                                             input_sql.df['Тип ВП'].unique())

        # Filter dataframe
        segment_rigt_right_ipn = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                              & (input_sql.df['К-ть правильних ІПН'].isin(right_ipn))]



        segment_active_vd = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                         & (input_sql.df['К-ть ІПН з діючим ВД'].isin(active_vd))]

        segment_vdchange = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                        & (input_sql.df['К-ть ІПН з  діючим ВД та заміненою стороною'].isin(
            active_vd_changed))]

        segment_asvp = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                    & (input_sql.df['Активне АСВП'].isin(active_asvp))]
        segment_vp_type = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                       & (input_sql.df['Тип ВП'].isin(vp_type))]
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

        df1 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                               & input_sql.df['К-ть правильних ІПН'].isin(right_ipn)]
        pivot1 = df1.pivot_table(index=['Сегмент боргу'], values=['К-ть правильних ІПН'],
                                 aggfunc='count')
        fig = go.Figure()
        for col in pivot1.columns:
            fig.add_trace(go.Bar(x=pivot1.index, y=pivot1[col].values, text=pivot1[col].values))

        st.plotly_chart(fig)

        st.markdown('Таблиця за параметрами Сегмент боргу i К-ть ІПН з діючим ВД')
        st.write(pivot2)
        st.write(segment_active_vd)
        df2 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                               & input_sql.df['К-ть ІПН з діючим ВД'].isin(active_vd)]
        pivot_2 = df2.pivot_table(index=['Сегмент боргу'], values=['К-ть ІПН з діючим ВД'],
                                 aggfunc='count')

        fig = go.Figure()
        for col in pivot_2.columns:
            fig.add_trace(go.Bar(x=pivot_2.index, y=pivot_2[col].values, text=pivot_2[col].values))
        st.plotly_chart(fig)

        st.markdown('Таблиця за параметрами Сегмент боргу i К-ть ІПН з  діючим ВД та заміненою стороною')
        st.write(pivot3)
        st.write(segment_vdchange)
        df3 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                               & input_sql.df['К-ть ІПН з  діючим ВД та заміненою стороною'].isin(active_vd_changed)]
        pivot_3 = df3.pivot_table(index=['Сегмент боргу'], values=['К-ть ІПН з  діючим ВД та заміненою стороною'],
                                  aggfunc='count')

        fig = go.Figure()
        for col in pivot_3.columns:
            fig.add_trace(go.Bar(x=pivot_3.index, y=pivot_3[col].values, text=pivot_3[col].values))
        st.plotly_chart(fig)
        st.markdown('Таблиця за параметрами Сегмент боргу i Активне АСВП')
        st.write(pivot4)
        st.write(segment_asvp)
        df4 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                               & input_sql.df['Активне АСВП'].isin(active_asvp)]
        pivot_4 = df4.pivot_table(index=['Сегмент боргу'], values=['Активне АСВП'],
                                  aggfunc='count')
        fig = go.Figure()
        for col in pivot_4.columns:
            fig.add_trace(go.Bar(x=pivot_4.index, y=pivot_4[col].values, text=pivot_4[col].values))
        st.plotly_chart(fig)
        st.markdown('Таблиця за параметрами Сегмент боргу i Тип ВП')
        st.write(pivot5)
        st.write(segment_vp_type)
        df5 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                               & input_sql.df['Тип ВП'].isin(vp_type)]
        pivot_5 = df5.pivot_table(index=['Сегмент боргу'], values=['Тип ВП'],
                                  aggfunc='count')
        fig = go.Figure()
        for col in pivot_5.columns:
            fig.add_trace(go.Bar(x=pivot_5.index, y=pivot_5[col].values, text=pivot_5[col].values))
        st.plotly_chart(fig)

    elif page == "НКС":
        st.title("Таблиця для НКC")
        pivot1 = input_nks.pivot_business_borg30
        pivot2 = input_nks.pivot_business_borg30_vd
        pivot3 = input_nks.pivot_business_borg30_active_vd
        pivot4 = input_nks.pivot_business_borg30_asvp
        pivot5 = input_nks.pivot_business_borg30_vp_type

        all = st.sidebar.checkbox("Select all")
        if all:
            busines = st.sidebar.multiselect('Бізнес?',
                                             input_nks.df1['Бізнес'].unique(),
                                             input_nks.df1['Бізнес'].unique())

            borg_30k = st.sidebar.multiselect('К-ть НКС з боргом від 30к грн',
                                              input_nks.df1['К-ть НКС з боргом від 30к грн'].unique(),
                                              input_nks.df1['К-ть НКС з боргом від 30к грн'].unique())
            active_vd = st.sidebar.multiselect('К-ть ІПН з діючим ВД',
                                               input_nks.df1['К-ть ІПН з діючим ВД'].unique(),
                                               input_nks.df1['К-ть ІПН з діючим ВД'].unique())

            active_vd_changed = st.sidebar.multiselect('К-ть ІПН з  діючим ВД та заміненою стороною',
                                                       input_nks.df1[
                                                           'К-ть ІПН з  діючим ВД та заміненою стороною'].unique(),
                                                       input_nks.df1[
                                                           'К-ть ІПН з  діючим ВД та заміненою стороною'].unique())

            active_asvp = st.sidebar.multiselect('Активне АСВП',
                                                 input_nks.df1['Активне АСВП'].unique(),
                                                 input_nks.df1['Активне АСВП'].unique())

            vp_type = st.sidebar.multiselect('Тип ВП',
                                             input_nks.df1['Тип ВП'].unique(),
                                             input_nks.df1['Тип ВП'].unique())

        else:
            busines = st.sidebar.multiselect('Бізнес?',
                                             input_nks.df1['Бізнес'].unique())

            borg_30k = st.sidebar.multiselect('К-ть НКС з боргом від 30к грн',
                                              input_nks.df1['К-ть НКС з боргом від 30к грн'].unique())

            active_vd = st.sidebar.multiselect('К-ть ІПН з діючим ВД',
                                               input_nks.df1['К-ть ІПН з діючим ВД'].unique())

            active_vd_changed = st.sidebar.multiselect('К-ть ІПН з  діючим ВД та заміненою стороною',
                                                       input_nks.df1[
                                                           'К-ть ІПН з  діючим ВД та заміненою стороною'].unique())

            active_asvp = st.sidebar.multiselect('Активне АСВП',
                                                 input_nks.df1['Активне АСВП'].unique())

            vp_type = st.sidebar.multiselect('Тип ВП',
                                             input_nks.df1['Тип ВП'].unique())

        # Filter dataframe
        busines_borg30 = input_nks.df1[(input_nks.df1['Бізнес'].isin(busines))
                                       & (input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k))]

        busines_activeVD = input_nks.df1[(input_nks.df1['Бізнес'].isin(busines))
                                         & (input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k))
                                         & (input_nks.df1['К-ть ІПН з діючим ВД'].isin(active_vd))]

        busines_vdchange = input_nks.df1[(input_nks.df1['Бізнес'].isin(busines))
                                         & (input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k))
                                         & (input_nks.df1['К-ть ІПН з  діючим ВД та заміненою стороною'].isin(
            active_vd_changed))]

        busines_vsvp = input_nks.df1[(input_nks.df1['Бізнес'].isin(busines))
                                     & (input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k))
                                     & (input_nks.df1['Активне АСВП'].isin(active_asvp))]

        busines_vp_type = input_nks.df1[(input_nks.df1['Бізнес'].isin(busines))
                                        & (input_nks.df1['Тип ВП'].isin(vp_type))]

        st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн')
        st.write(pivot1)
        st.write(busines_borg30)
        df_1 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(busines)
                               & input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k)]
        pivot_1 = df_1.pivot_table(index=['Бізнес'], values=['К-ть НКС з боргом від 30к грн'],
                                  aggfunc='count')
        fig = go.Figure()
        for col in pivot_1.columns:
            fig.add_trace(go.Bar(x=pivot_1.index, y=pivot_1[col].values, text=pivot_1[col].values))
        st.plotly_chart(fig)

        st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн, i К-ть ІПН з діючим ВД')
        st.write(pivot2)
        st.write(busines_activeVD)
        df_2 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(busines)
                                 & input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k)
                & input_nks.df1['К-ть ІПН з діючим ВД'].isin(active_vd)]

        pivot_2 = df_2.pivot_table(index=['Бізнес'], values=['К-ть ІПН з діючим ВД'],
                                   aggfunc='count')
        fig = go.Figure()
        for col in pivot_2.columns:
            fig.add_trace(go.Bar(x=pivot_2.index, y=pivot_2[col].values, text=pivot_2[col].values))
        st.plotly_chart(fig)

        st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн, '
                    'i К-ть ІПН з  діючим ВД та заміненою стороною')
        st.write(pivot3)
        st.write(busines_vdchange)
        df_3 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(busines)
                                 & input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k)
              & input_nks.df1['К-ть ІПН з  діючим ВД та заміненою стороною'].isin(active_vd_changed)]

        pivot_3 = df_3.pivot_table(index=['Бізнес'], values=['К-ть ІПН з  діючим ВД та заміненою стороною'],
                                   aggfunc='count')
        fig = go.Figure()
        for col in pivot_3.columns:
            fig.add_trace(go.Bar(x=pivot_3.index, y=pivot_3[col].values, text=pivot_3[col].values))
        st.plotly_chart(fig)

        st.markdown('Таблиця за параметрами Бізнес i К-ть НКС з боргом від 30к грн, i Активне АСВП')
        st.write(pivot4)
        st.write(busines_vsvp)
        df_4 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(busines)
                                 & input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30k)
              & input_nks.df1[
                       'Активне АСВП'].isin(active_asvp)]

        pivot_4 = df_4.pivot_table(index=['Бізнес'], values=['Активне АСВП'],
                                   aggfunc='count')
        fig = go.Figure()
        for col in pivot_4.columns:
            fig.add_trace(go.Bar(x=pivot_4.index, y=pivot_4[col].values, text=pivot_4[col].values))
        st.plotly_chart(fig)

        st.markdown('Таблиця за параметрами Бізнес i Тип ВП')
        st.write(pivot5)
        st.write(busines_vp_type)
        df_5 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(busines)
                                 & input_nks.df1['Тип ВП'].isin(vp_type)]
        pivot_5 = df_5.pivot_table(index=['Бізнес'], values=['Тип ВП'],
                                   aggfunc='count')
        fig = go.Figure()
        for col in pivot_5.columns:
            fig.add_trace(go.Bar(x=pivot_5.index, y=pivot_5[col].values, text=pivot_5[col].values))
        st.plotly_chart(fig)

    elif page == "Таблицi":
        all = st.sidebar.checkbox("Select all")
        if all:
            business = st.sidebar.multiselect('Бізнес?',
                                              input_nks.df1['Бізнес'].unique(),
                                              input_nks.df1['Бізнес'].unique())

            borg_30kk = st.sidebar.multiselect('К-ть НКС з боргом від 30к грн',
                                               input_nks.df1['К-ть НКС з боргом від 30к грн'].unique(),
                                               input_nks.df1['К-ть НКС з боргом від 30к грн'].unique())

            free_check = st.sidebar.multiselect('К-ть  НКС перевірених по безкоштовній перевірці',
                                                input_nks.df1[
                                                    'К-ть  НКС перевірених по безкоштовній перевірці'].unique(),
                                                input_nks.df1[
                                                    'К-ть  НКС перевірених по безкоштовній перевірці'].unique())

            free_check_property = st.sidebar.multiselect('К-ть НКС з майном по безкоштовній перевірці',
                                                         input_nks.df1[
                                                             'К-ть НКС з майном по безкоштовній перевірці'].unique(),
                                                         input_nks.df1[
                                                             'К-ть НКС з майном по безкоштовній перевірці'].unique())

            dowload_pay_check = st.sidebar.multiselect('К-ть завантажених НКС з платною перевіркою',
                                                       input_nks.df1[
                                                           'К-ть завантажених НКС з платною перевіркою'].unique(),
                                                       input_nks.df1[
                                                           'К-ть завантажених НКС з платною перевіркою'].unique())

            with_propertry = st.sidebar.multiselect('К-ть НКС з майном',
                                                    input_nks.df1['К-ть НКС з майном'].unique(),
                                                    input_nks.df1['К-ть НКС з майном'].unique())

            segment_borg = st.sidebar.container().multiselect('Сегмент боргу?',
                                                              input_sql.df['Сегмент боргу'].unique(),
                                                              input_sql.df['Сегмент боргу'].unique())

            right_ipn = st.sidebar.multiselect('К-ть правильних ІПН',
                                               input_sql.df['К-ть правильних ІПН'].unique(),
                                               input_sql.df['К-ть правильних ІПН'].unique())

            check_free_ipn = st.sidebar.multiselect('К-ть перевірених ІПН по безкоштовній перевірці',
                                                    input_sql.df[
                                                        'К-ть перевірених ІПН по безкоштовній перевірці'].unique(),
                                                    input_sql.df[
                                                        'К-ть перевірених ІПН по безкоштовній перевірці'].unique())

            check_free_property_ipn = st.sidebar.multiselect('К-ть ІПН з майном по безкоштовній перевірці',
                                                             input_sql.df[
                                                                 'К-ть ІПН з майном по безкоштовній перевірці'].unique(),
                                                             input_sql.df[
                                                                 'К-ть ІПН з майном по безкоштовній перевірці'].unique())

            properety_ipn = st.sidebar.multiselect('К-ть ІПН з майном',
                                                   input_sql.df['К-ть ІПН з майном'].unique(),
                                                   input_sql.df['К-ть ІПН з майном'].unique())

            in_peaceful_Ukr = st.sidebar.multiselect(' К-ть ІПН з майном на Мирній Україні iпн',
                                                     input_sql.df[' К-ть ІПН з майном на Мирній Україні'].unique(),
                                                     input_sql.df[' К-ть ІПН з майном на Мирній Україні'].unique())

            check_download = st.sidebar.multiselect('К-ть завантажених ІПН з платною перевіркою за адресою',
                                                    input_sql.df[
                                                        'К-ть завантажених ІПН з платною перевіркою за адресою'].unique(),
                                                    input_sql.df[
                                                        'К-ть завантажених ІПН з платною перевіркою за адресою'].unique())

        else:
            business = st.sidebar.multiselect('Бізнес?',
                                              input_nks.df1['Бізнес'].unique())

            borg_30kk = st.sidebar.multiselect('К-ть НКС з боргом від 30к грн',
                                               input_nks.df1['К-ть НКС з боргом від 30к грн'].unique())

            free_check = st.sidebar.multiselect('К-ть  НКС перевірених по безкоштовній перевірці',
                                                input_nks.df1[
                                                    'К-ть  НКС перевірених по безкоштовній перевірці'].unique())

            free_check_property = st.sidebar.multiselect('К-ть НКС з майном по безкоштовній перевірці',
                                                         input_nks.df1[
                                                             'К-ть НКС з майном по безкоштовній перевірці'].unique())

            dowload_pay_check = st.sidebar.multiselect('К-ть завантажених НКС з платною перевіркою',
                                                       input_nks.df1[
                                                           'К-ть завантажених НКС з платною перевіркою'].unique())

            with_propertry = st.sidebar.multiselect('К-ть НКС з майном',
                                                    input_nks.df1['К-ть НКС з майном'].unique())

            segment_borg = st.sidebar.container().multiselect('Сегмент боргу?',
                                                              input_sql.df['Сегмент боргу'].unique())

            right_ipn = st.sidebar.multiselect('К-ть правильних ІПН',
                                               input_sql.df['К-ть правильних ІПН'].unique())

            check_free_ipn = st.sidebar.multiselect('К-ть перевірених ІПН по безкоштовній перевірці',
                                                    input_sql.df[
                                                        'К-ть перевірених ІПН по безкоштовній перевірці'].unique())

            check_free_property_ipn = st.sidebar.multiselect('К-ть ІПН з майном по безкоштовній перевірці',
                                                             input_sql.df[
                                                                 'К-ть ІПН з майном по безкоштовній перевірці'].unique())

            properety_ipn = st.sidebar.multiselect('К-ть ІПН з майном',
                                                   input_sql.df['К-ть ІПН з майном'].unique())

            in_peaceful_Ukr = st.sidebar.multiselect(' К-ть ІПН з майном на Мирній Україні iпн',
                                                     input_sql.df[' К-ть ІПН з майном на Мирній Україні'].unique())

            check_download = st.sidebar.multiselect('К-ть завантажених ІПН з платною перевіркою за адресою',
                                                    input_sql.df[
                                                        'К-ть завантажених ІПН з платною перевіркою за адресою'].unique())

        business_free_check = input_nks.df1[(input_nks.df1['Бізнес'].isin(business))
                                            & (input_nks.df1['К-ть  НКС перевірених по безкоштовній перевірці']
                                               .isin(free_check))
                                            & (input_nks.df1['К-ть НКС з майном по безкоштовній перевірці']
                                               .isin(free_check_property))]

        business_free_pay_check = input_nks.df1[(input_nks.df1['Бізнес'].isin(business))
                                                & (input_nks.df1[
                                                       'К-ть  НКС перевірених по безкоштовній перевірці']
                                                   .isin(free_check))
                                                & (input_nks.df1['К-ть завантажених НКС з платною перевіркою']
                                                   .isin(dowload_pay_check))]

        # business_borg_check = input_nks.df1[(input_nks.df1['Бізнес'].isin(business))
        #                                    & (input_nks.df1['К-ть  НКС перевірених по безкоштовній перевірці'].isin(free_check))
        #                                    & (input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30kk))]

        business_property_check = input_nks.df1[(input_nks.df1['Бізнес'].isin(business))
                                                & (input_nks.df1['К-ть НКС з майном по безкоштовній перевірці']
                                                   .isin(free_check_property))
                                                & (input_nks.df1['К-ть НКС з майном'].isin(with_propertry))]

        segment_free_check = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                          & (input_sql.df['К-ть перевірених ІПН по безкоштовній перевірці']
                                             .isin(check_free_ipn))
                                          & (input_sql.df['К-ть ІПН з майном по безкоштовній перевірці']
                                             .isin(check_free_property_ipn))]

        segment_free_right_check = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                                & (input_sql.df['К-ть перевірених ІПН по безкоштовній перевірці']
                                                   .isin(check_free_ipn))
                                                & (input_sql.df['К-ть правильних ІПН'].isin(right_ipn))]

        segment_property_check = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                              & (input_sql.df['К-ть ІПН з майном по безкоштовній перевірці']
                                                 .isin(check_free_property_ipn))
                                              & (input_sql.df['К-ть ІПН з майном'].isin(properety_ipn))]

        segment_pro = input_sql.df[(input_sql.df['Сегмент боргу'].isin(segment_borg))
                                   & (input_sql.df['К-ть перевірених ІПН по безкоштовній перевірці'].isin(check_free_ipn))
                                   & (input_sql.df[' К-ть ІПН з майном на Мирній Україні'].isin(in_peaceful_Ukr))
                                   & (input_sql.df['К-ть завантажених ІПН з платною перевіркою за адресою']
                                      .isin(check_download))]

        fig = px.histogram(business_free_check,
                           x='Бізнес',
                           y=['К-ть  НКС перевірених по безкоштовній перевірці',
                              'К-ть НКС з майном по безкоштовній перевірці'],
                           barmode="group")
        st.write(business_free_check)

        st.plotly_chart(fig)

        df_1 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(business)
                                 & input_nks.df1['К-ть  НКС перевірених по безкоштовній перевірці'].isin(free_check)
                                 & input_nks.df1['К-ть НКС з майном по безкоштовній перевірці'].isin(free_check_property)]
        pivot_1 = df_1.pivot_table(index=['Бізнес'], values=['К-ть  НКС перевірених по безкоштовній перевірці',
                                                             'К-ть НКС з майном по безкоштовній перевірці'],
                                   aggfunc={'К-ть  НКС перевірених по безкоштовній перевірці': 'count',
                                            'К-ть НКС з майном по безкоштовній перевірці': 'count'})
        fig = go.Figure()
        st.write(pivot_1)
        st.write(df_1)
        for col in pivot_1.columns:
            fig.add_trace(go.Bar(x=pivot_1.index, y=pivot_1[col].values, text=pivot_1[col].values))
        st.plotly_chart(fig)

        fig = px.histogram(business_free_pay_check,
                           x='Бізнес',
                           y=['К-ть  НКС перевірених по безкоштовній перевірці',
                              'К-ть завантажених НКС з платною перевіркою'],
                           barmode="group")
        st.plotly_chart(fig)
        df_2 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(business)
                                 & input_nks.df1['К-ть  НКС перевірених по безкоштовній перевірці'].isin(free_check)
                                 & input_nks.df1['К-ть завантажених НКС з платною перевіркою'].isin(dowload_pay_check)]
        pivot_2 = df_2.pivot_table(index=['Бізнес'], values=['К-ть  НКС перевірених по безкоштовній перевірці',
                                                             'К-ть завантажених НКС з платною перевіркою'],
                                   aggfunc={'К-ть  НКС перевірених по безкоштовній перевірці': 'count',
                                            'К-ть завантажених НКС з платною перевіркою': 'count'})
        fig = go.Figure()
        for col in pivot_2.columns:
            fig.add_trace(go.Bar(x=pivot_2.index, y=pivot_2[col].values, text=pivot_2[col].values))
        st.plotly_chart(fig)

        # fig = px.histogram(business_borg_check,
        #                    x='Бізнес',
        #                    y=['К-ть  НКС перевірених по безкоштовній перевірці',
        #                       'К-ть НКС з боргом від 30к грн'],
        #                    barmode="group")
        # st.plotly_chart(fig)

        df_3 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(business)
                                 & input_nks.df1['К-ть  НКС перевірених по безкоштовній перевірці'].isin(free_check)
                                 & input_nks.df1['К-ть НКС з боргом від 30к грн'].isin(borg_30kk)]
        pivot_3 = df_3.pivot_table(index=['Бізнес'], values=['К-ть  НКС перевірених по безкоштовній перевірці',
                                                             'К-ть НКС з боргом від 30к грн'],
                                   aggfunc={'К-ть  НКС перевірених по безкоштовній перевірці': 'count',
                                            'К-ть НКС з боргом від 30к грн': 'count'})
        fig = go.Figure()
        for col in pivot_3.columns:
            fig.add_trace(go.Bar(x=pivot_3.index, y=pivot_3[col].values, text=pivot_3[col].values))
        st.plotly_chart(fig)

        fig = px.histogram(business_property_check,
                           x='Бізнес',
                           y=['К-ть НКС з майном по безкоштовній перевірці',
                              'К-ть НКС з майном'],
                           barmode="group")
        st.plotly_chart(fig)
        df_4 = input_nks.df1.loc[input_nks.df1['Бізнес'].isin(business)
                                 & input_nks.df1['К-ть НКС з майном по безкоштовній перевірці'].isin(free_check_property)
                                 & input_nks.df1['К-ть НКС з майном'].isin(with_propertry)]
        pivot_4 = df_4.pivot_table(index=['Бізнес'], values=['К-ть НКС з майном по безкоштовній перевірці',
                                                             'К-ть НКС з майном'],
                                   aggfunc={'К-ть НКС з майном по безкоштовній перевірці': 'count',
                                            'К-ть НКС з майном': 'count'})
        fig = go.Figure()
        for col in pivot_4.columns:
            fig.add_trace(go.Bar(x=pivot_4.index, y=pivot_4[col].values, text=pivot_4[col].values))
        st.plotly_chart(fig)

        fig = px.histogram(segment_free_check,
                           x='Сегмент боргу',
                           y=['К-ть перевірених ІПН по безкоштовній перевірці',
                              'К-ть ІПН з майном по безкоштовній перевірці'],
                           barmode="group")
        st.plotly_chart(fig)
        df_5 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                                 & input_sql.df['К-ть перевірених ІПН по безкоштовній перевірці'].isin(check_free_ipn)
                                 & input_sql.df['К-ть ІПН з майном по безкоштовній перевірці'].isin(check_free_property_ipn)]
        pivot_5 = df_5.pivot_table(index=['Сегмент боргу'], values=['К-ть перевірених ІПН по безкоштовній перевірці',
                                                             'К-ть ІПН з майном по безкоштовній перевірці'],
                                   aggfunc={'К-ть перевірених ІПН по безкоштовній перевірці': 'count',
                                            'К-ть ІПН з майном по безкоштовній перевірці': 'count'})
        fig = go.Figure()
        for col in pivot_5.columns:
            fig.add_trace(go.Bar(x=pivot_5.index, y=pivot_5[col].values, text=pivot_5[col].values))
        st.plotly_chart(fig)

        fig = px.histogram(segment_free_right_check,
                           x='Сегмент боргу',
                           y=['К-ть перевірених ІПН по безкоштовній перевірці',
                              'К-ть правильних ІПН'],
                           barmode="group")
        st.plotly_chart(fig)

        df_6 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                                & input_sql.df['К-ть перевірених ІПН по безкоштовній перевірці'].isin(check_free_ipn)
                                & input_sql.df['К-ть правильних ІПН'].isin(right_ipn)]
        pivot_6 = df_6.pivot_table(index=['Сегмент боргу'], values=['К-ть перевірених ІПН по безкоштовній перевірці',
                                                                    'К-ть правильних ІПН'],
                                   aggfunc={'К-ть перевірених ІПН по безкоштовній перевірці': 'count',
                                            'К-ть правильних ІПН': 'count'})
        fig = go.Figure()
        for col in pivot_6.columns:
            fig.add_trace(go.Bar(x=pivot_6.index, y=pivot_6[col].values, text=pivot_6[col].values))
        st.plotly_chart(fig)

        fig = px.histogram(segment_property_check,
                           x='Сегмент боргу',
                           y=['К-ть ІПН з майном по безкоштовній перевірці',
                              'К-ть ІПН з майном'],
                           barmode="group")
        st.plotly_chart(fig)
        df_7 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                                & input_sql.df['К-ть ІПН з майном по безкоштовній перевірці'].isin(check_free_property_ipn)
                                & input_sql.df['К-ть ІПН з майном'].isin(properety_ipn)]
        pivot_7 = df_7.pivot_table(index=['Сегмент боргу'], values=['К-ть ІПН з майном по безкоштовній перевірці',
                                                                    'К-ть ІПН з майном'],
                                   aggfunc={'К-ть ІПН з майном по безкоштовній перевірці': 'count',
                                            'К-ть ІПН з майном': 'count'})
        fig = go.Figure()
        for col in pivot_7.columns:
            fig.add_trace(go.Bar(x=pivot_7.index, y=pivot_7[col].values, text=pivot_7[col].values))
        st.plotly_chart(fig)

        fig = px.histogram(segment_pro,
                           x='Сегмент боргу',
                           y=['К-ть перевірених ІПН по безкоштовній перевірці',
                              ' К-ть ІПН з майном на Мирній Україні',
                              'К-ть завантажених ІПН з платною перевіркою за адресою'],
                           barmode="group")
        st.plotly_chart(fig)
        df_8 = input_sql.df.loc[input_sql.df['Сегмент боргу'].isin(segment_borg)
                                & input_sql.df['К-ть перевірених ІПН по безкоштовній перевірці'].isin(check_free_ipn)
                                & input_sql.df[' К-ть ІПН з майном на Мирній Україні'].isin(in_peaceful_Ukr)
                                & input_sql.df['К-ть завантажених ІПН з платною перевіркою за адресою'].isin(check_download)]
        pivot_8 = df_8.pivot_table(index=['Сегмент боргу'], values=['К-ть перевірених ІПН по безкоштовній перевірці',
                                                                    ' К-ть ІПН з майном на Мирній Україні',
                                                                    'К-ть завантажених ІПН з платною перевіркою за адресою'],
                                   aggfunc={'К-ть перевірених ІПН по безкоштовній перевірці': 'count',
                                            ' К-ть ІПН з майном на Мирній Україні': 'count',
                                            'К-ть завантажених ІПН з платною перевіркою за адресою': 'count'})
        fig = go.Figure()
        for col in pivot_8.columns:
            fig.add_trace(go.Bar(x=pivot_8.index, y=pivot_8[col].values, text=pivot_8[col].values))
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()
