import pandas as pd
import urllib
from sqlalchemy import create_engine
from itertools import zip_longest
import inputing

requestString = ''' Select distinct c.id , isnull(pro.Name, r.name) as 'Проект', 
        cast(case when c.CurrencyId = 8 then SummToClose * 1 
        when c.CurrencyId = 9 then SummToClose * 27.2 
        when c.CurrencyId = 10 then SummToClose * 31.45
        when c.CurrencyId = 19 then SummToClose * 29.32
        else SummToClose * 1 end  AS float)  as 'Сума боргу',
        case when  r.RNumber in (3847, 3846, 3845)  then 'Беззаставні'
        when cg.name like 'Ипотека_%' then 'Іпотека'
        when cg.name like 'авто%' then 'Авто' 
        when cg.name like 'КЦ%' then 'Авто'
        else 'Беззаставні' end as 'Бізнес',
        case when fpc.conID is null then '0'
        else '1' end as 'К-ть  НКС перевірених по безкоштовній перевірці',
        case when maino.conID is null then '0'
        else '1' end as 'К-ть НКС з майном по безкоштовній перевірці',
        case when mu1.conID is null then '0'
        else '1' end as 'К-ть НКС з майном на Мирній Україні',
        case when ato.conID is null then '0'
        else '1' end as 'К-ть НКС з майном в Донецькій/Луганській обл',
        case when pp.ContractId is null then 0
        else 1 end as 'К-ть завантажених НКС з платною перевіркою',
        case when ipo.conID is null then 0
        else 1 end as 'К-ть НКС з майном в іпотеці',
        case when adp.conID is null then 0
        else 1 end as 'К-ть НКС з додатковим майном',
        case when vd_all.NKS is null then 0
        else  1 end 'К-ть ІПН з діючим ВД',
        case when zam_all.NKS is null then 0
        else  1 end 'К-ть ІПН з  діючим ВД та заміненою стороною'
        from Collect.dbo.reestr r 
        inner join collect.dbo.contract c on c.ReestrId = r.id
        left join [10.1.32.64].legalcollection.property.collectiongroup cg on c.id = cg.contractid
        left join (select p.RNumber, n.Name from SDSD.Invest.NKSInvestProject p
                        left join SDSD.Invest.InvestProject n on p.InvestProjectId = n.id) pro on pro.RNumber= r.RNumber
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
        --безкоштовна перевірка
        left join (select distinct inn.conID from (select
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
          where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо') as inn
          left join SDSD.invest.FreePropertyCheck pc on inn.INN = pc.INN collate Cyrillic_General_CI_AS
          where pc.PropertyList is not null)as fpc on c.id = fpc.conID

        -- НКС з майном
        left join (select distinct inn.conID from (select
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
          where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо') as inn
          left join SDSD.invest.FreeINNPropertyCheck pc1 on inn.INN = pc1.INN collate Cyrillic_General_CI_AS
          where pc1.Description is not null)as maino on c.id = maino.conID
          --Мирна Україна
          left join (select distinct mu_all.conID from (select
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
        ) as mu_all
        left join (select t4.INN from (select *,
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
        )as mu on mu_all.INN = mu.INN collate Cyrillic_General_CI_AS
        where mu.INN is not null)as mu1 on c.id = mu1.conID
        --АТО
        left join (select distinct mu_all.conID from (select
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
        ) as mu_all
        left join (select t4.INN from (select *,
        case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%' 
        and PropertyList not like '85%' then 'Мирна Україіна'
        when PropertyList like '14%' then 'Донецька/Луганська обл'
        when PropertyList like '44%' then 'Донецька/Луганська обл'
        when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
        when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
        when PropertyList like 'Автономна%' then 'Крим'
        when PropertyList like '85%' then 'Крим'
        else 'Нічого не знайдено' end 'Регіон' 
        from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Донецька/Луганська обл'
        )as mu on mu_all.INN = mu.INN collate Cyrillic_General_CI_AS
        where mu.INN is not null and mu_all.conID not in (select distinct mu_all.conID from (select
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
        ) as mu_all
        left join (select t4.INN from (select *,
        case when PropertyList not like '14%' and PropertyList not like '44%' and PropertyList not like 'Донецька%' and PropertyList not like 'Луганська%' and PropertyList not like 'Автономна%' 
        and PropertyList not like '85%' then 'Мирна Україіна'
        when PropertyList like '14%' then 'Донецька/Луганська обл'
        when PropertyList like '44%' then 'Донецька/Луганська обл'
        when PropertyList like 'Донецька%' then 'Донецька/Луганська обл'
        when PropertyList like 'Луганська%' then 'Донецька/Луганська обл'
        when PropertyList like 'Автономна%' then 'Крим'
        when PropertyList like '85%' then 'Крим'
        else 'Мирна Україіна' end 'Регіон' 
        from SDSD.Invest.FreePropertyCheck ) as t4 where t4.Регіон = 'Мирна Україіна'
        )as mu on mu_all.INN = mu.INN collate Cyrillic_General_CI_AS
        where mu.INN is not null))as ato on c.id = ato.conID
        --Платна перевірка 
        left join ( select distinct ContractId from SDSD.Invest.ContractProperty where PropertyId in (
        select distinct PropertyId from SDSD.Invest.PropertyCheck )) as pp on c.id = pp.ContractId
        --майно в іпотеці
        left join (select distinct ipoteka.conID from (select
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
        ) as ipoteka
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
         group by  t2.ClientINN) as ipot on ipoteka.INN = ipot.ClientINN collate Cyrillic_General_CI_AS where ipot.ClientINN is not null) as ipo on c.id = ipo.conID
         --додаткове майно
         left join (select distinct ipoteka.conID from (select
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
        ) as ipoteka
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
         where pr.ClientINN is not null and pr.IsActual = 1 and pr.propertyid in (select PropertyId from SDSD.Invest.PropertyCheck) ) as t2 where t2.[Статус_майна] = 'Доп_майно' 
         group by  t2.ClientINN) as ipot on ipoteka.INN = ipot.ClientINN collate Cyrillic_General_CI_AS where ipot.ClientINN is not null)as adp on c.id = adp.conID
         --діючі ВД
         left join (select distinct	cc.ContractId	AS	[NKS]
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
        where ed.Term	>= GETDATE() ) as vd_all on  uclcon.conID = vd_all.NKS 
        --Вд зі стороною
        left join (Select distinct vl2.NKS  from (select
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
        ,	cc.ContractId														as	[NKS]
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
        where ed.Term	>= GETDATE() and case when  isnull(zam1.zam, zam2.number ) is null then 0 else 1 end >=1)as vl2)as zam_all on  uclcon.conID = zam_all.NKS
         where (stl.Name is null or stl.Name = 'В работе Залогов') and r.IsActual = 1 and r.TypeId = 632263  '''
params = 'DRIVER={SQL Server};' \
         'SERVER=10.1.32.56;' \
         'PORT=1433;' \
         'DATABASE=Collect;' \
         'UID=sqlbot;' \
         'PWD=9"BgB4J2;'

params = urllib.parse.quote_plus(params)

db = create_engine('mssql+pyodbc:///?odbc_connect=%s' % params)
df1 = pd.read_sql_query(requestString, db)
in_ipotec = [row for row in df1['К-ть НКС з майном в іпотеці']]
dop_property = [row for row in df1['К-ть НКС з додатковим майном']]
property_all = [x + y for x, y in zip_longest(in_ipotec, dop_property, fillvalue=0)]

for key, value in enumerate(property_all):
    if value < 1:
        property_all[key] = 0
    else:
        property_all[key] = 1
inputing.adding_to_table(df1, 'К-ть НКС з майном', property_all)

borg = [row for row in df1['Сума боргу']]
for key, value in enumerate(borg):
    if value < 30000:
        borg[key] = 0
    else:
        borg[key] = 1
inputing.adding_to_table(df1, 'К-ть НКС з боргом від 30к грн', borg)

ff = inputing.addingfromExcel(file=r'\\fs250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
                              sheetName='Полотно_ІПН', column='Тип ВП')
vp_type = [str(row) for row in ff]
inputing.adding_to_table(df1, 'Тип ВП', vp_type)

inputing.adding_to_table(df1, 'К-ть НКС з платною перевіркою за адресою',
                         inputing.addingfromExcel(file=r'\\fs250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
                                                  sheetName='Полотно НКС',
                                                  column=' К-ть ІПН з платною перевіркою за адресою'))

inputing.adding_to_table(df1, 'Активне АСВП',
                         inputing.addingfromExcel(file=r'\\fs250\Documents repository DOP\Analytics\LEGAL\VHoch\Звіти\Звіт по іпн.xlsx',
                                                  sheetName='Полотно НКС',
                                                  column='Активне АСВП'))
free_check = [int(row) for row in df1['К-ть  НКС перевірених по безкоштовній перевірці']]
inputing.adding_to_table(df1, 'К-ть  НКС перевірених по безкоштовній перевірці', free_check)

property_dl = [int(row) for row in df1['К-ть НКС з майном в Донецькій/Луганській обл']]
inputing.adding_to_table(df1, 'К-ть НКС з майном в Донецькій/Луганській обл', property_dl)

property_uk = [int(row) for row in df1['К-ть НКС з майном на Мирній Україні']]
inputing.adding_to_table(df1, 'К-ть НКС з майном на Мирній Україні', property_uk)


property_with = [int(row) for row in df1['К-ть НКС з майном']]
inputing.adding_to_table(df1, 'К-ть НКС з майном', property_with)

free_check_property = [int(row) for row in df1['К-ть НКС з майном по безкоштовній перевірці']]
inputing.adding_to_table(df1, 'К-ть НКС з майном по безкоштовній перевірці', free_check_property)

download_pay_check = [int(row) for row in df1['К-ть завантажених НКС з платною перевіркою']]
inputing.adding_to_table(df1, 'К-ть завантажених НКС з платною перевіркою', download_pay_check)


df1.loc[df1['К-ть НКС з платною перевіркою за адресою'].notnull(), 'К-ть НКС з платною перевіркою за адресою'] \
    = df1.loc[df1['К-ть НКС з платною перевіркою за адресою'].notnull(), 'К-ть НКС з платною перевіркою за адресою'].apply(int)
# pay_check_adress = [int(row) for row in df1['К-ть НКС з платною перевіркою за адресою']]
# inputing.adding_to_table(df1, 'К-ть НКС з платною перевіркою за адресою', pay_check_adress)

property_ipoteque = [int(row) for row in df1['К-ть НКС з майном в іпотеці']]
inputing.adding_to_table(df1, 'К-ть НКС з майном в іпотеці',property_ipoteque)

extra_property = [int(row) for row in df1['К-ть НКС з додатковим майном']]
inputing.adding_to_table(df1, 'К-ть НКС з додатковим майном', extra_property)

fre1 = [str(row) for row in df1['К-ть НКС з боргом від 30к грн']]
inputing.adding_to_table(df1, 'К-ть НКС з боргом від 30к грн', fre1)

fre2 = [str(row) for row in df1['К-ть ІПН з діючим ВД']]
inputing.adding_to_table(df1, 'К-ть ІПН з діючим ВД', fre2)

fre3 = [str(row) for row in df1[ 'К-ть ІПН з  діючим ВД та заміненою стороною']]
inputing.adding_to_table(df1,  'К-ть ІПН з  діючим ВД та заміненою стороною', fre3)

fre4 = [str(row) for row in df1[ 'Активне АСВП']]
inputing.adding_to_table(df1, 'Активне АСВП', fre4)



values = ['id', 'К-ть  НКС перевірених по безкоштовній перевірці', 'К-ть НКС з майном по безкоштовній перевірці',
          'К-ть НКС з майном на Мирній Україні', 'К-ть НКС з майном в Донецькій/Луганській обл',
          'К-ть НКС з майном', 'К-ть завантажених НКС з платною перевіркою',
          'К-ть НКС з платною перевіркою за адресою', 'К-ть НКС з майном в іпотеці',
          'К-ть НКС з додатковим майном']


pivot_business_borg30 = pd.pivot_table(df1, index=['Бізнес', 'К-ть НКС з боргом від 30к грн'], values=values,
                                       aggfunc={'id': 'count',
                                                'К-ть  НКС перевірених по безкоштовній перевірці': 'sum',
                                                'К-ть НКС з майном по безкоштовній перевірці': 'sum',
                                                'К-ть НКС з майном на Мирній Україні': 'sum',
                                                'К-ть НКС з майном в Донецькій/Луганській обл': 'sum',
                                                'К-ть НКС з майном': 'sum',
                                                'К-ть завантажених НКС з платною перевіркою': 'sum',
                                                'К-ть НКС з платною перевіркою за адресою': 'sum',
                                                'К-ть НКС з майном в іпотеці': 'sum',
                                                'К-ть НКС з додатковим майном': 'sum'},
                                       fill_value='', margins=True, dropna=True, margins_name='All', observed=False)

pivot_business_borg30['id'] = pivot_business_borg30['id'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть  НКС перевірених по безкоштовній перевірці']\
    = pivot_business_borg30['К-ть  НКС перевірених по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть НКС з майном по безкоштовній перевірці'] = \
    pivot_business_borg30['К-ть НКС з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть НКС з майном на Мирній Україні'] \
    = pivot_business_borg30['К-ть НКС з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть НКС з майном в Донецькій/Луганській обл'] \
    = pivot_business_borg30['К-ть НКС з майном в Донецькій/Луганській обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть НКС з майном'] \
    = pivot_business_borg30['К-ть НКС з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть завантажених НКС з платною перевіркою'] \
    = pivot_business_borg30['К-ть завантажених НКС з платною перевіркою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть НКС з платною перевіркою за адресою'] \
    = pivot_business_borg30['К-ть НКС з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть НКС з майном в іпотеці'] = pivot_business_borg30['К-ть НКС з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30['К-ть НКС з додатковим майном'] = pivot_business_borg30['К-ть НКС з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')

pivot_business_borg30_vd = pd.pivot_table(df1, index=['Бізнес', 'К-ть НКС з боргом від 30к грн', 'К-ть ІПН з діючим ВД'],
                                          values=values,
                                          aggfunc={'id': 'count',
                                                   'К-ть  НКС перевірених по безкоштовній перевірці': 'sum',
                                                   'К-ть НКС з майном по безкоштовній перевірці': 'sum',
                                                   'К-ть НКС з майном на Мирній Україні': 'sum',
                                                   'К-ть НКС з майном в Донецькій/Луганській обл': 'sum',
                                                   'К-ть НКС з майном': 'sum',
                                                   'К-ть завантажених НКС з платною перевіркою': 'sum',
                                                   'К-ть НКС з платною перевіркою за адресою': 'sum',
                                                   'К-ть НКС з майном в іпотеці': 'sum',
                                                   'К-ть НКС з додатковим майном': 'sum'},
                                          fill_value='', margins=True, dropna=True, margins_name='All', observed=False)
pivot_business_borg30_vd['id'] = pivot_business_borg30_vd['id'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть  НКС перевірених по безкоштовній перевірці']\
    = pivot_business_borg30_vd['К-ть  НКС перевірених по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть НКС з майном по безкоштовній перевірці'] = \
    pivot_business_borg30_vd['К-ть НКС з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть НКС з майном на Мирній Україні'] \
    = pivot_business_borg30_vd['К-ть НКС з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть НКС з майном в Донецькій/Луганській обл'] \
    = pivot_business_borg30_vd['К-ть НКС з майном в Донецькій/Луганській обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть НКС з майном'] \
    = pivot_business_borg30_vd['К-ть НКС з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть завантажених НКС з платною перевіркою'] \
    = pivot_business_borg30_vd['К-ть завантажених НКС з платною перевіркою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть НКС з платною перевіркою за адресою'] \
    = pivot_business_borg30_vd['К-ть НКС з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть НКС з майном в іпотеці'] \
    = pivot_business_borg30_vd['К-ть НКС з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vd['К-ть НКС з додатковим майном'] \
    = pivot_business_borg30_vd['К-ть НКС з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')

pivot_business_borg30_active_vd = pd.pivot_table(df1, index=['Бізнес', 'К-ть НКС з боргом від 30к грн',
                                                             'К-ть ІПН з  діючим ВД та заміненою стороною'],
                                                 values=values,
                                                 aggfunc={'id': 'count',
                                                          'К-ть  НКС перевірених по безкоштовній перевірці': 'sum',
                                                          'К-ть НКС з майном по безкоштовній перевірці': 'sum',
                                                          'К-ть НКС з майном на Мирній Україні': 'sum',
                                                          'К-ть НКС з майном в Донецькій/Луганській обл': 'sum',
                                                          'К-ть НКС з майном': 'sum',
                                                          'К-ть завантажених НКС з платною перевіркою': 'sum',
                                                          'К-ть НКС з платною перевіркою за адресою': 'sum',
                                                          'К-ть НКС з майном в іпотеці': 'sum',
                                                          'К-ть НКС з додатковим майном': 'sum'},
                                                 fill_value='', margins=True, dropna=True, margins_name='All', observed=False)
pivot_business_borg30_active_vd['id'] = pivot_business_borg30_active_vd['id'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть  НКС перевірених по безкоштовній перевірці']\
    = pivot_business_borg30_active_vd['К-ть  НКС перевірених по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть НКС з майном по безкоштовній перевірці'] = \
    pivot_business_borg30_active_vd['К-ть НКС з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть НКС з майном на Мирній Україні'] \
    = pivot_business_borg30_active_vd['К-ть НКС з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть НКС з майном в Донецькій/Луганській обл'] \
    = pivot_business_borg30_active_vd['К-ть НКС з майном в Донецькій/Луганській обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть НКС з майном'] \
    = pivot_business_borg30_active_vd['К-ть НКС з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть завантажених НКС з платною перевіркою'] \
    = pivot_business_borg30_active_vd['К-ть завантажених НКС з платною перевіркою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть НКС з платною перевіркою за адресою'] \
    = pivot_business_borg30_active_vd['К-ть НКС з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть НКС з майном в іпотеці'] \
    = pivot_business_borg30_active_vd['К-ть НКС з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_active_vd['К-ть НКС з додатковим майном'] \
    = pivot_business_borg30_active_vd['К-ть НКС з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')

pivot_business_borg30_asvp = pd.pivot_table(df1, index=['Бізнес', 'К-ть НКС з боргом від 30к грн', 'Активне АСВП'],
                                            values=values,
                                            aggfunc={'id': 'count',
                                                     'К-ть  НКС перевірених по безкоштовній перевірці': 'sum',
                                                     'К-ть НКС з майном по безкоштовній перевірці': 'sum',
                                                     'К-ть НКС з майном на Мирній Україні': 'sum',
                                                     'К-ть НКС з майном в Донецькій/Луганській обл': 'sum',
                                                     'К-ть НКС з майном': 'sum',
                                                     'К-ть завантажених НКС з платною перевіркою': 'sum',
                                                     'К-ть НКС з платною перевіркою за адресою': 'sum',
                                                     'К-ть НКС з майном в іпотеці': 'sum',
                                                     'К-ть НКС з додатковим майном': 'sum'},
                                            fill_value='', margins=True, dropna=True, margins_name='All', observed=False)
pivot_business_borg30_asvp['id'] = pivot_business_borg30_asvp['id'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть  НКС перевірених по безкоштовній перевірці']\
    = pivot_business_borg30_asvp['К-ть  НКС перевірених по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть НКС з майном по безкоштовній перевірці'] = \
    pivot_business_borg30_asvp['К-ть НКС з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть НКС з майном на Мирній Україні'] \
    = pivot_business_borg30_asvp['К-ть НКС з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть НКС з майном в Донецькій/Луганській обл'] \
    = pivot_business_borg30_asvp['К-ть НКС з майном в Донецькій/Луганській обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть НКС з майном'] \
    = pivot_business_borg30_asvp['К-ть НКС з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть завантажених НКС з платною перевіркою'] \
    = pivot_business_borg30_asvp['К-ть завантажених НКС з платною перевіркою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть НКС з платною перевіркою за адресою'] \
    = pivot_business_borg30_asvp['К-ть НКС з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть НКС з майном в іпотеці'] \
    = pivot_business_borg30_asvp['К-ть НКС з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_asvp['К-ть НКС з додатковим майном'] \
    = pivot_business_borg30_asvp['К-ть НКС з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')


pivot_business_borg30_vp_type = pd.pivot_table(df1, index=['Бізнес', 'Тип ВП'],
                                               values=values,
                                               aggfunc={'id': 'count',
                                                        'К-ть  НКС перевірених по безкоштовній перевірці': 'sum',
                                                        'К-ть НКС з майном по безкоштовній перевірці': 'sum',
                                                        'К-ть НКС з майном на Мирній Україні': 'sum',
                                                        'К-ть НКС з майном в Донецькій/Луганській обл': 'sum',
                                                        'К-ть НКС з майном': 'sum',
                                                        'К-ть завантажених НКС з платною перевіркою': 'sum',
                                                        'К-ть НКС з платною перевіркою за адресою': 'sum',
                                                        'К-ть НКС з майном в іпотеці': 'sum',
                                                        'К-ть НКС з додатковим майном': 'sum'},
                                               fill_value='', margins=True, dropna=True, margins_name='All', observed=False)
pivot_business_borg30_vp_type['id'] = pivot_business_borg30_vp_type['id'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть  НКС перевірених по безкоштовній перевірці']\
    = pivot_business_borg30_vp_type['К-ть  НКС перевірених по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть НКС з майном по безкоштовній перевірці'] = \
    pivot_business_borg30_vp_type['К-ть НКС з майном по безкоштовній перевірці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть НКС з майном на Мирній Україні'] \
    = pivot_business_borg30_vp_type['К-ть НКС з майном на Мирній Україні'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть НКС з майном в Донецькій/Луганській обл'] \
    = pivot_business_borg30_vp_type['К-ть НКС з майном в Донецькій/Луганській обл'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть НКС з майном'] \
    = pivot_business_borg30_vp_type['К-ть НКС з майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть завантажених НКС з платною перевіркою'] \
    = pivot_business_borg30_vp_type['К-ть завантажених НКС з платною перевіркою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть НКС з платною перевіркою за адресою'] \
    = pivot_business_borg30_vp_type['К-ть НКС з платною перевіркою за адресою'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть НКС з майном в іпотеці'] \
    = pivot_business_borg30_vp_type['К-ть НКС з майном в іпотеці'].map(lambda x: f'{x:,}').str.replace(',', ' ')
pivot_business_borg30_vp_type['К-ть НКС з додатковим майном'] \
    = pivot_business_borg30_vp_type['К-ть НКС з додатковим майном'].map(lambda x: f'{x:,}').str.replace(',', ' ')
