USE B3 
GO

SELECT * FROM dbo.FIIS_Consol


CREATE VIEW FIIS_Classificados
AS
SELECT FIIS_Consol.*,
       FIIS_Classification.[SEGMENTO],
	   FIIS_Classification.[ADMINISTRADOR]
FROM dbo.FIIS_Consol
INNER JOIN dbo.FIIS_Classification ON FIIS_Consol.[CÓDIGO] = FIIS_Classification.[CÓDIGO];