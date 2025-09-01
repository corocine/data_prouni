
# Análise de Dados do Prouni 2018

## Descrição do Projeto

Este projeto realiza uma análise exploratória dos dados do Programa Universidade para Todos (Prouni) em 2018. O objetivo é extrair insights sobre as bolsas de estudo oferecidas, os cursos, notas de corte, as mensalidades e a distribuição geográfica das instituições.

## Tecnologias Utilizadas

* **Linguagem**: Python
* **Bibliotecas de Análise**: pandas
* **Bibliotecas de Visualização**: Plotly
* **Dashboard**: Streamlit
* **Modelagem de Dados**: dbt (Data Build Tool)
* **Banco de Dados**: SQLite
* **Ambiente de Desenvolvimento**: Jupyter Notebook

## Instalação

Para executar este projeto localmente, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```
2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows, use: .venv\Scripts\activate
   ```
3. **Instale as dependências:**
   Como não há um arquivo `requirements.txt`, você pode instalar as bibliotecas necessárias manualmente:

   ```bash
   pip install pandas plotly streamlit dbt-sqlite jupyterlab
   ```
4. **Execute a análise:**
   Para explorar a análise de dados, inicie o Jupyter Lab:

   ```bash
   jupyter lab
   ```

   Para visualizar o dashboard interativo (se houver um script `app.py` ou similar):

   ```bash
   streamlit run <NOME_DO_ARQUIVO_STREAMLIT>.py
   ```
