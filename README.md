
# Análise de Dados do Prouni 2018

## Descrição do Projeto

Este projeto realiza uma análise exploratória dos dados do Programa Universidade para Todos (Prouni) em 2018. O objetivo é extrair insights sobre as bolsas de estudo oferecidas, os cursos, notas de corte, as mensalidades e a distribuição geográfica das instituições através de um dashboard interativo.

## Tecnologias Utilizadas

* **Linguagem**: Python
* **Bibliotecas de Análise**: pandas
* **Bibliotecas de Visualização**: Plotly
* **Dashboard**: Streamlit
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
   Use o arquivo `requirements.txt` para instalar as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```
4. **Execute o Dashboard:**
   Para visualizar o dashboard interativo, execute o seguinte comando:

   ```bash
   streamlit run src/main.py
   ```

   Para explorar a análise de dados nos notebooks, inicie o Jupyter Lab:

   ```bash
   jupyter lab
   ```
