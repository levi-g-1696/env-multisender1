USE [env]
GO

/****** Object:  UserDefinedFunction [dbo].[GetMeteoDatesSchemaEnd]    Script Date: 03/03/2021 9:00:06 ******/
SET ANSI_NULLS OFF
GO

SET QUOTED_IDENTIFIER ON
GO








CREATE      function [dbo].[GetMeteoDatesSchemaEnd](
@TimeIntervalType char(1),--Time interval Type ('d','h','m')
@TimeInterval int,--Time interval
@BaseTimeIntervalMin int,
@fromDate datetime,
@ToDate datetime
)
RETURNS
@DateTable TABLE (Date DateTime primary key)

--Return Date Table by requested time interval and period
--Call Example---------------------------------------------------
/*declare @fromDate datetime
declare @ToDate datetime
set @fromDate='01-oct-2004 00:00'
set @ToDate='02-nov-2004 14:00'

select * from GetMeteoDatesSchema('m',30,10,@fromDate,@ToDate)*/
--------------------------------------------------------------
as
begin

--set @fromDate='01-oct-2004 00:00'
--set @ToDate='02-nov-2004 14:00'
--set @TimeIntervalType = 'm'
--set @TimeInterval = 30

declare
@CurDate datetime

--Time Interval >= 10 min
if (@TimeIntervalType = 'm') and (@TimeInterval < @BaseTimeIntervalMin)
  set @TimeInterval = @BaseTimeIntervalMin
----set FromDate by interval begin with (00:00 m,01:00 h,01 d) + FromDate
--if ((DATEPART(SECOND,@fromDate)) > 0) --not periodic
	set @FromDate = dbo.GetMeteoDateByIntevalEnd(DATEADD(mi,@BaseTimeIntervalMin,@FromDate) ,@TimeIntervalType,@TimeInterval,@BaseTimeIntervalMin)  
--else
--begin
--  if (((DATEPART(HOUR,@fromDate)) = 0) and ((DATEPART(MINUTE,@fromDate)) = 0))
--    set @FromDate = DateAdd(mi,-@BaseTimeIntervalMin,@FromDate)
--  set @FromDate = 
--  --dbo.GetMeteoDateByInteval(@FromDate,@TimeIntervalType,@TimeInterval) 
--  case @TimeIntervalType
--    when 'd' then DateAdd(d,(((DATEPart(d, @FromDate)-1) / @TimeInterval)* @TimeInterval) + @TimeInterval,CONVERT(char(8),  @FromDate, 20) + '01')
--    when 'h' then DateAdd(hh,((DATEPart(hh, @FromDate) / @TimeInterval)* @TimeInterval) + @TimeInterval,CONVERT(char(10),  @FromDate, 20))
--    when 'm' then DateAdd(mi,((DATEPart(mi, @FromDate) / @TimeInterval)* @TimeInterval) + @TimeInterval,(CONVERT(char(13),  @FromDate, 20) + ':00'))
--    else DateAdd(mi,((DATEPart(mi, @FromDate) / @TimeInterval)* @TimeInterval) + @TimeInterval,(CONVERT(char(13),  @FromDate, 20) + ':00')) -- error Timer interval type,set time interval = 5 min
--  end
--end

set @CurDate = @FromDate


--fill result table
while @CurDate <= @ToDate
begin
  insert into @DateTable (Date) values(@CurDate)

  select @CurDate =
  --case @TimeIntervalType
  --  when 'd' then DATEADD(dd,@TimeInterval,@CurDate )
  --  when 'h' then DATEADD(hh,@TimeInterval,@CurDate )
  --  when 'm' then DATEADD(mi,@TimeInterval,@CurDate )
  --  else DATEADD(mi,@BaseTimeIntervalMin,@CurDate ) -- error Timer interval type,set time interval = 5 min
  --end
 case @TimeIntervalType
    when 'd' then DateAdd(d,(((DATEPart(d, @CurDate)-1) / @TimeInterval)* @TimeInterval) + @TimeInterval,CONVERT(char(8),  @CurDate, 20) + '01')
    when 'h' then DateAdd(hh,((DATEPart(hh, @CurDate) / @TimeInterval)* @TimeInterval) + @TimeInterval,CONVERT(char(10),  @CurDate, 20))
    when 'm' then DateAdd(mi,((DATEPart(mi, @CurDate) / @TimeInterval)* @TimeInterval) + @TimeInterval,(CONVERT(char(13),  @CurDate, 20) + ':00'))
    else DateAdd(mi,((DATEPart(mi, @CurDate) / @TimeInterval)* @TimeInterval) + @TimeInterval,(CONVERT(char(13),  @CurDate, 20) + ':00')) -- error Timer interval type,set time interval = 5 min
  end
  --dbo.GetMeteoDateByIntevalEnd( @CurDate, @TimeIntervalType, @TimeInterval)


end

  return

end



GO


