USE [DS_DATASCIENSE_TST]

SELECT * FROM [dbo].[RAW_CLIENTE_AFRICA_SUL];
GO

SELECT COUNT (*) FROM [dbo].[RAW_CLIENTE_AFRICA_SUL];

DELETE FROM [dbo].[RAW_CLIENTE_AFRICA_SUL];

SELECT TOP (1000) * FROM [dbo].[RAW_CLIENTE_AFRICA_SUL]



SELECT TOP (1000) *
FROM [DS_DATASCIENSE_TST].[dbo].[RAW_Anomalias_ClienteAfrica]


SELECT COUNT(*) FROM  [dbo].[RAW_Anomalias_ClienteAfrica];


DELETE FROM [dbo].[RAW_Anomalias_ClienteAfrica];


SELECT 
SUM(TRY_CAST([AmountPaid] AS DECIMAL(10, 2))) AS TOTAL_VENDAS 
FROM [dbo].[RAW_Anomalias_ClienteAfrica];


SELECT 
SUM(TRY_CAST(REPLACE([AmountPaid], ',', '.') AS DECIMAL(10,2)))AS TOTAL_VENDAS 
FROM [dbo].[RAW_Anomalias_ClienteAfrica];


ALTER TABLE [dbo].[RAW_Anomalias_ClienteAfrica] DROP COLUMN 
    [Password],
    [BrowserUserAgent],
    [NationalID],
    [UPS],
    [WesternUnionMTCN],
    [MoneyGramMTCN],
    [GUID],
    [Latitude],
    [Longitude],
    [Coluna 46];
GO


SELECT [AmountPaid] 
FROM [dbo].[RAW_Anomalias_ClienteAfrica]
WHERE TRY_CAST([AmountPaid] AS DECIMAL(10,2)) IS NULL AND [AmountPaid] IS NOT NULL;



-- verificando regra de negocio se campos  NameSet,Gender, Zipcode, Country, ContryFull { os que estao vazios }  e  AmountPaid { se existe diferente do formto %.% }
-- efetue  ISS a regra de split  condicional  ->  Divisao Condicional _> direcionando as anomalias para um arquivo
-- NOT LIKE '%' = DIFERENTE DE PREENCHIDO  OR VAZIO
-- NOT LIKE '%.%' = DIFERENTE DE FORMATO QUE CONTENHA ALGO PONTO E CONTENHA ALGO APOS O PONTO

SELECT *
FROM [DS_DATASCIENSE_TST].[dbo].[RAW_ClienteAfrica_OK]
WHERE [NameSet] NOT LIKE '%'
OR [AmountPaid] NOT LIKE '%.%'
OR [Gender] NOT LIKE '%'
OR [ZipCode] NOT LIKE '%'
OR [Country] NOT LIKE '%'
OR [CountryFull] NOT LIKE '%'


-- PELO MOTIVO IMPORTANTE  TENDO EM VISTA QUE IMPORTAMOS COM TEXTO  SENDO QUE TEXTO NAO EXISTE REGISTRO NULO {NILL}  E  SIM VAZIO { ' ' }
-- POR ESTE MOTIVO QUE NAO GERADO QUALQUER RETORNO DO SELECT ABAIXO.
-- POR ESTE MOTIVO UTILIZE LIKE PARA  IMPORTA��O DE ARQUIVOS TEXTO.

SELECT *
FROM [DS_DATASCIENSE_TST].[dbo].[RAW_ClienteAfrica_OK]
WHERE [Surname] IS NULL
OR[AmountPaid] IS NULL

SELECT * FROM [DS_DATASCIENSE_TST].[dbo].[RAW_Transacoes]


SELECT * FROM [dbo].[RAW_Transacoes]
ORDER BY CAST([Unit Price] AS FLOAT)
GO