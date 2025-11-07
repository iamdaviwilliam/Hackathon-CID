Com certeza. Eu analisei os arquivos do seu projeto, especialmente o `ETL.ipynb` e o `etl/extract.py`, para extrair os resultados e metodologias corretos.

Atualizei a fonte de dados (estava usando um link do Kaggle diferente do que o script `extract.py` utiliza), preenchi a seção de "Principais Descobertas" com os dados do seu notebook (saídas das células 12 e 13) e atualizei a lista de tecnologias para incluir PySpark e Kaggle API, que são centrais para o projeto.

Também adicionei as instruções para configurar a API do Kaggle, conforme você solicitou.

Aqui está a versão completa e atualizada do seu `readme.md`:

-----

# 📊 Decifrando o Profissional de Dados: Uma Análise de Vagas no LinkedIn

## 🎯 1. Objetivo do Projeto

Este projeto foi desenvolvido durante o **carrers in data** com o objetivo principal de analisar o mercado de trabalho para profissionais de dados (Data Scientists, Data Analysts, Data Engineers, etc.).

Utilizando um conjunto de dados de vagas publicadas no LinkedIn, buscamos identificar e dissecar quais são as **características, habilidades técnicas (hard skills) e habilidades comportamentais (soft skills)** mais esperadas e valorizadas pelas empresas atualmente.

## ❓ 2. O Problema

O campo de dados está em constante e rápida evolução. Para aspirantes que desejam entrar na área e para profissionais que buscam se manter atualizados, surge a pergunta central:

> **"Quais são as competências essenciais que definem um profissional de dados competitivo no mercado atual?"**

Este projeto visa responder a essa pergunta por meio de uma análise quantitativa e qualitativa das descrições de vagas reais.

## 💾 3. Fonte de Dados

A análise é baseada no conjunto de dados público **"LinkedIn Job Postings Dataset"**, disponível na plataforma Kaggle. Este dataset foi extraído pelo script `etl/extract.py`.

  * **Link do Dataset:** [Kaggle - LinkedIn Job Postings Dataset](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)

Este dataset agrega milhares de postagens de vagas, contendo informações valiosas como:

  * Título do Cargo (Job Title)
  * Descrição da Vaga (Job Description)
  * Empresa (Company)
  * Localização (Location)
  * Nível de Senioridade (Seniority Level)
  * E outras informações relevantes.

## 🛠️ 4. Metodologia e Análise

Nossa abordagem para extrair insights dos dados, implementada no notebook `ETL.ipynb` usando PySpark, seguiu as seguintes etapas:

1.  **Extração (Extract):**

      * Download e extração automática dos dados do Kaggle utilizando a API oficial (conforme `etl/extract.py`).

2.  **Pré-processamento e Limpeza (Transform):**

      * Carregamento dos dados em um DataFrame Spark.
      * Tratamento de valores ausentes (NaN) e duplicados.
      * Correção e conversão (cast) dos tipos de dados (ex: salários para `double`, datas para `timestamp`).

3.  **Análise Exploratória de Dados (EDA) & Extração de Habilidades:**

      * Análise de vagas por nível de senioridade, tipo de contrato e modalidade (remoto vs. presencial).
      * **Mapeamento de Hard Skills:** Definição de uma lista-catálogo de tecnologias (Python, SQL, Spark, etc.). A descrição de cada vaga foi tokenizada e cruzada com essa lista para identificar as tecnologias mencionadas.
      * **Mapeamento de Soft Skills:** Extração e contagem das habilidades listadas na coluna `skills_desc`.

4.  **Visualização e Carga (Load):**

      * Agregação dos dados para sumarizar as descobertas.
      * Criação de um DataFrame final e exportação para `transformed_postings.csv` para consumo futuro (ex: dashboards).

## 📈 5. Principais Descobertas (Resultados)

A análise realizada no notebook `ETL.ipynb` revelou os seguintes insights:

  * **Quais são as 10 Hard Skills (tecnologias) mais demandadas?**
    *Nota: Com base na contagem de vagas em que a tecnologia foi mencionada (extraído da Célula 13 do notebook).*

    1.  **R** (5.210 vagas)
    2.  **SQL** (5.181 vagas)
    3.  **Python** (4.647 vagas)
    4.  **Spark** (856 vagas)
    5.  **Hadoop** (313 vagas)
    6.  **PyTorch** (243 vagas)
    7.  **TensorFlow** (224 vagas)
    8.  **BigQuery** (101 vagas)
    9.  **Pandas** (95 vagas)
    10. **NumPy** (85 vagas)

  * **Qual a proporção de vagas que exigem "Python" vs. "R"?**

      * Os dados mostraram uma leve preferência por **R (5.210 vagas)** em comparação com **Python (4.647 vagas)** no dataset analisado.

  * **Quais as Soft Skills (ou habilidades gerais) mais citadas?**
    *Nota: Com base na contagem da coluna `skills_desc` (extraído da Célula 12 do notebook). A alta frequência de termos de saúde sugere que o dataset original é amplo e não se limita a vagas de tecnologia.*

    1.  People Skills (74 menções)
    2.  Healthcare (65 menções)
    3.  Hospice Care (60 menções)
    4.  Patient Care (56 menções)
    5.  Fundraising (53 menções)
    6.  Verbal / Written Communication (53 menções)

## 🚀 6. Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes ferramentas e bibliotecas:

## 📂 7. Como Executar o Projeto

Para replicar esta análise, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone [URL-DO-SEU-REPOSITÓRIO]
    cd [NOME-DO-REPOSITÓRIO]
    ```

2.  **Configure a API do Kaggle:**

      * Faça login no [Kaggle](https://www.kaggle.com).
      * Vá até seu perfil, clique em "Account" e na seção "API", clique em "Create New API Token".
      * Isso fará o download do arquivo `kaggle.json`.
      * Coloque este arquivo no local esperado pela API.
          * **Linux/Mac:** `~/.kaggle/kaggle.json`
          * **Windows:** `C:\Users\<SeuUsuario>\.kaggle\kaggle.json`
      * (Certifique-se de definir as permissões corretas para o arquivo, se necessário: `chmod 600 ~/.kaggle/kaggle.json`)

3.  **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    .\venv\Scripts\activate   # Para Windows
    ```

4.  **Instale as dependências:**
    *O projeto depende de `pyspark`, `pandas`, `pyarrow` e `kaggle`.*

    ```bash
    pip install pyspark pandas pyarrow kaggle
    ```

    *(Opcional: crie um arquivo `requirements.txt` com essas dependências e rode `pip install -r requirements.txt`)*

5.  **Execute o script de Extração (ETL):**
    *Este script baixará os dados do Kaggle para a pasta `data/`.*

    ```bash
    python etl/extract.py
    ```

6.  **Execute os Notebooks:**
    Abra o Jupyter Lab (ou VS Code) e execute o notebook `ETL.ipynb` para processar os dados e gerar o arquivo `transformed_postings.csv`.

    ```bash
    jupyter lab
    ```

## 👥 8. Equipe

  * Deivyson Gomes
  * Davi Silva
  * Gustavo Henrique
  * Gabriel Estrela
  * Antônio Ramalho