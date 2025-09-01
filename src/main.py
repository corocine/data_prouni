import pandas as pd
import plotly.express as px
from pathlib import Path
import sqlite3
import streamlit as st
from utils import load_data_with_join, get_unique_values

#  ---- page config ----
db_path = Path.cwd() / 'data' / 'clean_prouni.sqlite'

st.set_page_config(
    page_title='Cursos Prouni 2018',
    layout='wide'
)

st.title('Cursos Prouni 2018')
st.subheader('Análise exploratória dos cursos disponíveis no PROUNI 2018')

#  ---- side bar config ----
st.sidebar.markdown("<h1 style='text-align: center;'> Preferências </h1>", unsafe_allow_html=True)

courses = get_unique_values(db_path, 'cursos', 'curso_busca')
states = get_unique_values(db_path, 'enderecos', 'uf')
level = get_unique_values(db_path, 'cursos', 'grau')
period = get_unique_values(db_path, 'cursos', 'turno')
school = get_unique_values(db_path, 'cursos', 'universidade_nome')
cities = get_unique_values(db_path, 'enderecos', 'municipio_limpo')

course_name_filter = st.sidebar.multiselect("Curso", options=courses)
states_filter = st.sidebar.multiselect("Estado (UF)", options=states)
school_filter = st.sidebar.text_input("Universidade")
period_filter = st.sidebar.multiselect("Períodos", options=period)
level = st.sidebar.multiselect("Grau", options=level)

active_filters = {}

if course_name_filter:
    active_filters['c.curso_busca'] = course_name_filter

if states_filter:
    active_filters['e.uf'] = states_filter

if school_filter:
    active_filters['c.universidade_nome'] = school_filter

if level:
    active_filters['c.grau'] = level

if period_filter:
    active_filters['c.turno'] = period_filter
    
    
# ---- dashboard config ---- 
df_filtred = load_data_with_join(db_path, filters=active_filters)

st.sidebar.subheader(f"**Registros encontrados: {len(df_filtred)}**")
st.markdown('---')

total_courses = len(df_filtred['curso'].unique())
st.metric('Cursos', total_courses)


if not df_filtred.empty:
    st.markdown('---')
    page_size = 10000  
    page_number = st.number_input("Página", min_value=1, value=1, label_visibility="collapsed", width=130 )
    start_idx = (page_number - 1) * page_size
    end_idx = min(start_idx + page_size, len(df_filtred))
    st.dataframe(df_filtred.iloc[start_idx:end_idx])
else:
    st.warning("Nenhum resultado encontrado para os filtros aplicados.")
