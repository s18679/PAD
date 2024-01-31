import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib as plt
import time
import datetime
from streamlit_option_menu import option_menu
from PIL import Image

df = pd.read_csv('clean_data.csv')

category = option_menu(
    menu_title = 'Menu',
    options = ['Variable Distribution', 'Histogram', 'Pairplot', 'Regression'], #, 'Correlation matrix'
    menu_icon = 'cast',
    default_index = 1,
    orientation = 'horizontal'
)

features = list(df.columns)
features.remove('Unnamed: 0')

if category == 'Histogram':
    var_main = st.selectbox('Select feature', features)
    if st.checkbox('Second feature in color'):
        var_secondary = st.selectbox('Secondary feature', features)
        fig = px.histogram(df, var_main, color = var_secondary)
    else:
        fig = px.histogram(df, var_main)

    #col1 = st.columns(1)
    st.plotly_chart(fig, use_container_width=True)
elif category == 'Variable Distribution':
    plot_types = ['Bar plot', 'Box plot', 'Line plot', 'Scatter plot']
    plot_type = st.selectbox('Select plot type', plot_types)
    var_x = st.selectbox('Select feature 1 (x)', features)
    var_y = st.selectbox('Select feature 2 (y)', features)
    if st.checkbox('Third feature in color'):
        var_col = st.selectbox('Select third feature (color)', features)
        if plot_type == 'Bar plot':
            fig = px.bar(df, x=var_x, y=var_y, color=var_col)
        elif plot_type == 'Box plot':
            fig = px.box(df, x=var_x, y=var_y, color=var_col)
        elif plot_type == 'Scatter plot':
            fig = px.scatter(df, x=var_x, y=var_y, color=var_col)
        elif plot_type == 'Line plot':
            df_sorted = df.sort_values(by=[var_x])
            fig = px.line(df_sorted, x=var_x, y=var_y, color=var_col)
    else:
        if plot_type == 'Bar plot':
            fig = px.bar(df, x=var_x, y=var_y)
        elif plot_type == 'Box plot':
            fig = px.box(df, x=var_x, y=var_y)
        elif plot_type == 'Scatter plot':
            fig = px.scatter(df, x=var_x, y=var_y)
        elif plot_type == 'Line plot':
            df_sorted = df.sort_values(by=[var_x])
            fig = px.line(df_sorted, x=var_x, y=var_y)

    
    st.plotly_chart(fig, use_container_width=False)
elif category == 'Pairplot':
    fig = sns.pairplot(data=df, hue='price', plot_kws={'alpha': 0.5})
    st.pyplot(fig.fig)
elif category =='Regression':
    try:
        var_x = st.selectbox('Select feature 1 (x)', features)
        plot = sns.regplot(x=var_x, y='price', data=df)
        st.pyplot(plot.get_figure())
    except:
        st.error('Failed to create regplot for non-numeric feature')
# elif category == 'Correlation matrix':
    # correlation_matrix = df.corr().round(2)
    # fig, ax = plt.subplots(figsize=(6,5))
    # heatmap = sns.heatmap(correlation_matrix, annot=True)
