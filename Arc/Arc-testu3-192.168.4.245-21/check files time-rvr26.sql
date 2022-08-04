use env
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP 50000 [Tab_Id]
      ,[Tab_TabularTag]
      ,[Tab_DateTime]
      ,[Tab_DateTime_Source]
      ,[Tab_Value_monRVR]
      ,[Tab_Value_monRVR10L]
      ,[Tab_Value_mTime]
      ,[Tab_Value_mTimeN]
  FROM [env].[dbo].[MeteoTabulartabtRVR] where [Tab_TabularTag]='65_F1R26_RVR'
  order by Tab_DateTime desc