USE [env]
GO

/****** Object:  UserDefinedFunction [dbo].[GetMeteoDateByIntevalEnd]    Script Date: 03/03/2021 14:46:02 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER OFF
GO





-- IF OBJECT DOES NOT EXIST USE "CREATE" in place of "ALTER"
alter     FUNCTION [dbo].[GetMeteoDateByIntevalEnd]
--Conver Date to Date by time interval
     (
      @Date datetime,
      @TimeIntervalType char(1),--Time interval Type ('d','h','m')
      @IntervalTime int,
	  @BaseTimeInterval int
     )
RETURNS datetime
AS
begin

declare 
@Result datetime
set @Date = DateAdd(mi,-@BaseTimeInterval,@Date);

  select @Result =
  case @TimeIntervalType
    when 'd' then DateAdd(d,(((DATEPart(d,@Date)-1) / @IntervalTime)* @IntervalTime) + @IntervalTime,CONVERT(char(8), @Date, 20) + '01')
    when 'h' then DateAdd(hh,((DATEPart(hh,@Date) / @IntervalTime)* @IntervalTime) + @IntervalTime,CONVERT(char(10), @Date, 20))
    when 'm' then DateAdd(mi,((DATEPart(mi,@Date) / @IntervalTime)* @IntervalTime) + @IntervalTime,(CONVERT(char(13), @Date, 20) + ':00'))
    else DateAdd(mi,((DATEPart(mi,@Date) / @IntervalTime)* @IntervalTime) + @IntervalTime,(CONVERT(char(13), @Date, 20) + ':00')) -- error Timer interval type,set time interval = 5 min
  end

--set @Result = CONVERT(char(13), @Date, 20) + ':00'
--select @Result = DateAdd(mi,((DATEPart(mi,@Date) / @IntervalTime)* @IntervalTime),(CONVERT(char(13), @Date, 20) + ':00'))

RETURN @result
end

/*
declare 
  @result datetime,
  @Date datetime,
  @IntervalTime int,
  @Part int
set @Date = '22-nov-2003 00:59'
set @IntervalTime = 2

set @Result = CONVERT(char(8), @Date, 20) + '01'
select @Result
select @Result = DateAdd(d,(((DATEPart(d,@Date)-1) / @IntervalTime)* @IntervalTime),CONVERT(char(8), @Date, 20) + '01')
select @Result

*/






GO


