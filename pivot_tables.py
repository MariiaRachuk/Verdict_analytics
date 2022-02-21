# st.markdown('Таблиця за параметрами Сегмент боргу i К-ть ІПН з діючим ВД')
# st.write(pivot2)
# st.write(new_df1)
# fig = px.histogram(new_df1, x='Сегмент боргу')
# st.plotly_chart(fig)
#
# st.markdown('Таблиця за параметрами Сегмент боргу i К-ть ІПН з  діючим ВД та заміненою стороною')
# st.write(pivot3)
# st.write(new_df2)
# fig = px.histogram(new_df2, x='Сегмент боргу')
# st.plotly_chart(fig)
#
# st.markdown('Таблиця за параметрами Сегмент боргу i Активне АСВП')
# st.write(pivot4)
# st.write(new_df3)
# fig = px.histogram(new_df3, x='Сегмент боргу')
# st.plotly_chart(fig)
# графики

# def normalization(funk):
#     def wrapper(*args, **kwargd):
#         funk(*args, **kwargd)
#         normalized = [k + f for k, f in zip_longest(addingColumns(x,y), addingColumns(x,y), fillvalue=0)]
#         for key, value in enumerate(normalized):
#             if value < 1:
#                 normalized[key] = 0
#             else:
#                 normalized[key] = 1
#
#         return normalized
#
#     return wrapper
#
#
# @normalization
# def addingColumns(column_name1, column_name2):
#     global df
#     property_mortgage = [int(row) for row in df[column_name1]]
#     property_extra = [int(row) for row in df[column_name2]]
#     return property_mortgage, property_extra
# a = addingColumns('К-ть ІПН з майном в іпотеці', 'К-ть ІПН з додатковим майном')


# clubs = st.sidebar.multiselect('Бізнес?', df1['Бізнес'].unique())
# nationalities = st.sidebar.multiselect('К-ть НКС з боргом від 30к грн',
#                                        df1['К-ть НКС з боргом від 30к грн'].unique())
# active_vd = st.sidebar.multiselect('К-ть ІПН з діючим ВД',
#                                    df1['К-ть ІПН з діючим ВД'].unique())
# active_vd_changed = st.sidebar.multiselect('К-ть ІПН з  діючим ВД та заміненою стороною',
#                                            df1['К-ть ІПН з  діючим ВД та заміненою стороною'].unique())
# active_asvp = st.sidebar.multiselect('Активне АСВП',
#                                      df1['Активне АСВП'].unique())
import locale
import sys
import pyodbc
import pandas as pd

# sys.setrecursionlimit(5000)
# server = '10.1.32.56'
# database = 'Collect'
# username = 'sqlbot'
# password = '''9"BgB4J2'''
# connection = pyodbc.connect('Driver={SQL Server};'f'Server='
#                                 f'' + server + ';DATABASE=' + database
#                                 + ';UID=' + username + ';PWD=' + password)
#
# dbCursor = connection.cursor()
# dbCursor.fast_executemany = True
# requestString = ''' Select distinct c.id , isnull(pro.Name, r.name) as 'Проект',
#         cast(case when c.CurrencyId = 8 then SummToClose * 1
#         when c.CurrencyId = 9 then SummToClose * 27.2
#         when c.CurrencyId = 10 then SummToClose * 31.45
#         when c.CurrencyId = 19 then SummToClose * 29.32
#         else SummToClose * 1 end  AS float)  as 'Сума боргу',
#         case when  r.RNumber in (3847, 3846, 3845)  then 'Беззаставні'
#         when cg.name like 'Ипотека_%' then 'Іпотека'
#         when cg.name like 'авто%' then 'Авто'
#         when cg.name like 'КЦ%' then 'Авто'
#         else 'Беззаставні' end as 'Бізнес',
#         case when fpc.conID is null then '0'
#         else '1' end as 'К-ть  НКС перевірених по безкоштовній перевірці',
#         case when maino.conID is null then '0'
#         else '1' end as 'К-ть НКС з майном по безкоштовній перевірці',
#         case when mu1.conID is null then '0'
#         else '1' end as 'К-ть НКС з майном на Мирній Україні',
#         case when ato.conID is null then '0'
#         else '1' end as 'К-ть НКС з майном в Донецькій/Луганській обл',
#         case when pp.ContractId is null then 0
#         else 1 end as 'К-ть завантажених НКС з платною перевіркою',
#         case when ipo.conID is null then 0
#         else 1 end as 'К-ть НКС з майном в іпотеці',
#         case when adp.conID is null then 0
#         else 1 end as 'К-ть НКС з додатковим майном',
#         case when vd_all.NKS is null then 0
#         else  1 end 'К-ть ІПН з діючим ВД',
#         case when zam_all.NKS is null then 0
#         else  1 end 'К-ть ІПН з  діючим ВД та заміненою стороною'
#         from Collect.dbo.reestr r
#         inner join collect.dbo.contract c on c.ReestrId = r.id
#         left join [10.1.32.64].legalcollection.property.collectiongroup cg on c.id = cg.contractid
#         left join (select p.RNumber, n.Name from SDSD.Invest.NKSInvestProject p
#                         left join SDSD.Invest.InvestProject n on p.InvestProjectId = n.id) pro on pro.RNumber= r.RNumber
#         left join  (
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
#         ) as uclcon on uclcon.conid=c.id
#         left join	(select sl.itemid, sl.Activedate, d.Name
#                         from collect.dbo.StopList sl
#                         inner join collect.dbo.Dictionary d on d.id = sl.ReasonId
#                         where sl.ActiveStopList = 1 and sl.StopDate is null and sl.TypeId = 82 and sl.Pretendent = 0) as stl on stl.ItemId = c.id
#         --безкоштовна перевірка
#         left join (select distinct inn.conID from (select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо') as inn
#           left join SDSD.invest.FreePropertyCheck pc on inn.INN = pc.INN collate Cyrillic_General_CI_AS
#           where pc.PropertyList is not null)as fpc on c.id = fpc.conID
#
#         -- НКС з майном
#         left join (select distinct inn.conID from (select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо') as inn
#           left join SDSD.invest.FreeINNPropertyCheck pc1 on inn.INN = pc1.INN collate Cyrillic_General_CI_AS
#           where pc1.Description is not null)as maino on c.id = maino.conID
#           --Мирна Україна
#           left join (select distinct mu_all.conID from (select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
#         ) as mu_all
#         left join (select t4.INN from (select *,
#         case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
#         and PropertyList not like '85%' and PropertyList not like 'нічого не знайдено' and PropertyList not like 'Невизначене майно' then 'Мирна Україіна'
#         when PropertyList like '14%' then 'Донецька/Луганська обл'
#         when PropertyList like '44%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Автономна%' then 'Крим'
#         when PropertyList like '85%' then 'Крим'
#         else '?' end 'Регіон'
#         from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Мирна Україіна'
#         )as mu on mu_all.INN = mu.INN collate Cyrillic_General_CI_AS
#         where mu.INN is not null)as mu1 on c.id = mu1.conID
#         --АТО
#         left join (select distinct mu_all.conID from (select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
#         ) as mu_all
#         left join (select t4.INN from (select *,
#         case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
#         and PropertyList not like '85%' then 'Мирна Україіна'
#         when PropertyList like '14%' then 'Донецька/Луганська обл'
#         when PropertyList like '44%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Автономна%' then 'Крим'
#         when PropertyList like '85%' then 'Крим'
#         else 'Нічого не знайдено' end 'Регіон'
#         from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Донецька/Луганська обл'
#         )as mu on mu_all.INN = mu.INN collate Cyrillic_General_CI_AS
#         where mu.INN is not null and mu_all.conID not in (select distinct mu_all.conID from (select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
#         ) as mu_all
#         left join (select t4.INN from (select *,
#         case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
#         and PropertyList not like '85%' then 'Мирна Україіна'
#         when PropertyList like '14%' then 'Донецька/Луганська обл'
#         when PropertyList like '44%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
#         when PropertyList like 'Автономна%' then 'Крим'
#         when PropertyList like '85%' then 'Крим'
#         else 'Мирна Україіна' end 'Регіон'
#         from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Мирна Україіна'
#         )as mu on mu_all.INN = mu.INN collate Cyrillic_General_CI_AS
#         where mu.INN is not null))as ato on c.id = ato.conID
#         --Платна перевірка
#         left join ( select distinct ContractId from SDSD.Invest.ContractProperty where PropertyId in (
#         select distinct PropertyId from SDSD.Invest.PropertyCheck )) as pp on c.id = pp.ContractId
#         --майно в іпотеці
#         left join (select distinct ipoteka.conID from (select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
#         ) as ipoteka
#         left join ( Select t2.ClientINN, count(t2.ClientINN) as 'couipt' from (select pr.ClientINN, case when isnull(ob.name, obt.name) is null then 'Доп_майно'
#          else 'Іпотека' end 'Статус_майна'
#          from SDSD.Invest.PropertyRights pr
#          left join (SELECT Main.propertyid,
#                LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
#         FROM
#             (
#                 SELECT DISTINCT ST2.propertyid,
#                     (
#                         SELECT ST1.Name + '--' AS [text()]
#                         FROM (
#                             select mr.propertyid, c.Name
#                                 from SDSD.Invest.MortgageRecord mr
#                                 join SDSD.Invest.Collector c on mr.MortgageeId = c.id
#                                 where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                         ) ST1
#                         WHERE ST1.propertyid = ST2.propertyid
#                         ORDER BY ST1.propertyid
#                         FOR XML PATH ('')
#                     ) [LMDescr]
#                 FROM (
#                     select mr.propertyid, c.Name
#                                 from SDSD.Invest.MortgageRecord mr
#                                 join SDSD.Invest.Collector c on mr.MortgageeId = c.id
#                                 where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                 ) ST2
#             ) [Main]) ob on ob.PropertyId = pr.PropertyId
#         left join (SELECT Main.propertyid,
#                LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
#         FROM
#             (
#                 SELECT DISTINCT ST2.propertyid,
#                     (
#                         SELECT ST1.Name + '--' AS [text()]
#                         FROM (
#                             select en.propertyid, c.Name
#                                 from SDSD.Invest.Encumbrance en
#                                 join SDSD.Invest.Collector c on en.CumbersomeId = c.id
#                                 where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                         ) ST1
#                         WHERE ST1.propertyid = ST2.propertyid
#                         ORDER BY ST1.propertyid
#                         FOR XML PATH ('')
#                     ) [LMDescr]
#                 FROM (
#                     select en.propertyid, c.Name
#                                 from SDSD.Invest.Encumbrance en
#                                 join SDSD.Invest.Collector c on en.CumbersomeId = c.id
#                                 where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                 ) ST2
#             ) [Main]) obt on obt.PropertyId = pr.PropertyId
#          where pr.ClientINN is not null and pr.IsActual = 1 and pr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck) ) as t2 where t2.[Статус_майна] = 'Іпотека'
#          group by  t2.ClientINN) as ipot on ipoteka.INN = ipot.ClientINN collate Cyrillic_General_CI_AS where ipot.ClientINN is not null) as ipo on c.id = ipo.conID
#          --додаткове майно
#          left join (select distinct ipoteka.conID from (select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.Client cl on cl.id=cont.ClientId
#           union all
#           select
#             cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#           from Collect.dbo.Contract cont
#           left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#           left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#             left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#           where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
#         ) as ipoteka
#         left join ( Select t2.ClientINN, count(t2.ClientINN) as 'couipt' from (select pr.ClientINN, case when isnull(ob.name, obt.name) is null then 'Доп_майно'
#          else 'Іпотека' end 'Статус_майна'
#          from SDSD.Invest.PropertyRights pr
#          left join (SELECT Main.propertyid,
#                LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
#         FROM
#             (
#                 SELECT DISTINCT ST2.propertyid,
#                     (
#                         SELECT ST1.Name + '--' AS [text()]
#                         FROM (
#                             select mr.propertyid, c.Name
#                                 from SDSD.Invest.MortgageRecord mr
#                                 join SDSD.Invest.Collector c on mr.MortgageeId = c.id
#                                 where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                         ) ST1
#                         WHERE ST1.propertyid = ST2.propertyid
#                         ORDER BY ST1.propertyid
#                         FOR XML PATH ('')
#                     ) [LMDescr]
#                 FROM (
#                     select mr.propertyid, c.Name
#                                 from SDSD.Invest.MortgageRecord mr
#                                 join SDSD.Invest.Collector c on mr.MortgageeId = c.id
#                                 where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                 ) ST2
#             ) [Main]) ob on ob.PropertyId = pr.PropertyId
#         left join (SELECT Main.propertyid,
#                LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
#         FROM
#             (
#                 SELECT DISTINCT ST2.propertyid,
#                     (
#                         SELECT ST1.Name + '--' AS [text()]
#                         FROM (
#                             select en.propertyid, c.Name
#                                 from SDSD.Invest.Encumbrance en
#                                 join SDSD.Invest.Collector c on en.CumbersomeId = c.id
#                                 where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                         ) ST1
#                         WHERE ST1.propertyid = ST2.propertyid
#                         ORDER BY ST1.propertyid
#                         FOR XML PATH ('')
#                     ) [LMDescr]
#                 FROM (
#                     select en.propertyid, c.Name
#                                 from SDSD.Invest.Encumbrance en
#                                 join SDSD.Invest.Collector c on en.CumbersomeId = c.id
#                                 where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
#                 ) ST2
#             ) [Main]) obt on obt.PropertyId = pr.PropertyId
#          where pr.ClientINN is not null and pr.IsActual = 1 and pr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck) ) as t2 where t2.[Статус_майна] = 'Доп_майно'
#          group by  t2.ClientINN) as ipot on ipoteka.INN = ipot.ClientINN collate Cyrillic_General_CI_AS where ipot.ClientINN is not null)as adp on c.id = adp.conID
#          --діючі ВД
#          left join (select distinct	cc.ContractId	AS	[NKS]
#         from [10.1.32.64].[LegalCollection].[dbo].[b_Document]					d
#         left join [Collect].dbo.Dictionary							ddoc		on	ddoc.id = d.TypeId
#         left join [Collect].dbo.Dictionary							ddoc2		on	ddoc2.id = d.SubtypeId
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_Claim]					clm			on	d.id = clm.[BDocumentId]
#         left join [Collect].dbo.Dictionary							dicclm		on	dicclm.id = clm.ClaimTypeId
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_ContractClaim]			cc			on	cc.ClaimId = clm.Id
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_PersonClaim]			pc			on	pc.ClaimId = clm.Id
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_DebtClaim]				dclm		on	dclm.ClaimId = clm.Id
#         left join [Collect].dbo.Currency							curr		on	curr.id = dclm.CurrencyId
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_ExecutiveDocument]		ed			on	ed.BDocumentId = d.Id
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_DocumentLawsuit]		dls			on	dls.BDocumentId = d.Id
#         where ed.Term	>= GETDATE() ) as vd_all on  uclcon.conID = vd_all.NKS
#         --Вд зі стороною
#         left join (Select distinct vl2.NKS  from (select
#             d.Id
#         ,	ddoc.name															as	[Тип документу]
#         ,	ddoc2.name															as	[Підтип документу]
#         ,	convert(nvarchar(max),d.docname	)									as	[Номер/Назва ВД]
#         ,	d.docdate															as	[Дата видачі ВД]
#         ,	d.documentlinkid													as	[Посилання на документ] --на документ онлайн
#         ,	d.note																as	[Коментар]
#         ,	d.importdate														as	[Дата загрузки]
#         ,	dicclm.Name															as	[Тип стягування]
#         ,	dclm.[Sum]															as	[Cума боргу]
#         ,	curr.CurrCode														AS	[Валюта]
#         ,	ed.Term																as	[Строк подачі]
#         ,	pc.INN																AS	[INN]
#         ,	cc.ContractId														as	[NKS]
#         ,  convert(nvarchar(max), cc.ContractId) + '_' +  convert(nvarchar(max), pc.INN)as 'vduniq'
#         ,case when  isnull(zam1.zam, zam2.number ) is null then 0
#         else 1 end as 'zamena'
#         from [10.1.32.64].[LegalCollection].[dbo].[b_Document]					d
#         left join [Collect].dbo.Dictionary							ddoc		on	ddoc.id = d.TypeId
#         left join [Collect].dbo.Dictionary							ddoc2		on	ddoc2.id = d.SubtypeId
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_Claim]					clm			on	d.id = clm.[BDocumentId]
#         left join [Collect].dbo.Dictionary							dicclm		on	dicclm.id = clm.ClaimTypeId
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_ContractClaim]			cc			on	cc.ClaimId = clm.Id
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_PersonClaim]			pc			on	pc.ClaimId = clm.Id
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_DebtClaim]				dclm		on	dclm.ClaimId = clm.Id
#         left join [Collect].dbo.Currency							curr		on	curr.id = dclm.CurrencyId
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_ExecutiveDocument]		ed			on	ed.BDocumentId = d.Id
#         left join [10.1.32.64].[LegalCollection].[dbo].[b_DocumentLawsuit]		dls			on	dls.BDocumentId = d.Id
#         left join (select distinct convert(nvarchar(max), zam.CaseNamber) as 'zam' from (select c.id as 'НКС', leg.CaseNamber,
#                leg.EventDate as 'EventDate', leg.ReceiptDate,  leg.EventType,
#                et.Name as 'EventName', etr.Name as 'RootName'
#         from collect.dbo.reestr r
#         join Collect.dbo.Contragent cn on cn.id = r.ContragentId
#         join collect.dbo.contract c on c.reestrId = r.id
#         join [10.1.32.64].legalcollection.property.collectiongroup cgp on c.id = cgp.ContractID
#         join collect.dbo.client cl on cl.id = c.clientId
#         left join [10.1.32.64].LegalCollection.dbo.contract lc on lc.contractId = c.id
#         left join ( select ls.Number as 'CaseNamber', ev.EventTypeId as 'EventType',  lwc.contractSuitId,  ev.id as 'EventId',
#                     ev.eventDate, ev.receiptDate, ev.typerootId, ev.eventTypeId
#                     from [10.1.32.64].LegalCollection.dbo.LawContract lwc
#                     join [10.1.32.64].LegalCollection.dbo.LawSuit ls on lwc.LawSuitId = ls.id
#                     left join [10.1.32.64].LegalCollection.dbo.event ev on ev.SuitId = ls.id
#                     ) as leg on leg.contractSuitId = lc.id
#         left join [10.1.32.64].LegalCollection.dbo.EventType et on et.id = leg.EventTypeId
#         left join [10.1.32.64].LegalCollection.dbo.EventType etR on et.rootId = etR.id
#         where  --cgp.Name in ( 'Ипотека_Алексей', 'Ипотека_Алёна')    and
#         leg.EventType in (102,	120,	147,	192,	486,	488,	490,	636,	638,	643,	644,	654,	655)) zam )as zam1 on convert(nvarchar(max), d.docname)	= zam1.zam
#         left join (select distinct ls.number from [10.1.32.64].LegalCollection.dbo.LawSuit ls
#         left join [10.1.32.64].LegalCollection.dbo.Client c on ls.Plaintiffid = c.id
#         where c.id in (4899	,
#         63	,
#         113185	,
#         259623	,
#         104116	,
#         341492	,
#         80609	,
#         80612	,
#         81062	,
#         81094	,
#         81096	,
#         25694	,
#         81047	,
#         81060	,
#         80610	,
#         80611	,
#         81061	,
#         81063	,
#         81095	,
#         81097	,
#         80599	,
#         80601	,
#         80603	,
#         25695	,
#         80606	,
#         80613	,
#         81051	,
#         81092	,
#         81099	,
#         25697	,
#         259430	,
#         80602	,
#         80604	,
#         81052	,
#         81087	,
#         81088	,
#         85616	,
#         80608	,
#         81049	,
#         81056	,
#         81058	,
#         81065	,
#         81067	,
#         81090	,
#         104122	,
#         81054	,
#         81055	,
#         81068	,
#         81070	,
#         85617	,
#         81089	,
#         81091	,
#         81093	,
#         81098	,
#         81100	,
#         94037	,
#         80600	,
#         80607	,
#         80614	,
#         81050	,
#         81057	,
#         81059	,
#         81064	,
#         81066	,
#         25696	,
#         81053	,
#         81069	,
#         81071	,
#         85618	,
#         80138	,
#         80147	,
#         80154	,
#         104120	,
#         81699	,
#         80141	,
#         80159	,
#         104118	,
#         81648	,
#         81697	,
#         80131	,
#         80156	,
#         80129	,
#         80140	,
#         80145	,
#         80163	,
#         80165	,
#         105412	,
#         81583	,
#         81585	,
#         81592	,
#         81649	,
#         81708	,
#         81710	,
#         81694	,
#         81701	,
#         81703	,
#         80158	,
#         80160	,
#         80161	,
#         80130	,
#         80155	,
#         81582	,
#         81650	,
#         81691	,
#         81693	,
#         81702	,
#         81711	,
#         22792	,
#         80133	,
#         80150	,
#         80151	,
#         81589	,
#         81590	,
#         81705	,
#         81707	,
#         80136	,
#         80149	,
#         80152	,
#         81587	,
#         81588	,
#         81704	,
#         81580	,
#         81581	,
#         81647	,
#         81695	,
#         81698	,
#         81712	,
#         81715	,
#         80132	,
#         80137	,
#         80139	,
#         80157	,
#         80162	,
#         80164	,
#         81700	,
#         81709	,
#         104124	,
#         80142	,
#         80143	,
#         80144	,
#         81646	,
#         81696	,
#         81713	,
#         81714	,
#         80135	,
#         80166	,
#         81706	,
#         81722	,
#         81723	,
#         80605	,
#         81048	,
#         80146	,
#         80153	,
#         81584	,
#         81586	,
#         81591	))as zam2 on convert(nvarchar(max), d.docname)	= zam2.number
#         where ed.Term	>= GETDATE() and case when  isnull(zam1.zam, zam2.number ) is null then 0 else 1 end >=1)as vl2)as zam_all on  uclcon.conID = zam_all.NKS
#          where (stl.Name is null or stl.Name = 'В работе Залогов') and r.IsActual = 1 and r.TypeId = 632263  '''
# psql.read_sql(requestString, connection)
# df = pd.read_gbq(requestString, dialect='standard')

# df = pd.read_sql(requestString, connection)
# dbCursor.execute(requestString).fetchall()

# psql.sqldf(requestString)
# table = df.groupby('Сегмент боргу').agg({'INN': ['count']})
# table['sum'] = table.sum(axis=1)
# table['sum'].fillna(0, inplace=True)
# print(table)

import streamlit as st
import inputing
import numpy as np
import plotly.graph_objs as go
from pandas.api.types import CategoricalDtype
# dbCursor = inputing.dbCursor()

# requestString = """ select distinct uclcon.INN ,
# case when borg.sum_borg < 30000 then '0 - 30 000'
# when borg.sum_borg < 50000 then '30 000 - 50 000'
# when borg.sum_borg < 100000 then '50 000 - 100 000'
# when borg.sum_borg < 250000 then '100 000 - 250 000'
# when borg.sum_borg < 500000 then '250 000 - 500 000'
# else '500 000+' end as 'Сегмент боргу',
# case when  uclcon.INN = '0000000000' then 0
# when len(uclcon.INN) = 10 then 1
# when len(uclcon.INN) = 8 then 1
# else 0 end as 'К-ть правильних ІПН',
# case when pc.PropertyList is null then '0'
# else '1' end as 'К-ть перевірених ІПН по безкоштовній перевірці',
# case when cou.Count1 >=1 then 1
# else 0 end as 'К-ть ІПН з майном по безкоштовній перевірці',
# case when mu.kt >=1 then 1
# else  0 end as ' К-ть ІПН з майном на Мирній Україні',
# case when  ato.kt>=1 then 1
# else  0 end as 'К-ть в Донецька/Луганська обл',
# case when pp.inn is null then 0 else 1 end 'К-ть завантажених ІПН з платною перевіркою за адресою',
# case when ipot.couipt >= 1 then 1
# else 0 end as 'К-ть ІПН з майном в іпотеці' ,
# case when ad.couipt >= 1 then 1
# else 0 end as 'К-ть ІПН з додатковим майном' ,
# case when vd_all.INN is null then 0
# else  1 end 'К-ть ІПН з діючим ВД',
# case when zam_all.INN is null then 0
# else  1 end 'К-ть ІПН з  діючим ВД та заміненою стороною'
# from Collect.dbo.reestr r
# inner join collect.dbo.contract c on c.ReestrId = r.id
# left join  (
#   select
#     cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#   from Collect.dbo.Contract cont
#   left join Collect.dbo.Client cl on cl.id=cont.ClientId
#   union all
#   select
#     cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#   from Collect.dbo.Contract cont
#   left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#   left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#     left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#   where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
# ) as uclcon on uclcon.conid=c.id
# left join	(select sl.itemid, sl.Activedate, d.Name
# 				from collect.dbo.StopList sl
# 				inner join collect.dbo.Dictionary d on d.id = sl.ReasonId
# 				where sl.ActiveStopList = 1 and sl.StopDate is null and sl.TypeId = 82 and sl.Pretendent = 0) as stl on stl.ItemId = c.id
# left join SDSD.invest.FreePropertyCheck pc on uclcon.INN = pc.INN collate Cyrillic_General_CI_AS
# left join (select inn, count (INN) as 'Count1' from SDSD.invest.FreeINNPropertyCheck group by INN) as cou on uclcon.INN = cou.INN collate Cyrillic_General_CI_AS
#
# --Мирна Україна
# left join (select t4.INN, count(t4.INN)as 'kt' from (select *,
# case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
# and PropertyList not like '85%' and PropertyList not like 'нічого не знайдено' and PropertyList not like 'Невизначене майно' then 'Мирна Україіна'
# when PropertyList like '14%' then 'Донецька/Луганська обл'
# when PropertyList like '44%' then 'Донецька/Луганська обл'
# when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
# when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
# when PropertyList like 'Автономна%' then 'Крим'
# when PropertyList like '85%' then 'Крим'
# else '?' end 'Регіон'
# from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Мирна Україіна'
# group by t4.INN)as mu on uclcon.INN = mu.INN collate Cyrillic_General_CI_AS
# --ATO
# left join (select t3.INN, count(t3.INN)as 'kt' from (select *,
# case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
# and PropertyList not like '85%' and PropertyList not like 'нічого не знайдено' and PropertyList not like 'Невизначене майно' then 'Мирна Україіна'
# when PropertyList like '14%' then 'Донецька/Луганська обл'
# when PropertyList like '44%' then 'Донецька/Луганська обл'
# when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
# when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
# when PropertyList like 'Автономна%' then 'Крим'
# when PropertyList like '85%' then 'Крим'
# else '?' end 'Регіон'
# from SDSD.Invest.FreePropertyCheck ) as t3 where t3.Регіон = 'Донецька/Луганська обл'
# and t3.INN not in (select t4.INN from (select *,
# case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
# and PropertyList not like '85%' and PropertyList not like 'нічого не знайдено' and PropertyList not like 'Невизначене майно' then 'Мирна Україіна'
# when PropertyList like '14%' then 'Донецька/Луганська обл'
# when PropertyList like '44%' then 'Донецька/Луганська обл'
# when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
# when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
# when PropertyList like 'Автономна%' then 'Крим'
# when PropertyList like '85%' then 'Крим'
# else '?' end 'Регіон'
# from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Мирна Україіна'
# group by t4.INN)
# group by t3.INN)as ato on uclcon.INN = ato.INN collate Cyrillic_General_CI_AS
#
#
# -- платна перевірка
# left join (Select distinct inn from (select distinct contractid, uclcon.INN from ( select * from SDSD.Invest.ContractProperty where PropertyId in (
# select distinct PropertyId from SDSD.Invest.PropertyCheck )) as t1
# left join  (
#   select
#     cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#   from Collect.dbo.Contract cont
#   left join Collect.dbo.Client cl on cl.id=cont.ClientId
#   union all
#   select
#     cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#   from Collect.dbo.Contract cont
#   left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#   left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#     left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#   where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
# ) as uclcon on uclcon.conid = t1.ContractId)t2)as pp  on uclcon.INN = pp.INN collate Cyrillic_General_CI_AS
# left join ( Select t2.ClientINN, count(t2.ClientINN) as 'couipt' from (select pr.ClientINN, case when isnull(ob.name, obt.name) is null then 'Доп_майно'
#  else 'Іпотека' end 'Статус_майна'
#  from SDSD.Invest.PropertyRights pr
#  left join (SELECT Main.propertyid,
#        LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
# FROM
#     (
#         SELECT DISTINCT ST2.propertyid,
#             (
#                 SELECT ST1.Name + '--' AS [text()]
#                 FROM (
# 					select mr.propertyid, c.Name
# 						from SDSD.Invest.MortgageRecord mr
# 						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
# 						where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 				) ST1
#                 WHERE ST1.propertyid = ST2.propertyid
#                 ORDER BY ST1.propertyid
#                 FOR XML PATH ('')
#             ) [LMDescr]
#         FROM (
# 			select mr.propertyid, c.Name
# 						from SDSD.Invest.MortgageRecord mr
# 						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
# 						where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 		) ST2
#     ) [Main]) ob on ob.PropertyId = pr.PropertyId
# left join (SELECT Main.propertyid,
#        LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
# FROM
#     (
#         SELECT DISTINCT ST2.propertyid,
#             (
#                 SELECT ST1.Name + '--' AS [text()]
#                 FROM (
# 					select en.propertyid, c.Name
# 						from SDSD.Invest.Encumbrance en
# 						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
# 						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 				) ST1
#                 WHERE ST1.propertyid = ST2.propertyid
#                 ORDER BY ST1.propertyid
#                 FOR XML PATH ('')
#             ) [LMDescr]
#         FROM (
# 			select en.propertyid, c.Name
# 						from SDSD.Invest.Encumbrance en
# 						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
# 						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 		) ST2
#     ) [Main]) obt on obt.PropertyId = pr.PropertyId
#  where pr.ClientINN is not null and pr.IsActual = 1 and pr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck) ) as t2 where t2.[Статус_майна] = 'Іпотека'
#  group by  t2.ClientINN) as ipot on uclcon.INN = ipot.ClientINN collate Cyrillic_General_CI_AS
# --додаткове майно
#  left join ( Select t2.ClientINN, count(t2.ClientINN) as 'couipt' from (select pr.ClientINN, case when isnull(ob.name, obt.name) is null then 'Доп_майно'
#  else 'Іпотека' end 'Статус_майна'
#  from SDSD.Invest.PropertyRights pr
#  left join (SELECT Main.propertyid,
#        LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
# FROM
#     (
#         SELECT DISTINCT ST2.propertyid,
#             (
#                 SELECT ST1.Name + '--' AS [text()]
#                 FROM (
# 					select mr.propertyid, c.Name
# 						from SDSD.Invest.MortgageRecord mr
# 						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
# 						where   IsActual = 1  and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 				) ST1
#                 WHERE ST1.propertyid = ST2.propertyid
#                 ORDER BY ST1.propertyid
#                 FOR XML PATH ('')
#             ) [LMDescr]
#         FROM (
# 			select mr.propertyid, c.Name
# 						from SDSD.Invest.MortgageRecord mr
# 						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
# 						where   IsActual = 1  and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 		) ST2
#     ) [Main]) ob on ob.PropertyId = pr.PropertyId
# left join (SELECT Main.propertyid,
#        LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
# FROM
#     (
#         SELECT DISTINCT ST2.propertyid,
#             (
#                 SELECT ST1.Name + '--' AS [text()]
#                 FROM (
# 					select en.propertyid, c.Name
# 						from SDSD.Invest.Encumbrance en
# 						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
# 						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 				) ST1
#                 WHERE ST1.propertyid = ST2.propertyid
#                 ORDER BY ST1.propertyid
#                 FOR XML PATH ('')
#             ) [LMDescr]
#         FROM (
# 			select en.propertyid, c.Name
# 						from SDSD.Invest.Encumbrance en
# 						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
# 						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
# 		) ST2
#     ) [Main]) obt on obt.PropertyId = pr.PropertyId
#  where ClientINN is not null and IsActual = 1 and pr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)) as t2 where t2.[Статус_майна] = 'Доп_майно'
#  group by  t2.ClientINN) as ad on uclcon.INN = ad.ClientINN collate Cyrillic_General_CI_AS
# left join (select uclcon.INN, sum(case when c.CurrencyId = 8 then SummToClose * 1
# when c.CurrencyId = 9 then SummToClose * 27.2
# when c.CurrencyId = 10 then SummToClose * 31.45
# when c.CurrencyId = 19 then SummToClose * 29.32
# else SummToClose * 1 end ) as 'sum_borg' from Collect.dbo.reestr r
# inner join collect.dbo.contract c on c.ReestrId = r.id
# left join  (
#   select
#     cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
#   from Collect.dbo.Contract cont
#   left join Collect.dbo.Client cl on cl.id=cont.ClientId
#   union all
#   select
#     cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
#   from Collect.dbo.Contract cont
#   left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
#   left join Collect.dbo.Client cl on cl.id=clcon.ClientId
#     left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
#   where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
# ) as uclcon on uclcon.conid=c.id
# left join	(select sl.itemid, sl.Activedate, d.Name
# 				from collect.dbo.StopList sl
# 				inner join collect.dbo.Dictionary d on d.id = sl.ReasonId
# 				where sl.ActiveStopList = 1 and sl.StopDate is null and sl.TypeId = 82 and sl.Pretendent = 0) as stl on stl.ItemId = c.id
# where (stl.Name is null or stl.Name = 'В работе Залогов') and r.IsActual = 1 and r.TypeId = 632263
# group by uclcon.INN)as borg on borg.INN = uclcon.INN
# -- діючі ВД
# left join (select distinct	pc.INN	AS	[INN]
# from [10.1.32.64].[LegalCollection].[dbo].[b_Document]					d
# left join [Collect].dbo.Dictionary							ddoc		on	ddoc.id = d.TypeId
# left join [Collect].dbo.Dictionary							ddoc2		on	ddoc2.id = d.SubtypeId
# left join [10.1.32.64].[LegalCollection].[dbo].[b_Claim]					clm			on	d.id = clm.[BDocumentId]
# left join [Collect].dbo.Dictionary							dicclm		on	dicclm.id = clm.ClaimTypeId
# left join [10.1.32.64].[LegalCollection].[dbo].[b_ContractClaim]			cc			on	cc.ClaimId = clm.Id
# left join [10.1.32.64].[LegalCollection].[dbo].[b_PersonClaim]			pc			on	pc.ClaimId = clm.Id
# left join [10.1.32.64].[LegalCollection].[dbo].[b_DebtClaim]				dclm		on	dclm.ClaimId = clm.Id
# left join [Collect].dbo.Currency							curr		on	curr.id = dclm.CurrencyId
# left join [10.1.32.64].[LegalCollection].[dbo].[b_ExecutiveDocument]		ed			on	ed.BDocumentId = d.Id
# left join [10.1.32.64].[LegalCollection].[dbo].[b_DocumentLawsuit]		dls			on	dls.BDocumentId = d.Id
# where ed.Term	>= GETDATE() ) as vd_all on  uclcon.INN = vd_all.inn collate Cyrillic_General_CI_AS
# -- замінена сторона в діючих
# left join (Select distinct vl2.INN from (select
# 	d.Id
# ,	ddoc.name															as	[Тип документу]
# ,	ddoc2.name															as	[Підтип документу]
# ,	convert(nvarchar(max),d.docname	)									as	[Номер/Назва ВД]
# ,	d.docdate															as	[Дата видачі ВД]
# ,	d.documentlinkid													as	[Посилання на документ] --на документ онлайн
# ,	d.note																as	[Коментар]
# ,	d.importdate														as	[Дата загрузки]
# ,	dicclm.Name															as	[Тип стягування]
# ,	dclm.[Sum]															as	[Cума боргу]
# ,	curr.CurrCode														AS	[Валюта]
# ,	ed.Term																as	[Строк подачі]
# ,	pc.INN																AS	[INN]
# ,	cc.ContractId														as	[НКС]
# ,  convert(nvarchar(max), cc.ContractId) + '_' +  convert(nvarchar(max), pc.INN)as 'vduniq'
# ,case when  isnull(zam1.zam, zam2.number ) is null then 0
# else 1 end as 'zamena'
# from [10.1.32.64].[LegalCollection].[dbo].[b_Document]					d
# left join [Collect].dbo.Dictionary							ddoc		on	ddoc.id = d.TypeId
# left join [Collect].dbo.Dictionary							ddoc2		on	ddoc2.id = d.SubtypeId
# left join [10.1.32.64].[LegalCollection].[dbo].[b_Claim]					clm			on	d.id = clm.[BDocumentId]
# left join [Collect].dbo.Dictionary							dicclm		on	dicclm.id = clm.ClaimTypeId
# left join [10.1.32.64].[LegalCollection].[dbo].[b_ContractClaim]			cc			on	cc.ClaimId = clm.Id
# left join [10.1.32.64].[LegalCollection].[dbo].[b_PersonClaim]			pc			on	pc.ClaimId = clm.Id
# left join [10.1.32.64].[LegalCollection].[dbo].[b_DebtClaim]				dclm		on	dclm.ClaimId = clm.Id
# left join [Collect].dbo.Currency							curr		on	curr.id = dclm.CurrencyId
# left join [10.1.32.64].[LegalCollection].[dbo].[b_ExecutiveDocument]		ed			on	ed.BDocumentId = d.Id
# left join [10.1.32.64].[LegalCollection].[dbo].[b_DocumentLawsuit]		dls			on	dls.BDocumentId = d.Id
# left join (select distinct convert(nvarchar(max), zam.CaseNamber) as 'zam' from (select c.id as 'НКС', leg.CaseNamber,
# 	   leg.EventDate as 'EventDate', leg.ReceiptDate,  leg.EventType,
# 	   et.Name as 'EventName', etr.Name as 'RootName'
# from collect.dbo.reestr r
# join Collect.dbo.Contragent cn on cn.id = r.ContragentId
# join collect.dbo.contract c on c.reestrId = r.id
# join [10.1.32.64].legalcollection.property.collectiongroup cgp on c.id = cgp.ContractID
# join collect.dbo.client cl on cl.id = c.clientId
# left join [10.1.32.64].LegalCollection.dbo.contract lc on lc.contractId = c.id
# left join ( select ls.Number as 'CaseNamber', ev.EventTypeId as 'EventType',  lwc.contractSuitId,  ev.id as 'EventId',
# 		    ev.eventDate, ev.receiptDate, ev.typerootId, ev.eventTypeId
# 			from [10.1.32.64].LegalCollection.dbo.LawContract lwc
# 			join [10.1.32.64].LegalCollection.dbo.LawSuit ls on lwc.LawSuitId = ls.id
# 			left join [10.1.32.64].LegalCollection.dbo.event ev on ev.SuitId = ls.id
# 			) as leg on leg.contractSuitId = lc.id
# left join [10.1.32.64].LegalCollection.dbo.EventType et on et.id = leg.EventTypeId
# left join [10.1.32.64].LegalCollection.dbo.EventType etR on et.rootId = etR.id
# where  --cgp.Name in ( 'Ипотека_Алексей', 'Ипотека_Алёна')    and
# leg.EventType in (102,	120,	147,	192,	486,	488,	490,	636,	638,	643,	644,	654,	655)) zam )as zam1 on convert(nvarchar(max), d.docname)	= zam1.zam
# left join (select distinct ls.number from [10.1.32.64].LegalCollection.dbo.LawSuit ls
# left join [10.1.32.64].LegalCollection.dbo.Client c on ls.Plaintiffid = c.id
# where c.id in (4899	,
# 63	,
# 113185	,
# 259623	,
# 104116	,
# 341492	,
# 80609	,
# 80612	,
# 81062	,
# 81094	,
# 81096	,
# 25694	,
# 81047	,
# 81060	,
# 80610	,
# 80611	,
# 81061	,
# 81063	,
# 81095	,
# 81097	,
# 80599	,
# 80601	,
# 80603	,
# 25695	,
# 80606	,
# 80613	,
# 81051	,
# 81092	,
# 81099	,
# 25697	,
# 259430	,
# 80602	,
# 80604	,
# 81052	,
# 81087	,
# 81088	,
# 85616	,
# 80608	,
# 81049	,
# 81056	,
# 81058	,
# 81065	,
# 81067	,
# 81090	,
# 104122	,
# 81054	,
# 81055	,
# 81068	,
# 81070	,
# 85617	,
# 81089	,
# 81091	,
# 81093	,
# 81098	,
# 81100	,
# 94037	,
# 80600	,
# 80607	,
# 80614	,
# 81050	,
# 81057	,
# 81059	,
# 81064	,
# 81066	,
# 25696	,
# 81053	,
# 81069	,
# 81071	,
# 85618	,
# 80138	,
# 80147	,
# 80154	,
# 104120	,
# 81699	,
# 80141	,
# 80159	,
# 104118	,
# 81648	,
# 81697	,
# 80131	,
# 80156	,
# 80129	,
# 80140	,
# 80145	,
# 80163	,
# 80165	,
# 105412	,
# 81583	,
# 81585	,
# 81592	,
# 81649	,
# 81708	,
# 81710	,
# 81694	,
# 81701	,
# 81703	,
# 80158	,
# 80160	,
# 80161	,
# 80130	,
# 80155	,
# 81582	,
# 81650	,
# 81691	,
# 81693	,
# 81702	,
# 81711	,
# 22792	,
# 80133	,
# 80150	,
# 80151	,
# 81589	,
# 81590	,
# 81705	,
# 81707	,
# 80136	,
# 80149	,
# 80152	,
# 81587	,
# 81588	,
# 81704	,
# 81580	,
# 81581	,
# 81647	,
# 81695	,
# 81698	,
# 81712	,
# 81715	,
# 80132	,
# 80137	,
# 80139	,
# 80157	,
# 80162	,
# 80164	,
# 81700	,
# 81709	,
# 104124	,
# 80142	,
# 80143	,
# 80144	,
# 81646	,
# 81696	,
# 81713	,
# 81714	,
# 80135	,
# 80166	,
# 81706	,
# 81722	,
# 81723	,
# 80605	,
# 81048	,
# 80146	,
# 80153	,
# 81584	,
# 81586	,
# 81591	))as zam2 on convert(nvarchar(max), d.docname)	= zam2.number
# where ed.Term	>= GETDATE() and case when  isnull(zam1.zam, zam2.number ) is null then 0 else 1 end >=1)as vl2)as zam_all on  uclcon.INN = zam_all.INN collate Cyrillic_General_CI_AS
# where (stl.Name is null or stl.Name = 'В работе Залогов') and r.IsActual = 1 and r.TypeId = 632263 and uclcon.INN <> '' """
#
# df = pd.read_sql_query(requestString, inputing.getConnection())
# dbCursor.execute(requestString).fetchall()
#
#
# cat_size_order = CategoricalDtype(
#     ['0 - 30 000', '30 000 - 50 000', '50 000 - 100 000','100 000 - 250 000',
#                              '250 000 - 500 000', '500 000+'],
#     ordered=True
# )
# df['К-ть ІПН з діючим ВД'] = df['К-ть ІПН з діючим ВД'].astype(str, errors = 'raise')
# df.sort_values('Сегмент боргу')
# values=['INN','К-ть правильних ІПН']
#
# df['К-ть ІПН з діючим ВД'] = pd.to_numeric(df['К-ть ІПН з діючим ВД'])
#
# pivot_segment = pd.pivot_table(df, index=['Сегмент боргу'], values=values,
#                        aggfunc={'INN': 'count',
#                                 'К-ть правильних ІПН': np.sum
#                                 }, margins = True, dropna = True, margins_name = 'All', observed = False)
#
# st.write(pivot_segment)

import sys
import pyodbc
import pandas as pd
from itertools import zip_longest
import inputing
from matplotlib import pyplot as plt
from pandas.api.types import CategoricalDtype
import plotly.express as px
global df
sys.setrecursionlimit(5000)

dbCursor = inputing.dbCursor()

requestString = """ select distinct uclcon.INN ,
case when borg.sum_borg < 30000 then '0 - 30 000'
when borg.sum_borg < 50000 then '30 000 - 50 000'
when borg.sum_borg < 100000 then '50 000 - 100 000'
when borg.sum_borg < 250000 then '100 000 - 250 000'
when borg.sum_borg < 500000 then '250 000 - 500 000'
else '500 000+' end as 'Сегмент боргу',
case when  uclcon.INN = '0000000000' then 0
when len(uclcon.INN) = 10 then 1
when len(uclcon.INN) = 8 then 1
else 0 end as 'К-ть правильних ІПН',
case when pc.PropertyList is null then '0'
else '1' end as 'К-ть перевірених ІПН по безкоштовній перевірці',
case when cou.Count1 >=1 then 1
else 0 end as 'К-ть ІПН з майном по безкоштовній перевірці',
case when mu.kt >=1 then 1
else  0 end as ' К-ть ІПН з майном на Мирній Україні',
case when  ato.kt>=1 then 1
else  0 end as 'К-ть в Донецька/Луганська обл',
case when pp.inn is null then 0 else 1 end 'К-ть завантажених ІПН з платною перевіркою за адресою',
case when ipot.couipt >= 1 then 1
else 0 end as 'К-ть ІПН з майном в іпотеці' ,
case when ad.couipt >= 1 then 1
else 0 end as 'К-ть ІПН з додатковим майном' ,
case when vd_all.INN is null then 0
else  1 end 'К-ть ІПН з діючим ВД',
case when zam_all.INN is null then 0
else  1 end 'К-ть ІПН з  діючим ВД та заміненою стороною'
from Collect.dbo.reestr r
inner join collect.dbo.contract c on c.ReestrId = r.id
left join  (
  select
    cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.Client cl on cl.id=cont.ClientId
  union all
  select
    cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
  left join Collect.dbo.Client cl on cl.id=clcon.ClientId
    left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
  where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
) as uclcon on uclcon.conid=c.id
left join	(select sl.itemid, sl.Activedate, d.Name
				from collect.dbo.StopList sl
				inner join collect.dbo.Dictionary d on d.id = sl.ReasonId
				where sl.ActiveStopList = 1 and sl.StopDate is null and sl.TypeId = 82 and sl.Pretendent = 0) as stl on stl.ItemId = c.id
left join SDSD.invest.FreePropertyCheck pc on uclcon.INN = pc.INN collate Cyrillic_General_CI_AS
left join (select inn, count (INN) as 'Count1' from SDSD.invest.FreeINNPropertyCheck group by INN) as cou on uclcon.INN = cou.INN collate Cyrillic_General_CI_AS

--Мирна Україна
left join (select t4.INN, count(t4.INN)as 'kt' from (select *,
case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
and PropertyList not like '85%' and PropertyList not like 'нічого не знайдено' and PropertyList not like 'Невизначене майно' then 'Мирна Україіна'
when PropertyList like '14%' then 'Донецька/Луганська обл'
when PropertyList like '44%' then 'Донецька/Луганська обл'
when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
when PropertyList like 'Автономна%' then 'Крим'
when PropertyList like '85%' then 'Крим'
else '?' end 'Регіон'
from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Мирна Україіна'
group by t4.INN)as mu on uclcon.INN = mu.INN collate Cyrillic_General_CI_AS
--ATO
left join (select t3.INN, count(t3.INN)as 'kt' from (select *,
case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
and PropertyList not like '85%' and PropertyList not like 'нічого не знайдено' and PropertyList not like 'Невизначене майно' then 'Мирна Україіна'
when PropertyList like '14%' then 'Донецька/Луганська обл'
when PropertyList like '44%' then 'Донецька/Луганська обл'
when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
when PropertyList like 'Автономна%' then 'Крим'
when PropertyList like '85%' then 'Крим'
else '?' end 'Регіон'
from SDSD.Invest.FreePropertyCheck ) as t3 where t3.Регіон = 'Донецька/Луганська обл'
and t3.INN not in (select t4.INN from (select *,
case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%'
and PropertyList not like '85%' and PropertyList not like 'нічого не знайдено' and PropertyList not like 'Невизначене майно' then 'Мирна Україіна'
when PropertyList like '14%' then 'Донецька/Луганська обл'
when PropertyList like '44%' then 'Донецька/Луганська обл'
when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
when PropertyList like 'Автономна%' then 'Крим'
when PropertyList like '85%' then 'Крим'
else '?' end 'Регіон'
from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Мирна Україіна'
group by t4.INN)
group by t3.INN)as ato on uclcon.INN = ato.INN collate Cyrillic_General_CI_AS


-- платна перевірка
left join (Select distinct inn from (select distinct contractid, uclcon.INN from ( select * from SDSD.Invest.ContractProperty where PropertyId in (
select distinct PropertyId from SDSD.Invest.PropertyCheck )) as t1
left join  (
  select
    cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.Client cl on cl.id=cont.ClientId
  union all
  select
    cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
  left join Collect.dbo.Client cl on cl.id=clcon.ClientId
    left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
  where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
) as uclcon on uclcon.conid = t1.ContractId)t2)as pp  on uclcon.INN = pp.INN collate Cyrillic_General_CI_AS
left join ( Select t2.ClientINN, count(t2.ClientINN) as 'couipt' from (select pr.ClientINN, case when isnull(ob.name, obt.name) is null then 'Доп_майно'
 else 'Іпотека' end 'Статус_майна'
 from SDSD.Invest.PropertyRights pr
 left join (SELECT Main.propertyid,
       LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
FROM
    (
        SELECT DISTINCT ST2.propertyid,
            (
                SELECT ST1.Name + '--' AS [text()]
                FROM (
					select mr.propertyid, c.Name
						from SDSD.Invest.MortgageRecord mr
						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
						where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
				) ST1
                WHERE ST1.propertyid = ST2.propertyid
                ORDER BY ST1.propertyid
                FOR XML PATH ('')
            ) [LMDescr]
        FROM (
			select mr.propertyid, c.Name
						from SDSD.Invest.MortgageRecord mr
						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
						where   IsActual = 1 and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
		) ST2
    ) [Main]) ob on ob.PropertyId = pr.PropertyId
left join (SELECT Main.propertyid,
       LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
FROM
    (
        SELECT DISTINCT ST2.propertyid,
            (
                SELECT ST1.Name + '--' AS [text()]
                FROM (
					select en.propertyid, c.Name
						from SDSD.Invest.Encumbrance en
						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
				) ST1
                WHERE ST1.propertyid = ST2.propertyid
                ORDER BY ST1.propertyid
                FOR XML PATH ('')
            ) [LMDescr]
        FROM (
			select en.propertyid, c.Name
						from SDSD.Invest.Encumbrance en
						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
		) ST2
    ) [Main]) obt on obt.PropertyId = pr.PropertyId
 where pr.ClientINN is not null and pr.IsActual = 1 and pr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck) ) as t2 where t2.[Статус_майна] = 'Іпотека'
 group by  t2.ClientINN) as ipot on uclcon.INN = ipot.ClientINN collate Cyrillic_General_CI_AS
--додаткове майно
 left join ( Select t2.ClientINN, count(t2.ClientINN) as 'couipt' from (select pr.ClientINN, case when isnull(ob.name, obt.name) is null then 'Доп_майно'
 else 'Іпотека' end 'Статус_майна'
 from SDSD.Invest.PropertyRights pr
 left join (SELECT Main.propertyid,
       LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
FROM
    (
        SELECT DISTINCT ST2.propertyid,
            (
                SELECT ST1.Name + '--' AS [text()]
                FROM (
					select mr.propertyid, c.Name
						from SDSD.Invest.MortgageRecord mr
						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
						where   IsActual = 1  and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
				) ST1
                WHERE ST1.propertyid = ST2.propertyid
                ORDER BY ST1.propertyid
                FOR XML PATH ('')
            ) [LMDescr]
        FROM (
			select mr.propertyid, c.Name
						from SDSD.Invest.MortgageRecord mr
						join SDSD.Invest.Collector c on mr.MortgageeId = c.id
						where   IsActual = 1  and mr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
		) ST2
    ) [Main]) ob on ob.PropertyId = pr.PropertyId
left join (SELECT Main.propertyid,
       LEFT(Main.LMDescr,Len(Main.LMDescr)-2) As "Name"
FROM
    (
        SELECT DISTINCT ST2.propertyid,
            (
                SELECT ST1.Name + '--' AS [text()]
                FROM (
					select en.propertyid, c.Name
						from SDSD.Invest.Encumbrance en
						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
				) ST1
                WHERE ST1.propertyid = ST2.propertyid
                ORDER BY ST1.propertyid
                FOR XML PATH ('')
            ) [LMDescr]
        FROM (
			select en.propertyid, c.Name
						from SDSD.Invest.Encumbrance en
						join SDSD.Invest.Collector c on en.CumbersomeId = c.id
						where   IsActual = 1 and en.EncumbranceTypeId = 637043 and en.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)
		) ST2
    ) [Main]) obt on obt.PropertyId = pr.PropertyId
 where ClientINN is not null and IsActual = 1 and pr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck)) as t2 where t2.[Статус_майна] = 'Доп_майно'
 group by  t2.ClientINN) as ad on uclcon.INN = ad.ClientINN collate Cyrillic_General_CI_AS
left join (select uclcon.INN, sum(case when c.CurrencyId = 8 then SummToClose * 1
when c.CurrencyId = 9 then SummToClose * 27.2
when c.CurrencyId = 10 then SummToClose * 31.45
when c.CurrencyId = 19 then SummToClose * 29.32
else SummToClose * 1 end ) as 'sum_borg' from Collect.dbo.reestr r
inner join collect.dbo.contract c on c.ReestrId = r.id
left join  (
  select
    cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, 'Должник' as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.Client cl on cl.id=cont.ClientId
  union all
  select
    cont.id as conID, cl.Surname, cl.Name, cl.MiddleName, cl.INN, cl_type.Name as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
  left join Collect.dbo.Client cl on cl.id=clcon.ClientId
    left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
  where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
) as uclcon on uclcon.conid=c.id
left join	(select sl.itemid, sl.Activedate, d.Name
				from collect.dbo.StopList sl
				inner join collect.dbo.Dictionary d on d.id = sl.ReasonId
				where sl.ActiveStopList = 1 and sl.StopDate is null and sl.TypeId = 82 and sl.Pretendent = 0) as stl on stl.ItemId = c.id
where (stl.Name is null or stl.Name = 'В работе Залогов') and r.IsActual = 1 and r.TypeId = 632263
group by uclcon.INN)as borg on borg.INN = uclcon.INN
-- діючі ВД
left join (select distinct	pc.INN	AS	[INN]
from [10.1.32.64].[LegalCollection].[dbo].[b_Document]					d
left join [Collect].dbo.Dictionary							ddoc		on	ddoc.id = d.TypeId
left join [Collect].dbo.Dictionary							ddoc2		on	ddoc2.id = d.SubtypeId
left join [10.1.32.64].[LegalCollection].[dbo].[b_Claim]					clm			on	d.id = clm.[BDocumentId]
left join [Collect].dbo.Dictionary							dicclm		on	dicclm.id = clm.ClaimTypeId
left join [10.1.32.64].[LegalCollection].[dbo].[b_ContractClaim]			cc			on	cc.ClaimId = clm.Id
left join [10.1.32.64].[LegalCollection].[dbo].[b_PersonClaim]			pc			on	pc.ClaimId = clm.Id
left join [10.1.32.64].[LegalCollection].[dbo].[b_DebtClaim]				dclm		on	dclm.ClaimId = clm.Id
left join [Collect].dbo.Currency							curr		on	curr.id = dclm.CurrencyId
left join [10.1.32.64].[LegalCollection].[dbo].[b_ExecutiveDocument]		ed			on	ed.BDocumentId = d.Id
left join [10.1.32.64].[LegalCollection].[dbo].[b_DocumentLawsuit]		dls			on	dls.BDocumentId = d.Id
where ed.Term	>= GETDATE() ) as vd_all on  uclcon.INN = vd_all.inn collate Cyrillic_General_CI_AS
-- замінена сторона в діючих
left join (Select distinct vl2.INN from (select
	d.Id
,	ddoc.name															as	[Тип документу]
,	ddoc2.name															as	[Підтип документу]
,	convert(nvarchar(max),d.docname	)									as	[Номер/Назва ВД]
,	d.docdate															as	[Дата видачі ВД]
,	d.documentlinkid													as	[Посилання на документ] --на документ онлайн
,	d.note																as	[Коментар]
,	d.importdate														as	[Дата загрузки]
,	dicclm.Name															as	[Тип стягування]
,	dclm.[Sum]															as	[Cума боргу]
,	curr.CurrCode														AS	[Валюта]
,	ed.Term																as	[Строк подачі]
,	pc.INN																AS	[INN]
,	cc.ContractId														as	[НКС]
,  convert(nvarchar(max), cc.ContractId) + '_' +  convert(nvarchar(max), pc.INN)as 'vduniq'
,case when  isnull(zam1.zam, zam2.number ) is null then 0
else 1 end as 'zamena'
from [10.1.32.64].[LegalCollection].[dbo].[b_Document]					d
left join [Collect].dbo.Dictionary							ddoc		on	ddoc.id = d.TypeId
left join [Collect].dbo.Dictionary							ddoc2		on	ddoc2.id = d.SubtypeId
left join [10.1.32.64].[LegalCollection].[dbo].[b_Claim]					clm			on	d.id = clm.[BDocumentId]
left join [Collect].dbo.Dictionary							dicclm		on	dicclm.id = clm.ClaimTypeId
left join [10.1.32.64].[LegalCollection].[dbo].[b_ContractClaim]			cc			on	cc.ClaimId = clm.Id
left join [10.1.32.64].[LegalCollection].[dbo].[b_PersonClaim]			pc			on	pc.ClaimId = clm.Id
left join [10.1.32.64].[LegalCollection].[dbo].[b_DebtClaim]				dclm		on	dclm.ClaimId = clm.Id
left join [Collect].dbo.Currency							curr		on	curr.id = dclm.CurrencyId
left join [10.1.32.64].[LegalCollection].[dbo].[b_ExecutiveDocument]		ed			on	ed.BDocumentId = d.Id
left join [10.1.32.64].[LegalCollection].[dbo].[b_DocumentLawsuit]		dls			on	dls.BDocumentId = d.Id
left join (select distinct convert(nvarchar(max), zam.CaseNamber) as 'zam' from (select c.id as 'НКС', leg.CaseNamber,
	   leg.EventDate as 'EventDate', leg.ReceiptDate,  leg.EventType,
	   et.Name as 'EventName', etr.Name as 'RootName'
from collect.dbo.reestr r
join Collect.dbo.Contragent cn on cn.id = r.ContragentId
join collect.dbo.contract c on c.reestrId = r.id
join [10.1.32.64].legalcollection.property.collectiongroup cgp on c.id = cgp.ContractID
join collect.dbo.client cl on cl.id = c.clientId
left join [10.1.32.64].LegalCollection.dbo.contract lc on lc.contractId = c.id
left join ( select ls.Number as 'CaseNamber', ev.EventTypeId as 'EventType',  lwc.contractSuitId,  ev.id as 'EventId',
		    ev.eventDate, ev.receiptDate, ev.typerootId, ev.eventTypeId
			from [10.1.32.64].LegalCollection.dbo.LawContract lwc
			join [10.1.32.64].LegalCollection.dbo.LawSuit ls on lwc.LawSuitId = ls.id
			left join [10.1.32.64].LegalCollection.dbo.event ev on ev.SuitId = ls.id
			) as leg on leg.contractSuitId = lc.id
left join [10.1.32.64].LegalCollection.dbo.EventType et on et.id = leg.EventTypeId
left join [10.1.32.64].LegalCollection.dbo.EventType etR on et.rootId = etR.id
where  --cgp.Name in ( 'Ипотека_Алексей', 'Ипотека_Алёна')    and
leg.EventType in (102,	120,	147,	192,	486,	488,	490,	636,	638,	643,	644,	654,	655)) zam )as zam1 on convert(nvarchar(max), d.docname)	= zam1.zam
left join (select distinct ls.number from [10.1.32.64].LegalCollection.dbo.LawSuit ls
left join [10.1.32.64].LegalCollection.dbo.Client c on ls.Plaintiffid = c.id
where c.id in (4899	,
63	,
113185	,
259623	,
104116	,
341492	,
80609	,
80612	,
81062	,
81094	,
81096	,
25694	,
81047	,
81060	,
80610	,
80611	,
81061	,
81063	,
81095	,
81097	,
80599	,
80601	,
80603	,
25695	,
80606	,
80613	,
81051	,
81092	,
81099	,
25697	,
259430	,
80602	,
80604	,
81052	,
81087	,
81088	,
85616	,
80608	,
81049	,
81056	,
81058	,
81065	,
81067	,
81090	,
104122	,
81054	,
81055	,
81068	,
81070	,
85617	,
81089	,
81091	,
81093	,
81098	,
81100	,
94037	,
80600	,
80607	,
80614	,
81050	,
81057	,
81059	,
81064	,
81066	,
25696	,
81053	,
81069	,
81071	,
85618	,
80138	,
80147	,
80154	,
104120	,
81699	,
80141	,
80159	,
104118	,
81648	,
81697	,
80131	,
80156	,
80129	,
80140	,
80145	,
80163	,
80165	,
105412	,
81583	,
81585	,
81592	,
81649	,
81708	,
81710	,
81694	,
81701	,
81703	,
80158	,
80160	,
80161	,
80130	,
80155	,
81582	,
81650	,
81691	,
81693	,
81702	,
81711	,
22792	,
80133	,
80150	,
80151	,
81589	,
81590	,
81705	,
81707	,
80136	,
80149	,
80152	,
81587	,
81588	,
81704	,
81580	,
81581	,
81647	,
81695	,
81698	,
81712	,
81715	,
80132	,
80137	,
80139	,
80157	,
80162	,
80164	,
81700	,
81709	,
104124	,
80142	,
80143	,
80144	,
81646	,
81696	,
81713	,
81714	,
80135	,
80166	,
81706	,
81722	,
81723	,
80605	,
81048	,
80146	,
80153	,
81584	,
81586	,
81591	))as zam2 on convert(nvarchar(max), d.docname)	= zam2.number
where ed.Term	>= GETDATE() and case when  isnull(zam1.zam, zam2.number ) is null then 0 else 1 end >=1)as vl2)as zam_all on  uclcon.INN = zam_all.INN collate Cyrillic_General_CI_AS
where (stl.Name is null or stl.Name = 'В работе Залогов') and r.IsActual = 1 and r.TypeId = 632263 and uclcon.INN <> '' """

df = pd.read_sql_query(requestString, inputing.getConnection())
dbCursor.execute(requestString).fetchall()

cat_size_order = CategoricalDtype(
    ['0 - 30 000', '30 000 - 50 000', '50 000 - 100 000','100 000 - 250 000',
                             '250 000 - 500 000', '500 000+'],
    ordered=True
)
df['Сегмент боргу'] = df['Сегмент боргу'].astype(cat_size_order)
df.sort_values('Сегмент боргу')
ipoteca = [row for row in df['К-ть ІПН з майном в іпотеці']]

extra_property = [row for row in df['К-ть ІПН з додатковим майном']]
property_all = [x + y for x, y in zip_longest(ipoteca, extra_property, fillvalue=0)]
for key, value in enumerate(property_all):
    if value < 1:
        property_all[key] = 0
    else:
        property_all[key] = 1

inputing.adding_to_table(df, 'К-ть ІПН з майном', property_all)

vp_type_table = inputing.addingfromExcel(file=r'\\fs250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
                              sheetName='Полотно_ІПН', column='Тип ВП')

vp_type = [str(row) for row in vp_type_table]

free_check_table = df['К-ть перевірених ІПН по безкоштовній перевірці']

free_check = [int(row) for row in free_check_table]
inputing.adding_to_table(df, 'К-ть перевірених ІПН по безкоштовній перевірці', free_check)

inputing.adding_to_table(df, ' К-ть ІПН з платною перевіркою за адресою',
                         inputing.addingfromExcel(file=r'\\fs250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
                                                  sheetName='Полотно_ІПН',
                                                  column=' К-ть ІПН з платною перевіркою за адресою'))


inputing.adding_to_table(df, 'Активне АСВП', inputing.addingfromExcel(file=r'\\fs250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
                                                                      sheetName='Полотно_ІПН',
                                                                      column='Активне АСВП'))

inputing.adding_to_table(df, 'К-ть ІПН з діючим ВД', inputing.addingfromExcel(file=r'\\fs250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
                                                                      sheetName='Полотно_ІПН',
                                                                      column='К-ть ІПН з діючим ВД'))
free = [str(row) for row in df['К-ть ІПН з діючим ВД']]
inputing.adding_to_table(df, 'К-ть ІПН з діючим ВД', free)

fre1 = [str(row) for row in df['К-ть ІПН з  діючим ВД та заміненою стороною']]
inputing.adding_to_table(df, 'К-ть ІПН з  діючим ВД та заміненою стороною', fre1)

fre2 = [str(row) for row in df['Активне АСВП']]
inputing.adding_to_table(df, 'Активне АСВП', fre2)

inputing.adding_to_table(df, 'Тип ВП', vp_type)

fre3 = [int(row) for row in df['К-ть ІПН з майном']]
inputing.adding_to_table(df, 'К-ть ІПН з майном', fre3)


values = ['INN', 'К-ть правильних ІПН', 'К-ть перевірених ІПН по безкоштовній перевірці',
        'К-ть ІПН з майном по безкоштовній перевірці', ' К-ть ІПН з майном на Мирній Україні',
        'К-ть в Донецька/Луганська обл', ' К-ть ІПН з платною перевіркою за адресою',
        'К-ть завантажених ІПН з платною перевіркою за адресою', 'К-ть ІПН з майном', 'К-ть ІПН з майном в іпотеці',
        'К-ть ІПН з додатковим майном']

pivot_segment = pd.pivot_table(df, index=['Сегмент боргу'], values=values, aggfunc={'INN': 'count',
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


pivot_segment['К-ть правильних ІПН'] = pivot_segment['К-ть правильних ІПН'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['INN'] = pivot_segment['INN'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['К-ть перевірених ІПН по безкоштовній перевірці'] = \
    pivot_segment['К-ть перевірених ІПН по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['К-ть ІПН з майном по безкоштовній перевірці'] \
    = pivot_segment['К-ть ІПН з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment[' К-ть ІПН з майном на Мирній Україні'] \
    = pivot_segment[' К-ть ІПН з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['К-ть в Донецька/Луганська обл'] \
    = pivot_segment['К-ть в Донецька/Луганська обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment[' К-ть ІПН з платною перевіркою за адресою'] \
    = pivot_segment[' К-ть ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['К-ть завантажених ІПН з платною перевіркою за адресою'] \
    = pivot_segment['К-ть завантажених ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['К-ть ІПН з майном'] = pivot_segment['К-ть ІПН з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['К-ть ІПН з майном в іпотеці'] = pivot_segment['К-ть ІПН з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_segment['К-ть ІПН з додатковим майном'] = pivot_segment['К-ть ІПН з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')


pivot_active_vd = pd.pivot_table(df, index=['Сегмент боргу', 'К-ть ІПН з діючим ВД'], values=values,
                                 aggfunc={'INN': 'count',
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
                               fill_value='', margins=True, dropna=True, margins_name='All', observed=False)

pivot_active_vd['К-ть правильних ІПН'] = pivot_active_vd['К-ть правильних ІПН'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['INN'] = pivot_active_vd['INN'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['К-ть перевірених ІПН по безкоштовній перевірці'] = \
    pivot_active_vd['К-ть перевірених ІПН по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['К-ть ІПН з майном по безкоштовній перевірці'] \
    = pivot_active_vd['К-ть ІПН з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd[' К-ть ІПН з майном на Мирній Україні'] \
    = pivot_active_vd[' К-ть ІПН з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['К-ть в Донецька/Луганська обл'] \
    = pivot_active_vd['К-ть в Донецька/Луганська обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd[' К-ть ІПН з платною перевіркою за адресою'] \
    = pivot_active_vd[' К-ть ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['К-ть завантажених ІПН з платною перевіркою за адресою'] \
    = pivot_active_vd['К-ть завантажених ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['К-ть ІПН з майном'] = pivot_active_vd['К-ть ІПН з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['К-ть ІПН з майном в іпотеці'] = pivot_active_vd['К-ть ІПН з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_vd['К-ть ІПН з додатковим майном'] = pivot_active_vd['К-ть ІПН з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')

pivot_changed_vd = pd.pivot_table(df, index=['Сегмент боргу', 'К-ть ІПН з  діючим ВД та заміненою стороною'], values=values,
                                 aggfunc={'INN': 'count',
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
                               fill_value='', margins=True, dropna=True, margins_name='All', observed=False)

pivot_changed_vd['К-ть правильних ІПН'] = pivot_changed_vd['К-ть правильних ІПН'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['INN'] = pivot_changed_vd['INN'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['К-ть перевірених ІПН по безкоштовній перевірці'] = \
    pivot_changed_vd['К-ть перевірених ІПН по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['К-ть ІПН з майном по безкоштовній перевірці'] \
    = pivot_changed_vd['К-ть ІПН з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd[' К-ть ІПН з майном на Мирній Україні'] \
    = pivot_changed_vd[' К-ть ІПН з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['К-ть в Донецька/Луганська обл'] \
    = pivot_changed_vd['К-ть в Донецька/Луганська обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd[' К-ть ІПН з платною перевіркою за адресою'] \
    = pivot_changed_vd[' К-ть ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['К-ть завантажених ІПН з платною перевіркою за адресою'] \
    = pivot_changed_vd['К-ть завантажених ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['К-ть ІПН з майном'] = pivot_changed_vd['К-ть ІПН з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['К-ть ІПН з майном в іпотеці'] = pivot_changed_vd['К-ть ІПН з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_changed_vd['К-ть ІПН з додатковим майном'] = pivot_changed_vd['К-ть ІПН з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')

pivot_active_asvp = pd.pivot_table(df, index=['Сегмент боргу', 'Активне АСВП'], values=values,
                                 aggfunc={'INN': 'count',
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
                               fill_value='', margins=True, dropna=True, margins_name='All', observed=False)

pivot_active_asvp['К-ть правильних ІПН'] = pivot_active_asvp['К-ть правильних ІПН'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['INN'] = pivot_active_asvp['INN'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['К-ть перевірених ІПН по безкоштовній перевірці'] = \
    pivot_active_asvp['К-ть перевірених ІПН по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['К-ть ІПН з майном по безкоштовній перевірці'] \
    = pivot_active_asvp['К-ть ІПН з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp[' К-ть ІПН з майном на Мирній Україні'] \
    = pivot_active_asvp[' К-ть ІПН з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['К-ть в Донецька/Луганська обл'] \
    = pivot_active_asvp['К-ть в Донецька/Луганська обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp[' К-ть ІПН з платною перевіркою за адресою'] \
    = pivot_active_asvp[' К-ть ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['К-ть завантажених ІПН з платною перевіркою за адресою'] \
    = pivot_active_asvp['К-ть завантажених ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['К-ть ІПН з майном'] = pivot_active_asvp['К-ть ІПН з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['К-ть ІПН з майном в іпотеці'] = pivot_active_asvp['К-ть ІПН з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_active_asvp['К-ть ІПН з додатковим майном'] = pivot_active_asvp['К-ть ІПН з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')

pivot_type_vp = pd.pivot_table(df, index=['Сегмент боргу', 'Тип ВП'], values=values,
                               aggfunc={'INN': 'count',
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
                               fill_value='', margins=True, dropna=True, margins_name='All', observed=False)

pivot_type_vp['К-ть правильних ІПН'] = pivot_type_vp['К-ть правильних ІПН'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['INN'] = pivot_type_vp['INN'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['К-ть перевірених ІПН по безкоштовній перевірці'] = \
    pivot_type_vp['К-ть перевірених ІПН по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['К-ть ІПН з майном по безкоштовній перевірці'] \
    = pivot_type_vp['К-ть ІПН з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp[' К-ть ІПН з майном на Мирній Україні'] \
    = pivot_type_vp[' К-ть ІПН з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['К-ть в Донецька/Луганська обл'] \
    = pivot_type_vp['К-ть в Донецька/Луганська обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp[' К-ть ІПН з платною перевіркою за адресою'] \
    = pivot_type_vp[' К-ть ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['К-ть завантажених ІПН з платною перевіркою за адресою'] \
    = pivot_type_vp['К-ть завантажених ІПН з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['К-ть ІПН з майном'] = pivot_type_vp['К-ть ІПН з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['К-ть ІПН з майном в іпотеці'] = pivot_type_vp['К-ть ІПН з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_type_vp['К-ть ІПН з додатковим майном'] = pivot_type_vp['К-ть ІПН з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')


