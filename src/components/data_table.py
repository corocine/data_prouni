import streamlit as st
import pandas as pd

def show_data_table(df_filtred: pd.DataFrame):
    """
    
    Displays the data table with pagination.

    Args:
        df_filtred (pd.DataFrame): The filtered DataFrame with the data to be displayed.
    """
    if not df_filtred.empty:
        st.markdown('---')
        page_size = 10000  
        page_number = st.number_input("Página", min_value=1, value=1, label_visibility="collapsed", width=130 )
        start_idx = (page_number - 1) * page_size
        end_idx = min(start_idx + page_size, len(df_filtred))
        st.dataframe(df_filtred.iloc[start_idx:end_idx])
    else:
        st.warning("Nenhum resultado encontrado para os filtros aplicados.")
