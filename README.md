# Formação em Engenharia de Dados, Data Science & BI

Seja bem-vindo(a) ao meu repositório de estudos e projetos práticos! Este espaço foi estruturado para consolidar meu aprendizado em todo o ecossistema de dados, cobrindo desde a extração e tratamento até a análise preditiva e visualização estratégica.

---

## 🚀 Tecnologias e Ferramentas Utilizadas

* **Linguagem de Programação:** Python (Pandas, NumPy, Matplotlib)
* **Banco de Dados & SQL:** Microsoft SQL Server (T-SQL, SSMS)
* **Engenharia de Dados & ETL:** SQL Server Integration Services (SSIS)
* **Business Intelligence (BI):** Power BI (Power Query, Modelagem de Dados, DAX)

---

## 📁 Organização do Repositório

O projeto está dividido em módulos que simulam o fluxo real de um ambiente corporativo de dados:

* **`0_Area_Execução/`**: Ambiente de testes rápidos e execução de scripts temporários.
* **`1_ Dados Originais/`**: Bases brutas (*raw data*) simulando recebimento de sistemas de origem (CSV, XLSX, TXT).
* **`2_ Dados Preparados/`**: Dados processados, limpos e padronizados prontos para armazenamento.
* **`3_ Dados de Upload/`**: Arquivos estruturados especificamente para cargas em bancos de dados.
* **`4_ Analises_Scripts_Sql/`**: Consultas analíticas, automações com Jobs do SQL Server, tratamentos de desvios e detecção de anomalias usando T-SQL.
* **`7_Arqs_SSIS/`**: Pacotes completos do Integration Services para automação de pipelines de ETL (ex: cargas de Clientes Banco e África do Sul).
* **`8_Dev_PY/`**: Notebooks Jupyter (`.ipynb`) focados em lógica de programação, manipulação avançada de DataFrames (Pandas/NumPy) e análise exploratória de dados.
* **`9_PBI/`**: Desenvolvimento de relatórios interativos, tratamento avançado no Power Query, tabela calendário e dashboards gerenciais com Power BI.
* **`99_Datasets/`**: Repositório central de conjuntos de dados utilizados ao longo dos estudos (ex: Contoso, Titanic, Game of Thrones).

---

## 📊 Destaques dos Projetos Desenvolvidos

### 🔹 Engenharia de Dados e ETL (SSIS)
Desenvolvimento de pacotes de integração para automação de carga de dados, lidando com grandes volumes de registros, tratamento de valores nulos e isolamento de anomalias críticas de negócios de forma automatizada.

### 🔹 Análise de Dados com Python
Uso das bibliotecas **Pandas** e **NumPy** para limpeza de dados, fusão de tabelas, tratamento de tipos e tratamento de séries temporais. Visualização de dados utilizando **Matplotlib** para geração de insights focados em tomada de decisão.

### 🔹 Inteligência de Negócios (Power BI)
Construção de painéis dinâmicos utilizando as melhores práticas de self-service BI: modelagem dimensional, criação de tabelas fato/dimensão, funções DAX avançadas e design focado na experiência do usuário (UX).

---

## 🛠️ Como Executar este Repositório

1. **Scripts SQL:** Podem ser executados diretamente no SQL Server Management Studio (SSMS).
2. **Notebooks Python:** Certifique-se de ter o ambiente Jupyter ou VS Code configurado com as bibliotecas Pandas e NumPy instaladas:
   ```bash
   pip install pandas numpy matplotlib
