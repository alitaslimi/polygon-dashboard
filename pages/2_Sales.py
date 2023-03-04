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
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Config
st.set_page_config(page_title='NFT Mints - Polygon Mega Dashboard', page_icon=favicon, layout='wide')

# Title
st.title('NFT Sales')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
sales_overview = data.get_data('Sales Overview')
sales_weekly = data.get_data('Sales Weekly')
sales_heatmap = data.get_data('Sales Heatmap')

# Content
tab_overview, tab_prices, tab_heatmap = st.tabs(['**Overview**', '**Prices**', '**Heatmap**'])

with tab_overview:
    st.subheader('Overview')

    df = sales_overview
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label='**Total Sales Volume**', value=str('$' + df['Volume'].map('{:,.0f}'.format).values[0]), help=str(df['VolumeMatic'].map('{:,.0f}'.format).values[0] + ' MATIC'))
        st.metric(label='**Total Sales**', value=str(df['Sales'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Total Unique Buyers**', value=str(df['Buyers'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Total Unique Sellers**', value=str(df['Sellers'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Total Traded NFTs**', value=str(df['NFTs'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Total Traded Collections**', value=str(df['Collections'].map('{:,.0f}'.format).values[0]))
    
    st.subheader('Averages')
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Average Daily Volume**', value=str('$' + df['Volume/Day'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Traded NFTs**', value=str(df['NFTs/Day'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Volume/Collection**', value=str('$' + df['Volume/Collection'].map('{:,.0f}'.format).values[0]))
    with c2:
        st.metric(label='**Average Volume/Buyer**', value=str('$' + df['Volume/Buyer'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average NFTs/Buyer**', value=str(df['NFTs/Buyer'].map('{:,.2f}'.format).values[0]))
        st.metric(label='**Average NFTs/Collection**', value=str(df['NFTs/Collection'].map('{:,.0f}'.format).values[0]))
    with c3:
        st.metric(label='**Average Daily Sales**', value=str(df['Sales/Day'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average Daily Traded Collections**', value=str(df['Collections/Day'].map('{:,.0f}'.format).values[0]))
        st.metric(label='**Average NFTs/Sale**', value=str(df['NFTs/Sale'].map('{:,.2f}'.format).values[0]))
    with c4:
        st.metric(label='**Average Sales/Buyer**', value=str(df['Sales/Buyer'].map('{:,.2f}'.format).values[0]))
        st.metric(label='**Average Collections/Buyer**', value=str(df['Collections/Buyer'].map('{:,.2f}'.format).values[0]))
        st.metric(label='**Average Daily Buyers**', value=str(df['Buyers/Day'].map('{:,.0f}'.format).values[0]))
    
    st.subheader('Activity Over Time')

    df = sales_weekly

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=df['Date'], y=df['Volume'], name='Volume', hovertemplate='Volume: $%{y:,.0f}<extra></extra>'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['Sales'], name='Sales', hovertemplate='Sales: %{y:,.0f}<extra></extra>'), secondary_y=True)
    fig.update_layout(title_text='Total Volume and Number of Sales Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='Volume', secondary_y=False, rangemode='tozero')
    fig.update_yaxes(title_text='Sales', secondary_y=True, rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots()
    fig.add_trace(go.Line(x=df['Date'], y=df['Buyers'], name='Buyers', hovertemplate='Buyers: %{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['Sellers'], name='Sellers', hovertemplate='Sellers: %{y:,.0f}<extra></extra>'))
    fig.update_layout(title_text='Total Number of Unique Buyers and Sellers Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='Addresses', rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=df['Date'], y=df['NFTs'], name='NFTs', hovertemplate='NFTs: %{y:,.0f}<extra></extra>'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['Collections'], name='Collections', hovertemplate='Collections: %{y:,.0f}<extra></extra>'), secondary_y=True)
    fig.update_layout(title_text='Total Number of Traded NFTs and Collections Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='NFTs', secondary_y=False, rangemode='tozero')
    fig.update_yaxes(title_text='Collections', secondary_y=True, rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_prices:
    st.subheader('Overview')

    df = sales_overview
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label='**Average Price**', value=str('$' + df['PriceAverage'].map('{:,.2f}'.format).values[0]), help=str(df['PriceAverageMatic'].map('{:,.2f}'.format).values[0] + ' MATIC'))
    with c2:
        st.metric(label='**Median Price**', value=str('$' + df['PriceMedian'].map('{:,.2f}'.format).values[0]), help=str(df['PriceMedianMatic'].map('{:,.2f}'.format).values[0] + ' MATIC'))
    with c3:
        st.metric(label='**Highest Price**', value=str('$' + df['PriceMax'].map('{:,.0f}'.format).values[0]), help=str(df['PriceMaxMatic'].map('{:,.0f}'.format).values[0] + ' MATIC'))
    with c4:
        st.metric(label='**Floor Price**', value=str('$' + df['PriceMin'].map('{:,.2f}'.format).values[0]), help=str(df['PriceMinMatic'].map('{:,.2f}'.format).values[0] + ' MATIC'))
    
    st.subheader('Prices Over Time')

    df = sales_weekly

    fig = sp.make_subplots()
    fig.add_trace(go.Bar(x=df['Date'], y=df['PriceAverage'], name='Average', hovertemplate='Average: $%{y:,.2f}<extra></extra>'))
    fig.add_trace(go.Line(x=df['Date'], y=df['PriceMedian'], name='Median', hovertemplate='Median: $%{y:,.2f}<extra></extra>'))
    fig.update_layout(title_text='Average and Median Price of NFTs Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='Price [USD]', rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Line(x=df['Date'], y=df['PriceMax'], name='Highest Price', hovertemplate='Highest Price: $%{y:,.0f}<extra></extra>'), secondary_y=False)
    fig.add_trace(go.Line(x=df['Date'], y=df['PriceMin'], name='Floor Price', hovertemplate='Floor Price: $%{y:,.2f}<extra></extra>'), secondary_y=True)
    fig.update_layout(title_text='Highest and Floor Price of NFTs Over Time', hovermode='x unified')
    fig.update_yaxes(title_text='Highest Price [USD]', secondary_y=False, rangemode='tozero')
    fig.update_yaxes(title_text='Floor Price [USD]', secondary_y=True, rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab_heatmap:

    st.subheader('Activity Heatmap')

    df = sales_heatmap
    c1, c2 = st.columns(2)
    with c1:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='Volume', histfunc='avg', title='Heatmap of Sales Volume', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Volume [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='Buyers', histfunc='avg', title='Heatmap of Unique Buyers', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Buyers'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='NFTs', histfunc='avg', title='Heatmap of Traded NFTs', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='NFTs'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='Sales', histfunc='avg', title='Heatmap of Sales', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Sales'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='Sellers', histfunc='avg', title='Heatmap of Unique Sellers', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Sellers'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='Collections', histfunc='avg', title='Heatmap of Traded Collections', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Collections'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    st.subheader('Price Heatmap')
    c1, c2 = st.columns(2)
    with c1:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='PriceAverage', histfunc='avg', title='Heatmap of Average NFT Prices', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Average [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='PriceMax', histfunc='avg', title='Heatmap of Highest NFT Prices', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Highest Price [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        fig = px.density_heatmap(df, x='Hour', y='Day', z='PriceMedian', histfunc='avg', title='Heatmap of Median NFT Prices', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Median [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.density_heatmap(df, x='Hour', y='Day', z='PriceMin', histfunc='avg', title='Heatmap of NFT Floor Prices', nbinsx=24)
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title=None, xaxis={'dtick': 2}, coloraxis_colorbar=dict(title='Floor Price [USD]'))
        fig.update_yaxes(categoryorder='array', categoryarray=week_days)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)