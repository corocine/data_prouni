import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
from src.utils import load_data_with_join
from src.components.sidebar import show_sidebar, show_record_count
from src.components.metrics import show_metrics
from src.components.charts import show_charts
from src.components.data_table import show_data_table

def main():
    """
    Main function that orchestrates the creation and display of the dashboard.
    """
    # ---- Page configuration ----
    db_path = Path.cwd() / 'data' / 'clean_prouni.sqlite'
    st.set_page_config(
        page_title='Cursos Prouni 2018',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.title('Cursos Prouni 2018')
    st.subheader('Análise exploratória dos cursos e bolsas de estudos disponíveis no PROUNI 2018')

    # ---- Sidebar and Filters ----
    active_filters = show_sidebar(db_path)

    # ---- Data Loadings ----
    df_filtred = load_data_with_join(db_path, filters=active_filters)
    
    # ---- Dashboard ----
    if df_filtred.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
        st.stop()

    show_record_count(df_filtred)

    show_metrics(df_filtred)

    show_charts(df_filtred)

    show_data_table(df_filtred)

if __name__ == "__main__":
    main()
