# Análise de Dados do Prouni 2018

Um dashboard interativo para análise exploratória de dados sobre os cursos e bolsas de estudo do Prouni em 2018.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.10%2B-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-1.4%2B-blue?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.9%2B-purple?style=for-the-badge&logo=plotly)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)

## 🔗 Link para Acesso

- Acesse o dashboard interativo através do link: https://dataprouni-gabrielcorocine.streamlit.app/

![Preview da analise de dados proposta pelo projeto](/home/gabriel/Documentos/Estudos/data_prouni/image/analysis.gif "Preview")

## 🚀 Sobre o Projeto

Este projeto oferece uma ferramenta de visualização de dados para explorar as oportunidades do Programa Universidade para Todos (Prouni) com base nos dados de 2018. O objetivo é fornecer insights claros sobre:

- Distribuição de bolsas de estudo.
- Valores de mensalidade por curso e região.
- Notas de corte.
- Distribuição geográfica das instituições.

## ✨ Funcionalidades

O dashboard interativo permite:

- **Filtros Dinâmicos**: Filtre os dados por curso, estado, universidade, turno e nível do curso.
- **Métricas Chave**: Visualize rapidamente o total de cursos, mensalidades, universidades e bolsas.
- **Rankings**: Descubra os 10 cursos e universidades com mais bolsas.
- **Análise de Mensalidades**: Entenda a distribuição dos valores das mensalidades.
- **Análise Geográfica**: Explore a distribuição de mensalidades e bolsas (cotas vs. ampla concorrência) no mapa do Brasil.
- **Visualização de Dados**: Navegue pelos dados detalhados em uma tabela interativa.

## 🛠️ Como Executar

Siga os passos abaixo para executar o projeto localmente.

1. **Clone o repositório:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_DIRETORIO>
   ```
2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```
3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Execute a aplicação:**

   ```bash
   streamlit run src/main.py
   ```

   A aplicação estará disponível em `http://localhost:8501`.

## 🗃️ Estrutura do Projeto

```
.
├── data/
│   ├── clean_prouni.sqlite  # Banco de dados utilizado pela aplicação
│   └── prouni.sqlite        # Banco de dados original
├── notebooks/
│   ├── table1.ipynb         # Notebooks para análise e limpeza
│   └── table2.ipynb
├── src/
│   ├── components/          # Módulos dos componentes do dashboard
│   ├── main.py              # Ponto de entrada da aplicação Streamlit
│   └── utils.py             # Funções utilitárias
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## 📊 Dados

Os dados foram extraídos de uma fonte pública e pré-processados para esta análise. O banco de dados limpo (`clean_prouni.sqlite`) contém tabelas sobre cursos e endereços das instituições, relacionando informações como nome do curso, mensalidade, notas de corte e localização.

- **Fonte**: [Brasil.io
  ](https://brasil.io/dataset/cursos-prouni/cursos/)

---

[Gabriel Corocine](https://github.com/corocine)
