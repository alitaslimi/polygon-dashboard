# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import PIL
import data

# Page Favicon
favicon = PIL.Image.open('favicon.ico')

# Global Variables
theme_plotly = None # None or streamlit

# Config
st.set_page_config(page_title='NFT Sales Wash Trades - Polygon Mega Dashboard', page_icon=favicon, layout='wide')

# Title
st.title('NFT Sales Wash Trades')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
washed_overview = data.get_data('Washed Overview')
washed_weekly = data.get_data('Washed Weekly')

# Content
tab_overview, tab_marketplaces, tab_collections = st.tabs(['**Overview**', '**Marketplaces**', '**Collections**'])

with tab_overview:
    st.subheader('Overview')

    df = washed_overview

    c1, c2, c3 = st.columns(3)
    with c1:
        fig = px.pie(df.sort_values('Volume', ascending=False).head(10), values='Volume', names='Trade', title='Share of Legit vs Washed Sales Volume', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df, x='Trade', y='Price', color='Trade', custom_data=['Trade'], title='Average Legit vs Washed NFT Prices')
        fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: $%{y:,.2f}<extra></extra>')
        fig.update_xaxes(title=None, type='category', categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.pie(df.sort_values('Sales', ascending=False).head(10), values='Sales', names='Trade', title='Share of Legit vs Washed Sales', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.pie(df.sort_values('NFTs', ascending=False).head(10), values='NFTs', names='Trade', title='Share of Legit vs Washed NFTs', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c3:
        fig = px.pie(df.sort_values('Traders', ascending=False).head(10), values='Traders', names='Trade', title='Share of Legit vs Washed Traders', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.pie(df.sort_values('Collections', ascending=False).head(10), values='Collections', names='Trade', title='Share of Legit vs Washed Collections', hole=0.4)
        fig.update_layout(legend_title=None, legend_y=0.5)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Activity Over Time')
    
    df = washed_weekly

    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(df, x='Date', y='Volume', color='Trade', custom_data=['Trade'], title='Legit vs Washed Sales Volume Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df, x='Date', y='Traders', color='Trade', custom_data=['Trade'], title='Legit vs Washed Traders Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Traders', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.line(df, x='Date', y='Sales', color='Trade', custom_data=['Trade'], title='Legit vs Washed Sales Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.line(df, x='Date', y='NFTs', color='Trade', custom_data=['Trade'], title='Legit vs Washed NFTs Over Time')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)