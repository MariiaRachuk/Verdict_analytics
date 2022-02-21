import pyodbc
import sys
import pandas as pd
import input_sql
sys.setrecursionlimit(5000)
server = '10.1.32.64'
database = 'Collect'
username = 'sqlbot'
password = '''9"BgB4J2'''

connection = pyodbc.connect('Driver={SQL Server};'f'Server=' + server + ';DATABASE=' + database
                            + ';UID=' + username + ';PWD=' + password)

dbCursor = connection.cursor()
requestString = """ Select t1.NKS, t1.INN, ep.Name, ep.EPNumber, 
case when ep.CollectorId in (821, 939, 707, 471, 696, 821, 1411) then 'Наші ВП' else 'Нашого банку ВП' end as 'Тип ВП',
ep.CollectorName, gis.Name as Name2 from (select TOP(5) seg.SegmentionList as 'NKS', uclcon.INN as 'INN', seg.CollectorId from LegalCollection.dbo.ASVP_segmentation seg
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
) as uclcon on uclcon.conid=seg.SegmentionList
where seg.SegmentionType = 637286
union
select c.id as 'NKS', uclcon.INN as 'INN', seg.CollectorId from LegalCollection.dbo.ASVP_segmentation seg
inner join collect.dbo.reestr r on r.RNumber = SegmentionList
inner join collect.dbo.contract c on c.ReestrId = r.id
left join  (
  select
    distinct cont.id as conID, cl.INN, 'Должник' as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.Client cl on cl.id=cont.ClientId
  union all
  select
    distinct cont.id as conID, cl.INN, cl_type.Name as ClientType
  from Collect.dbo.Contract cont
  left join Collect.dbo.ClientContract clcon on clcon.ContractId=cont.id
  left join Collect.dbo.Client cl on cl.id=clcon.ClientId
  left join Collect.dbo.Dictionary cl_type on cl_type.id=clcon.ClientTypeId
  where cl_type.Name is not null and cl_type.Name not like 'Контактное лицо' --and cl_type.Name not like 'Поручитель материальный'
) as uclcon on uclcon.conid=c.id
where seg.SegmentionType = 637285) t1
right join LegalCollection.dbo.EnforcementProceedings ep on convert(nvarchar(50),t1.INN) + '_'+ convert(nvarchar(50), t1.CollectorId) = convert(nvarchar(50), ep.INN) + '_' + convert(nvarchar(50),ep.CollectorId) collate Cyrillic_General_CI_AS
left join	(select sl.itemid, sl.Activedate, d.Name 
				from collect.dbo.StopList sl
				inner join collect.dbo.Dictionary d on d.id = sl.ReasonId
				where sl.ActiveStopList = 1 and sl.StopDate is null and sl.TypeId = 82 and sl.Pretendent = 0) as stl on stl.ItemId = t1.NKS
left join LegalCollection.dbo.GisAgency gis on ep.AgencyId = gis.id
where ep.CollectorId is not null and ep.INN is not null and t1.CollectorId is not null and t1.INN is not null and EPStateId in (637014, 637015) and (stl.Name is null or stl.Name = 'В работе Залогов')

order by ep.CheckDate desc , OpeningDate desc """

asvp_table = pd.read_sql_query(requestString, connection)
#IFERROR(IF(VLOOKUP(A227;'Полотно АСВП'!A:A;1;0)>1;1;0)


print(asvp_table)

