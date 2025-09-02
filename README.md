
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

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- `data/`: Contém os bancos de dados SQLite.
  - `prouni.sqlite`: Banco de dados original com os dados brutos.
  - `clean_prouni.sqlite`: Banco de dados com os dados limpos e pré-processados, utilizado pela aplicação.
- `notebooks/`: Contém os Jupyter Notebooks utilizados para a limpeza e análise exploratória inicial dos dados.
- `src/`: Contém o código-fonte da aplicação.
  - `main.py`: Ponto de entrada da aplicação Streamlit (o dashboard interativo).
  - `utils.py`: Funções utilitárias para manipulação e carregamento de dados.
- `requirements.txt`: Lista de dependências do projeto.

## Dados

O banco de dados `clean_prouni.sqlite` contém duas tabelas principais:

- **`cursos`**: Armazena informações detalhadas sobre os cursos, incluindo nome, grau, turno, mensalidade, tipos de bolsa, notas de corte e informações sobre a universidade e o campus.
- **`enderecos`**: Armazena informações de endereço dos campi, como município, UF e telefone.

As tabelas são relacionadas pelo campo `campus_id`.

## Funcionalidades do Dashboard

O dashboard interativo (`src/main.py`) oferece as seguintes funcionalidades:

- **Filtros Dinâmicos**: Permite filtrar os dados por curso, estado (UF), universidade, período e nível.
- **Métricas Principais**: Exibe métricas importantes como total de cursos, mensalidades mínima e máxima, número de universidades, e totais de bolsas.
- **Rankings**: Gráficos de barras com o top 10 cursos e universidades por número de bolsas.
- **Análise de Mensalidades**: Gráfico de box plot para analisar a distribuição das mensalidades por período.
- **Relação Mensalidade vs. Bolsas**: Gráfico de dispersão para visualizar a correlação entre o valor da mensalidade e a quantidade de bolsas.
- **Distribuição de Bolsas**: Gráficos de rosca e sunburst para mostrar a proporção de bolsas por nível e tipo.
- **Análise Geográfica**: Mapa do Brasil (choropleth) com a média de mensalidades por estado e um gráfico de barras com a quantidade de bolsas (cotas vs. ampla concorrência) por estado.
- **Tabela de Dados**: Exibe os dados filtrados em uma tabela paginada.

## Visão Geral do Código

- **`src/main.py`**: É o coração da aplicação Streamlit. Ele define a interface do usuário, os filtros, as métricas e os gráficos que compõem o dashboard.
- **`src/utils.py`**: Contém funções auxiliares que são usadas no `main.py`. Isso inclui carregar dados do banco de dados, aplicar filtros, formatar valores monetários e de texto, e outras operações de pré-processamento.

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
