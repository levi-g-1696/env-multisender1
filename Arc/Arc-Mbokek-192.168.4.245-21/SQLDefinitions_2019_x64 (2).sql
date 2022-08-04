DECLARE
@DBPath varchar(8000),
@DBPathLog varchar(8000),
@sql varchar(8000)

--SET @DBPath = 'D:\DB\IGSOG\sql 2019'
--SET @DBPathlog = 'D:\DB\IGSOG\sql 2019'
SET @DBPath = 'd:\datalogger\db'
SET @DBPathlog = 'c:\datalogger\db'



SET @sql = 'RESTORE FILELISTONLY FROM DISK = ''' + @DBPath + '\IgSog.bak''

RESTORE DATABASE IgSog FROM DISK = ''' + @DBPath + '\IgSog.bak''
WITH MOVE ''IgSog'' TO ''' + @DBPath + '\IgSog.mdf'',
MOVE ''IgSog_Log'' TO ''' + @DBPath + '\IgSog_log.ldf''
'
--select(@sql)
print @sql
exec(@sql)


SET @sql = 'RESTORE FILELISTONLY FROM DISK = ''' + @DBPath + '\caching.bak''

RESTORE DATABASE caching FROM DISK = ''' + @DBPath + '\caching.bak''
WITH MOVE ''caching'' TO ''' + @DBPath + '\caching.mdf'',
MOVE ''caching_Log'' TO ''' + @DBPath + '\caching_log.ldf''
'
print @sql
exec(@sql)

SET @sql = 'RESTORE FILELISTONLY FROM DISK = ''' + @DBPath + '\aspnetdb.bak''

RESTORE DATABASE aspnetdb FROM DISK = ''' + @DBPath + '\aspnetdb.bak''
WITH MOVE ''aspnetdb'' TO ''' + @DBPath + '\aspnetdb.mdf'',
MOVE ''aspnetdb_Log'' TO ''' + @DBPath + '\aspnetdb_log.ldf''
'
print @sql
exec(@sql)


SET @sql = 'RESTORE FILELISTONLY FROM DISK = ''' + @DBPath + '\Env.dat_bak''

RESTORE DATABASE env FROM DISK = ''' + @DBPath + '\Env.dat_bak''
WITH MOVE ''Env_Data'' TO ''' + @DBPath + '\Env.mdf'',
MOVE ''Env_Log'' TO ''' + @DBPathLog + '\Env_log.ldf''
'
--select(@sql)
print @sql
exec(@sql)

go

sp_configure 'show advanced options', 1
go
reconfigure 
go

sp_configure 'Ad Hoc Distributed Queries', 1 
go
reconfigure 
go

use master

----before this check the database level. Must be > 80
--ALTER DATABASE env SET COMPATIBILITY_LEVEL = 120
--ALTER DATABASE caching SET COMPATIBILITY_LEVEL = 120
--ALTER DATABASE aspnetdb SET COMPATIBILITY_LEVEL = 120
--ALTER DATABASE IgSog SET COMPATIBILITY_LEVEL = 120
--go

EXEC sp_configure 'clr enabled', '1'
go

RECONFIGURE
go


exec  sp_configure 'clr strict security', '0'

go

RECONFIGURE
go