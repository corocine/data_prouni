import streamlit as st
import pandas as pd
from src.utils import format_to_brazilian_currency, replace_comma_with_dot

def show_metrics(df_filtred: pd.DataFrame):
    """
    Displays the metrics panel on the dashboard.

    Args:
        df_filtred (pd.DataFrame): The filtered DataFrame with the data to be displayed.
    """
    met1, met2, met3, met4  = st.columns(4)

    with met1:
        total_courses = len(df_filtred['curso'].unique())
        st.metric('Cursos', total_courses)
        
    with met2:
        min_monthly_fee = float(df_filtred['mensalidade'].min())
        st.metric('Mensalidade mínima', format_to_brazilian_currency(min_monthly_fee))
        
    with met3:
        max_monthly_fee = df_filtred['mensalidade'].max()
        st.metric('Mensalidade máxima', format_to_brazilian_currency(max_monthly_fee))
        
    with met4:
        total_universidades = len(df_filtred['universidade'].unique())
        st.metric('Universidades', total_universidades)

    met5, met6, met7 ,met8 = st.columns(4)

    with met5:
        mais_frequente_curso: str = str(df_filtred['curso'].value_counts().first_valid_index())
        st.metric('Curso mais ofertado nas universidades', mais_frequente_curso)

    with met6:
        total_cotas = df_filtred['bolsa_integral_cotas'].sum() + df_filtred['bolsa_parcial_cotas'].sum()
        st.metric('Total bolsas para cotas', replace_comma_with_dot(total_cotas))

    with met7:
        total_bolsas = df_filtred['bolsa_integral'].sum() + df_filtred['bolsa_parcial'].sum()
        st.metric('Total de bolsas', replace_comma_with_dot(total_bolsas))

    with met8:
        estado_mais_frequente: str = str(df_filtred['estado'].value_counts().first_valid_index())
        st.metric('Estado mais frequente', estado_mais_frequente)
        
    st.markdown('---')
