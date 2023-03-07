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
st.set_page_config(page_title='NFT Sales Collections - Polygon Mega Dashboard', page_icon=favicon, layout='wide')

# Title
st.title('NFT Sales by Collections')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
collections_overview = data.get_data('Collections Overview')
collections_weekly = data.get_data('Collections Weekly')

# Content
st.subheader('Overview')

df = collections_overview

c1, c2, c3 = st.columns(3)
with c1:
    fig = px.pie(df.sort_values('Volume', ascending=False).head(10), values='Volume', names='Collection', title='Share of Total Sales Volume by Collection', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df.sort_values('Sales', ascending=False).head(10), values='Sales', names='Collection', title='Share of Total Sales by Collection', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.pie(df.sort_values('Buyers', ascending=False).head(10), values='Buyers', names='Collection', title='Share of Total Unique Buyers by Collection', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Prices')

c1, c2, c3, c4 = st.columns(4)
with c1:
    fig = px.bar(df.sort_values('PriceAverage', ascending=False).head(10), x='Collection', y='PriceAverage', color='Collection', custom_data=['Collection'], title='Average Price of NFTs by Collection')
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.2f}<extra></extra>')
    fig.update_xaxes(title=None, type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df.sort_values('PriceMedian', ascending=False).head(10), x='Collection', y='PriceMedian', color='Collection', custom_data=['Collection'], title='Median Price of NFTs by Collection')
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.2f}<extra></extra>')
    fig.update_xaxes(title=None, type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c3:
    fig = px.bar(df.sort_values('PriceMax', ascending=False).head(10), x='Collection', y='PriceMax', color='Collection', custom_data=['Collection'], title='Highest Price of NFTs by Collection')
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.0f}<extra></extra>')
    fig.update_xaxes(title=None, type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c4:
    fig = px.bar(df.sort_values('PriceMin', ascending=False).head(10), x='Collection', y='PriceMin', color='Collection', custom_data=['Collection'], title='Floor Price of NFTs by Collection')
    fig.update_layout(showlegend=False, yaxis_title=None, hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.2f}<extra></extra>')
    fig.update_xaxes(title=None, type='category', categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Activity Over Time')

df = collections_weekly

df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Sellers': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Volume': 'sum',
    'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceMin': 'mean'}).reset_index()
df['RowNumber'] = df.groupby(['Date'])['Volume'].rank(method='max', ascending=False)
df.loc[df['RowNumber'] > 3, 'Collection'] = 'Other'
df = df.groupby(['Date', 'Collection']).agg({'Sales': 'sum', 'Sellers': 'sum', 'Buyers': 'sum', 'NFTs': 'sum', 'Volume': 'sum',
    'PriceAverage': 'mean', 'PriceMedian': 'mean', 'PriceMax': 'mean', 'PriceMin': 'mean'}).reset_index()

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='Date', y='Volume', color='Collection', custom_data=['Collection'], title='Daily Sales Volume of Top Collections By Volume')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: $%{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = px.bar(df, x='Date', y='Sales', color='Collection', custom_data=['Collection'], title='Daily Sales of Top Collections By Volume')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.bar(df, x='Date', y='Buyers', color='Collection', custom_data=['Collection'], title='Daily Buyers of Top Collections By Volume')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = px.bar(df, x='Date', y='NFTs', color='Collection', custom_data=['Collection'], title='Daily Traded NFTs of Top Collections By Volume')
    fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='NFTs', hovermode='x unified')
    fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
with c2:
    fig = go.Figure()
    for i in df['Collection'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Collection == @i")['Date'],
            y=df.query("Collection == @i")['Volume'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Daily Share of Sales Volume of Top Collections By Volume')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = go.Figure()
    for i in df['Collection'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Collection == @i")['Date'],
            y=df.query("Collection == @i")['Sales'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Daily Share of Sales of Top Collections By Volume')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = go.Figure()
    for i in df['Collection'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Collection == @i")['Date'],
            y=df.query("Collection == @i")['Buyers'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Daily Share of Buyers of Top Collections By Volume')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    
    fig = go.Figure()
    for i in df['Collection'].unique():
        fig.add_trace(go.Scatter(
            name=i,
            x=df.query("Collection == @i")['Date'],
            y=df.query("Collection == @i")['NFTs'],
            mode='lines',
            stackgroup='one',
            groupnorm='percent'
        ))
    fig.update_layout(title='Daily Share of Traded NFTs of Top Collections By Volume')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)