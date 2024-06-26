USE [B3]
GO
/****** Object:  Trigger [dbo].[TRG_DeleteDuplicates]    Script Date: 01/05/2024 18:26:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER TRIGGER [dbo].[TRG_DeleteDuplicates]
ON [dbo].[FIIS_Consol]
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY "CÓDIGO", "NOME", "Valor da Ação", "Variação", "Data", "YIELD  1 MES",
	    "YIELD  12 MESES", "DI Mensal" ORDER BY (SELECT 0)) AS rn
        FROM dbo.FIIS_Consol
    )
    DELETE FROM CTE WHERE rn > 1;
END;