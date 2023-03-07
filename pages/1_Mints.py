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
st.set_page_config(page_title='NFT Mints - Polygon Mega Dashboard', page_icon=favicon, layout='wide')

# Title
st.title('NFT Mints')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
mints_overview = data.get_data('Mints Overview')
mints_collections = data.get_data('Mints Collections')
mints_weekly = data.get_data('Mints Weekly')

# Content
st.subheader('Overview')

df = mints_overview
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(label='**Total Mints**', value=str(df['Mints'].map('{:,.0f}'.format).values[0]))
with c2:
    st.metric(label='**Total Unique Minters**', value=str(df['Minters'].map('{:,.0f}'.format).values[0]))
with c3:
    st.metric(label='**Total Minted NFTs**', value=str(df['NFTs'].map('{:,.0f}'.format).values[0]))
with c4:
    st.metric(label='**Total Minted Collections**', value=str(df['Collections'].map('{:,.0f}'.format).values[0]))

st.subheader('Collections')

df = mints_collections

c1, c2 = st.columns(2)
with c1:
    fig = px.pie(df.sort_values('Mints', ascending=False).head(10), values='Mints', names='Collection', title='Share of Total Mints by Collection', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df.sort_values('Minters', ascending=False).head(10), values='Minters', names='Collection', title='Share of Total Unique Minters by Collection', hole=0.4)
    fig.update_layout(legend_title=None, legend_y=0.5)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Activity Over Time')

df = mints_weekly

fig = sp.make_subplots()
fig.add_trace(go.Line(x=df['Date'], y=df['Mints'], name='Mints', hovertemplate='Mints: %{y:,.0f}<extra></extra>'))
fig.add_trace(go.Line(x=df['Date'], y=df['Minters'], name='Minters', hovertemplate='Minters: %{y:,.0f}<extra></extra>'))
fig.update_layout(title_text='Total Number of Mints and Minters Over Time', hovermode='x unified')
fig.update_yaxes(title_text='Number', rangemode='tozero')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
fig.add_trace(go.Line(x=df['Date'], y=df['NFTs'], name='NFTs', hovertemplate='NFTs: %{y:,.0f}<extra></extra>'), secondary_y=False)
fig.add_trace(go.Line(x=df['Date'], y=df['Collections'], name='Collections', hovertemplate='Collections: %{y:,.0f}<extra></extra>'), secondary_y=True)
fig.update_layout(title_text='Total Number of Minted NFTs and Collections Over Time', hovermode='x unified')
fig.update_yaxes(title_text='NFTs', secondary_y=False, rangemode='tozero')
fig.update_yaxes(title_text='Collections', secondary_y=True, rangemode='tozero')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)