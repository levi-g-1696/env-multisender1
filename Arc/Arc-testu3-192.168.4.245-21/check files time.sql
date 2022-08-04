use env
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP 1000 [Tab_Id]
      ,[Tab_TabularTag]
      ,[Tab_DateTime]
      ,[Tab_DateTime_Source]
      ,[Tab_Value_monRVR]
      ,[Tab_Value_monRVR10L]
      ,[Tab_Value_mTime]
      ,[Tab_Value_mTimeN]
  FROM [env].[dbo].[MeteoTabularttRVR]
  order by Tab_DateTime desc