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
st.set_page_config(page_title='NFT Sales Marketplaces - Polygon Mega Dashboard', page_icon=favicon, layout='wide')

# Title
st.title('NFT Sales of Marketplaces')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
marketplaces_overview = data.get_data('Marketplaces Overview')
marketplaces_weekly = data.get_data('Marketplaces Weekly')

# Content
st.subheader('Overview')

df = marketplaces_overview
c1, c2, c3 = st.columns(3)
with c1:
    fig = px.pie(df, values='Volume', names='Marketplace', title='Share of Total Sales Volume by Marketplace', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='Sales', names='Marketplace', title='Share of Total Sales by Marketplace', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.pie(df, values='Buyers', names='Marketplace', title='Share of Total Unique Buyers by Marketplace', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Prices')

c1, c2, c3, c4 = st.columns(4)
with c1:
    fig = px.bar(df, x='Marketplace', y='PriceAverage', color='Marketplace', custom_data=['Marketplace'], title='Average Price of NFTs by Marketplace', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.2f}<extra></extra>')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df, x='Marketplace', y='PriceMedian', color='Marketplace', custom_data=['Marketplace'], title='Median Price of NFTs by Marketplace', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.2f}<extra></extra>')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.bar(df, x='Marketplace', y='PriceMax', color='Marketplace', custom_data=['Marketplace'], title='Highest Price of NFTs by Marketplace', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.0f}<extra></extra>')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c4:
    fig = px.bar(df, x='Marketplace', y='PriceMin', color='Marketplace', custom_data=['Marketplace'], title='Floor Price of NFTs by Marketplace', log_y=True)
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.2f}<extra></extra>')
    fig.update_xaxes(title=None, categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Activity Over Time')

df = marketplaces_weekly.sort_values(['Date', 'Volume'], ascending=[True, False]).reset_index(drop=True)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='Date', y='Volume', color='Marketplace', custom_data=['Marketplace'], title='Sales Volume by Marketplace Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(df, x='Date', y='Sales', color='Marketplace', custom_data=['Marketplace'], title='Sales by Marketplace Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.bar(df, x='Date', y='Buyers', color='Marketplace', custom_data=['Marketplace'], title='Buyers by Marketplace Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.bar(df, x='Date', y='NFTs', color='Marketplace', custom_data=['Marketplace'], title='Traded NFTs by Marketplace Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.bar(df, x='Date', y='Collections', color='Marketplace', custom_data=['Marketplace'], title='Traded Collections by Marketplace Over Time')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Collections', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
with c2:
    fig = go.Figure()
    for i in df['Marketplace'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Marketplace == @i")['Date'],
            y=df.query("Marketplace == @i")['Volume'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Share of Sales Volume by Marketplace Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = go.Figure()
    for i in df['Marketplace'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Marketplace == @i")['Date'],
            y=df.query("Marketplace == @i")['Sales'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Share of Sales by Marketplace Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = go.Figure()
    for i in df['Marketplace'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Marketplace == @i")['Date'],
            y=df.query("Marketplace == @i")['Buyers'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Share of Buyers by Marketplace Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = go.Figure()
    for i in df['Marketplace'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Marketplace == @i")['Date'],
            y=df.query("Marketplace == @i")['NFTs'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Share of Traded NFTs by Marketplace Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = go.Figure()
    for i in df['Marketplace'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Marketplace == @i")['Date'],
            y=df.query("Marketplace == @i")['Collections'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Share of Traded Collections by Marketplace Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)