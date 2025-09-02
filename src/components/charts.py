import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import textwrap

def show_charts(df_filtred: pd.DataFrame):
    """
    Displays all dashboard charts.

    Args:
        df_filtred (pd.DataFrame): The filtered DataFrame with the data to be displayed.
    """
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
            
            formatted_labels = ['<br>'.join(textwrap.wrap(label, 40)) for label in ranking_schools.index]

            max_value = ranking_schools.max()
            text_positions = []
            text_font_colors = []
            for value in ranking_schools:
                if value < max_value * 0.30:
                    text_positions.append('outside')
                    text_font_colors.append('black')
                else:
                    text_positions.append('inside')
                    text_font_colors.append('white')

            fig_ranking_schools = px.bar(
                x=ranking_schools.values, 
                y=formatted_labels,   
                orientation='h',
                labels={'x': 'Total de Bolsas', 'y': 'Universidade'},
                text=ranking_schools.values,
                color_discrete_sequence=[PRIMARY_COLOR]
            )

            fig_ranking_schools.update_traces(
                hovertemplate='<b>Universidade:</b> %{customdata}<br><b>Total de Bolsas:</b> %{x:,.0f}<extra></extra>',
                customdata=ranking_schools.index, 
                texttemplate='%{x:,.0f}',
                textposition=text_positions,
                textfont_color=text_font_colors
            )

            fig_ranking_schools.update_layout(
                title_text="Top 10 Universidades por Total de Bolsas",
                title_x=0.5,
                title_xanchor="center",
                margin=dict(l=150, r=50, t=50, b=50)
            )

            st.plotly_chart(fig_ranking_schools, use_container_width=True)
        else:
            st.warning("Nenhum dado de universidade para exibir com os filtros atuais.")

    with graphic2:

        ranking_courses = df_graphics_ranking.groupby('curso')['total_bolsas'].sum().nlargest(10).sort_values(ascending=True)

        if not ranking_courses.empty:
  
            formatted_labels_courses = ['<br>'.join(textwrap.wrap(label, 30)) for label in ranking_courses.index]
            
            max_value_courses = ranking_courses.max()
            text_positions_courses = []
            text_font_colors_courses = []
            for value in ranking_courses:
                if value < max_value_courses * 0.25:
                    text_positions_courses.append('outside')
                    text_font_colors_courses.append('black')
                else:
                    text_positions_courses.append('inside')
                    text_font_colors_courses.append('white')

            fig_ranking_courses = px.bar(
                x=ranking_courses.values,
                y=formatted_labels_courses,
                orientation='h',
                labels={'x': 'Total de Bolsas', 'y': 'Curso'},
                text=ranking_courses.values,
                color_discrete_sequence=[PRIMARY_COLOR]
            )

            fig_ranking_courses.update_traces(
                hovertemplate='<b>Curso:</b> %{customdata}<br><b>Total de Bolsas:</b> %{x:,.0f}<extra></extra>',
                customdata=ranking_courses.index,
                texttemplate='%{x:,.0f}',
                textposition=text_positions_courses,
                textfont_color=text_font_colors_courses
            )

            fig_ranking_courses.update_layout(
                title_text="Top 10 Cursos por Total de Bolsas",
                title_x=0.5,
                title_xanchor="center",
                margin=dict(l=150, r=50, t=50, b=50) # Margens generosas
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

    df_bars = df_filtred.copy()

    cols_quotas = ['bolsa_integral_cotas', 'bolsa_parcial_cotas']
    cols_general = ['bolsa_integral', 'bolsa_parcial']

    df_bars['total_bolsas_cotas'] = df_bars[cols_quotas].sum(axis=1)
    df_bars['total_bolsas_ampla'] = df_bars[cols_general].sum(axis=1)

    df_groupby = df_bars.groupby('estado')[['total_bolsas_cotas', 'total_bolsas_ampla']].sum().reset_index()

    df_groupby['total_geral'] = df_groupby['total_bolsas_cotas'] + df_groupby['total_bolsas_ampla']

    df_groupby = df_groupby.sort_values(by='total_geral', ascending=False)

    fig_bars = px.bar(
        df_groupby,
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
    fig_bars.for_each_trace(lambda t: t.update(name = new_names[t.name]))
    fig_bars.update_traces(
        hovertemplate="<br><b>Estado</b>: %{x}<br><b>Tipo</b>: %{fullData.name}<br><b>Quantidade</b>: %{y:,.0f}<extra></extra>"
    )
    st.plotly_chart(fig_bars, use_container_width=True)
