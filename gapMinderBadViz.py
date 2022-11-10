# -*- coding: utf-8 -*-
"""
Created on Fri Nov 4 09:50:17 2022

@author: mrissler
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

@st.cache
@st.cache
def loadData():
    df = px.data.gapminder().query("year == 2007")
    df['logPop'] = np.log2(df['pop'])
    df['rootPop'] = np.sqrt(df['pop'])
    return df


hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        body {overflow: hidden;}
        div.block-container {padding-top:1rem;}
        div.block-container {padding-bottom:1rem;}
        </style>
        """

st.markdown(hide, unsafe_allow_html=True)

gm2007 = loadData()

tab1, tab2 = st.tabs(["Recommendations", "Playground"])

with tab1:
    col1, col2 = st.columns([1,4])

    baseTextDesc = '''The horizontal axis is labeled "GDP per capita ($/person)" and ranges from 0 to 50k.
    The vertical axis is labeled "Life expectancy (years)" and ranges from 39 to 83.
    Most points are follow a curve where low income (GDP per capita) countries (below \$2000) have low life expectancy (below 60 years),
    but life expectancy increases rapidly with income with countries with an average income above \$5000 have a life expectancy above 70 years.'''

    continentDesc = '''Most low income/low life expectancy countries are from Africa.
    European countries dominate the countries with high life expectancy.
    Countries in Asia and the Americas make up many of the countries with relatively low income and high life expectancy.'''

    with col1:
        plotType = st.selectbox('Type of color scale',
                                ('Rainbow',
                                 'Yellow-Blue',
                                 'Contrast based',
                                 'Shape based'))

        textDesc = st.checkbox('Text description of plot')

    with col2:

        if plotType == "Rainbow":
            if textDesc:
                st.markdown(baseTextDesc+'''The continents for this plot are colored red for Asia, blue for Europe,
                green for Africa, purple for the Americas, and orange for Oceania.'''+continentDesc)


            else:
                fig = px.scatter(gm2007, x = 'gdpPercap', y = 'lifeExp',
                            color = 'continent', size = 'logPop',
                            labels = {'gdpPercap' : 'GDP per capita ($/person)',
                                      'lifeExp' : 'Life expectancy (years)',
                                      'continent' : 'Continent',
                                      'logPop': 'log(Population)',
                                      'pop':'Population'},
                            hover_data={'gdpPercap':':.2f',
                                        'lifeExp':':.1f',
                                        'logPop':False,
                                        'pop':True},
                            color_discrete_sequence = px.colors.qualitative.Set1,
                    )
                fig.update_layout(font_size = 12,
                                  legend=dict(yanchor="top", y=0.7, x=.75)
                                  )
                st.plotly_chart(fig, use_container_width=True)

        else:
                st.text("Not implemented yet.")

    if plotType == "Rainbow":
        st.markdown('''Do **not** use a rainbow scale. The contrast between colors in rainbow scales
                   are not uniformly spaced making distinguishing colors difficult for people
                   with CVD.''')

    else:
        st.text("Recommendations for this color scale not yet implemented")
