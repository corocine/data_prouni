import streamlit as st
from ..utils import get_unique_values, replace_comma_with_dot

def show_sidebar(db_path):
    """
    Displays the sidebar with filters and returns active filters.

    Args:
        db_path (str or Path): The path to the SQLite database.

    Returns:
        dict: A dictionary with active filters.
    """
    st.sidebar.markdown("<h1 style='text-align: center;'> Preferências </h1>", unsafe_allow_html=True)

    courses = get_unique_values(db_path, 'cursos', 'curso_busca')
    states = get_unique_values(db_path, 'enderecos', 'uf')
    level_filter_options = get_unique_values(db_path, 'cursos', 'grau')
    period = get_unique_values(db_path, 'cursos', 'turno')
    school = get_unique_values(db_path, 'cursos', 'universidade_nome')

    course_name_filter = st.sidebar.multiselect("Curso", options=courses)
    states_filter = st.sidebar.multiselect("Estado (UF)", options=states)
    school_filter = st.sidebar.multiselect("Universidade", options=school)
    period_filter = st.sidebar.multiselect("Períodos", options=period)
    level_filter = st.sidebar.multiselect("Grau", options=level_filter_options)

    active_filters = {}

    if course_name_filter:
        active_filters['c.curso_busca'] = course_name_filter
    if states_filter:
        active_filters['e.uf'] = states_filter
    if school_filter:
        active_filters['c.universidade_nome'] = school_filter
    if level_filter:
        active_filters['c.grau'] = level_filter
    if period_filter:
        active_filters['c.turno'] = period_filter
    
    return active_filters

def show_record_count(df_filtred): 
    """
    Displays the count of records found in the sidebar.

    Args:
        df_filtred (pd.DataFrame): The filtered DataFrame.
    """
    search_size = len(df_filtred)
    st.sidebar.write(f"Registros encontrados: {replace_comma_with_dot(search_size)}")
