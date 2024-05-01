use b3
go

select * from dbo.FIIS_Consol

ALTER TABLE dbo.FIIS_Consol 
DROP COLUMN "YIELD  3 MESES", "YIELD  6 MESES";


WITH CTE AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY "CÓDIGO", "NOME", "Valor da Ação", "Variação", "Data", "YIELD  1 MES",
	"YIELD  12 MESES", "DI Mensal" ORDER BY (SELECT 0)) AS rn
    FROM dbo.FIIS_Consol)
DELETE FROM CTE WHERE rn > 1;