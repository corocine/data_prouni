import pandas as pd
import plotly.express as px
from pathlib import Path
import sqlite3
import streamlit as st
from utils import load_data_with_join, get_unique_values, format_to_brazilian_currency, replace_comma_with_dot
import requests

#  ---- page config ----
db_path = Path.cwd() / 'data' / 'clean_prouni.sqlite'

st.set_page_config(
    page_title='Cursos Prouni 2018',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('Cursos Prouni 2018')
st.subheader('Análise exploratória dos cursos e bolsas de estudos disponíveis no PROUNI 2018')

#  ---- side bar and filters config ----
st.sidebar.markdown("<h1 style='text-align: center;'> Preferências </h1>", unsafe_allow_html=True)

courses = get_unique_values(db_path, 'cursos', 'curso_busca')
states = get_unique_values(db_path, 'enderecos', 'uf')
level_filter = get_unique_values(db_path, 'cursos', 'grau')
period = get_unique_values(db_path, 'cursos', 'turno')
school = get_unique_values(db_path, 'cursos', 'universidade_nome')

course_name_filter = st.sidebar.multiselect("Curso", options=courses)
states_filter = st.sidebar.multiselect("Estado (UF)", options=states)
school_filter = st.sidebar.multiselect("Universidade", options=school)
period_filter = st.sidebar.multiselect("Períodos", options=period)
level_filter = st.sidebar.multiselect("Grau", options=level_filter)

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
    
# ---- dashboard config ---- 
df_filtred = load_data_with_join(db_path, filters=active_filters)

if df_filtred.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

search_size = len(df_filtred)
st.sidebar.write(f"Registros encontrados: {replace_comma_with_dot(search_size)}")

#  ----- metrics ------
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

#  ------ grafics ------

PRIMARY_COLOR = "#0F90DB"  
SECONDARY_COLOR = "#AE25EE"
THIRD_COLOR = "#06CA96"  
ORANGE_COLOR = "#FF7C25"
YELLOW_COLOR = "#FFD82C"
GRAY_COLOR = '#999999'
SCHOLARSHIP_TYPE_COLOR = {'Bolsas para Cotas': SECONDARY_COLOR, 'Ampla Concorrência': PRIMARY_COLOR}
SCALE_COLOR_MAP = 'Blues'
CATEGORIES_COLORS = [PRIMARY_COLOR, SECONDARY_COLOR, THIRD_COLOR, ORANGE_COLOR, YELLOW_COLOR, GRAY_COLOR]

graphic1, graphic2 = st.columns(2)
df_graphics_ranking = df_filtred.copy()

with graphic1:    
    columns_to_sum = [
        'bolsa_integral_cotas',
        'bolsa_parcial_cotas',
        'bolsa_integral',
        'bolsa_parcial'
    ]
    
    df_graphics_ranking['total_bolsas'] = df_graphics_ranking[columns_to_sum].sum(axis=1)

    ranking_schools = df_graphics_ranking.groupby('universidade')['total_bolsas'].sum().nlargest(10).sort_values(ascending=True)
    
    if not ranking_schools.empty:
        fig_ranking_schools = px.bar(
            ranking_schools,
            x='total_bolsas',
            y=ranking_schools.index,
            orientation='h',
            labels={'total_bolsas': 'Total de Bolsas', 'y': 'Universidade'},
            text='total_bolsas',
            color_discrete_sequence=[PRIMARY_COLOR]
        )
        
        fig_ranking_schools.update_traces(
            hovertemplate='<b>Universidade:</b> %{y}<br><b>Total de Bolsas:</b> %{x:,.0f}<extra></extra>',
            texttemplate='%{x:,.0f}',
            textposition='outside'
        )
        
        fig_ranking_schools.update_layout(
            title_text="Top 10 Cursos por Total de Bolsas",
            title_x=0.5,         
            title_xanchor="center"
        )
        
        st.plotly_chart(fig_ranking_schools, use_container_width=True)
    else:
        st.warning("Nenhum dado de universidade para exibir com os filtros atuais.")

with graphic2:
    
    ranking_courses = df_graphics_ranking.groupby('curso')['total_bolsas'].sum().nlargest(10).sort_values(ascending=True)

    if not ranking_courses.empty:
        fig_ranking_courses = px.bar(
            ranking_courses,
            x='total_bolsas',
            y=ranking_courses.index,
            orientation='h',
            labels={'total_bolsas': 'Total de Bolsas', 'y': 'Curso'},
            text='total_bolsas',
            color_discrete_sequence=[PRIMARY_COLOR]
        )
        
        fig_ranking_courses.update_traces(
            hovertemplate='<b>Curso:</b> %{y}<br><b>Total de Bolsas:</b> %{x:,.0f}<extra></extra>',
            texttemplate='%{x:,.0f}',
            textposition='outside'
        )
        
        fig_ranking_courses.update_layout(
            title_text="Top 10 Cursos por Total de Bolsas",
            title_x=0.5,         
            title_xanchor="center"
        )
        st.plotly_chart(fig_ranking_courses, use_container_width=True)
    else:
        st.warning("Nenhum dado de curso para exibir com os filtros atuais.")

st.markdown('---')

st.subheader("Distribuição de Mensalidades por período")
st.info("Períodos de ensino influenciam no preço?")

if 'mensalidade' in df_filtred.columns and 'período' in df_filtred.columns:
    fig_monthy_fee = px.box(df_filtred,
                x='período', 
                y='mensalidade', 
                color='período',
                labels={'mensalidade': 'Mensalidade (R$)', 'período': 'período do Curso'},
                color_discrete_sequence=CATEGORIES_COLORS
                )
    st.plotly_chart(fig_monthy_fee, use_container_width=True)

st.markdown("---")

st.subheader("Relação entre Mensalidade e Número de Bolsas")
st.info("Cursos mais caros oferecem mais ou menos bolsas?")

df_scatter = df_graphics_ranking.copy()

fig_scatter = px.scatter(
        df_scatter,
        x='mensalidade',
        y='total_bolsas',
        color='nível', 
        labels={'mensalidade': 'Valor da Mensalidade (R$)', 'total_bolsas': 'Nº Total de Bolsas'},
        hover_data=['universidade', 'curso', 'nível'],
        color_discrete_sequence=CATEGORIES_COLORS
    )

fig_scatter.update_traces(
    hovertemplate='<b>%{customdata[0]}</b><br>' +
                  '<b>Curso:</b> %{customdata[1]}<br>' +
                  '<b>Nível:</b> %{customdata[2]}<br>' +
                  '<b>Mensalidade:</b> R$ %{x:,.2f}<br>' +
                  '<b>Total de Bolsas:</b> %{y:,.0f}<extra></extra>'
)


st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown('---')

graphic3, graphic4 = st.columns([0.4, 0.6]) 

with graphic3:
    st.subheader("Proporção de Bolsas por Nível")
    st.info("Qual nível de curso possui mais bolsas?")
    
    df_level_copy = df_filtred.copy()
    columns_to_sum = ['bolsa_integral_cotas', 'bolsa_parcial_cotas', 'bolsa_integral', 'bolsa_parcial']
    df_level_copy['total_bolsas'] = df_level_copy[columns_to_sum].sum(axis=1)

    df_level_distribution = df_level_copy.groupby('nível')['total_bolsas'].sum().reset_index()

    if not df_level_distribution.empty and df_level_distribution['total_bolsas'].sum() > 0:
        fig_donut_level = px.pie(
            df_level_distribution, 
            names='nível', 
            values='total_bolsas', 
            hole=0.3, 
            color='nível', 
            color_discrete_sequence=CATEGORIES_COLORS
        )
        fig_donut_level.update_traces(
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Quantidade: %{value:,.0f}<br>Percentual: %{percent:.1%}<extra></extra>'
        )
        st.plotly_chart(fig_donut_level, use_container_width=True)
    else:
        st.warning("Não há dados de nível para exibir com os filtros atuais.")
        
with graphic4:
    st.subheader("Distribuição por Tipo de Bolsa e Estado")
    st.info("Quais tipos de bolsas são mais ofertadas por estado?")

    columns_to_melt = [
        'bolsa_integral_cotas', 'bolsa_parcial_cotas',
        'bolsa_integral', 'bolsa_parcial'
    ]

    df_long_format = pd.melt(
        df_filtred,
        id_vars=['estado'],
        value_vars=columns_to_melt,
        var_name='tipo_bolsa',
        value_name='quantidade'
    )

    scholarship_name_map = {
        'bolsa_integral_cotas': 'Integral - Cotas',
        'bolsa_parcial_cotas': 'Parcial - Cotas',
        'bolsa_integral': 'Integral - Ampla',
        'bolsa_parcial': 'Parcial - Ampla'
    }
    df_long_format['tipo_bolsa'] = df_long_format['tipo_bolsa'].map(scholarship_name_map)
    df_long_format = df_long_format[df_long_format['quantidade'] > 0]

    if not df_long_format.empty:
        fig_sunburst = px.sunburst(
            df_long_format,
            path=['tipo_bolsa', 'estado'], 
            values='quantidade',
            color='tipo_bolsa',
            color_discrete_sequence=CATEGORIES_COLORS
        )
        
        fig_sunburst.update_traces(
            textinfo='label+percent parent',
            hovertemplate='<b>%{label}</b><br>Quantidade: %{value:,.0f}<br>Percentual: %{percentParent:.1%}<extra></extra>'
        )
        
        fig_sunburst.update_layout(
            legend_title_text='Tipo de Bolsa',
            showlegend=True,
        )
        
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.warning("Não há dados de bolsas para exibir neste gráfico com os filtros atuais.")

st.markdown('---')
st.subheader("Distribuição Média de Mensalidades por Estado no Brasil")
st.info("Qual a média de mensalidade por estado?")
    
average_monthly_per_state = df_filtred.groupby('estado')['mensalidade'].mean().reset_index()
    
geojson_url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
response = requests.get(geojson_url)
geojson_brasil = response.json()

fig_states_br = px.choropleth(
    average_monthly_per_state,
    geojson=geojson_brasil,
    locations='estado',
    featureidkey='properties.sigla',
    color='mensalidade',
    color_continuous_scale=SCALE_COLOR_MAP,
    scope='south america',
    labels={'mensalidade': 'Mensalidade Média (R$)', 'uf_busca': 'Estado'}
)

fig_states_br.update_geos(
            visible=False,
            projection_type="mercator",
            center={"lat": -14, "lon": -53},
            fitbounds="locations"
        )
fig_states_br.update_layout(
    width=1000, 
    height=800,  
    margin={"r": 0, "t": 30, "l": 0, "b": 0}
)
fig_states_br.update_traces(
    hovertemplate='<b>%{location}</b><br><b>Mensalidade Média:</b> R$ %{z:.2f}<extra></extra>'
)

st.plotly_chart(fig_states_br, use_container_width=True)


st.markdown('---')

st.subheader("Quantidade de Bolsas (Cotas vs. Ampla) ofertadas por Estado")
st.info("Como foi a distribuição de bolsas por estado?")

df_barras = df_filtred.copy()

cols_quotas = ['bolsa_integral_cotas', 'bolsa_parcial_cotas']
cols_general = ['bolsa_integral', 'bolsa_parcial']

df_barras['total_bolsas_cotas'] = df_barras[cols_quotas].sum(axis=1)
df_barras['total_bolsas_ampla'] = df_barras[cols_general].sum(axis=1)

df_agrupado = df_barras.groupby('estado')[['total_bolsas_cotas', 'total_bolsas_ampla']].sum().reset_index()

df_agrupado['total_geral'] = df_agrupado['total_bolsas_cotas'] + df_agrupado['total_bolsas_ampla']

df_agrupado = df_agrupado.sort_values(by='total_geral', ascending=False)

fig_barras = px.bar(
    df_agrupado,
    x='estado',
    y=['total_bolsas_cotas', 'total_bolsas_ampla'],
    title='',
    labels={'value': 'Quantidade de Bolsas', 'estado': 'Estado', 'variable': 'Tipo de Bolsa'},
    color_discrete_map={
        'total_bolsas_cotas': SECONDARY_COLOR,
        'total_bolsas_ampla': PRIMARY_COLOR
    }
)

new_names = {'total_bolsas_cotas': 'Bolsas para Cotas', 'total_bolsas_ampla': 'Bolsas - Ampla Concorrência'}
fig_barras.for_each_trace(lambda t: t.update(name = new_names[t.name]))
fig_barras.update_traces(
    hovertemplate="<br><b>Estado</b>: %{x}<br><b>Tipo</b>: %{fullData.name}<br><b>Quantidade</b>: %{y:,.0f}<extra></extra>"
)
st.plotly_chart(fig_barras, use_container_width=True)
    
if not df_filtred.empty:
    st.markdown('---')
    page_size = 10000  
    page_number = st.number_input("Página", min_value=1, value=1, label_visibility="collapsed", width=130 )
    start_idx = (page_number - 1) * page_size
    end_idx = min(start_idx + page_size, len(df_filtred))
    st.dataframe(df_filtred.iloc[start_idx:end_idx])
else:
    st.warning("Nenhum resultado encontrado para os filtros aplicados.")

