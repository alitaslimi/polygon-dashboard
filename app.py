# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import PIL

# Page Favicon
favicon = PIL.Image.open('favicon.ico')

# Global Variables
theme_plotly = None # None or streamlit
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Layout
st.set_page_config(page_title='Polygon NFTs', page_icon=favicon, layout='wide')
st.title('Polygon NFTs')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Data Sources
# @st.cache(ttl=3600)
def get_data(query):
    if query == 'Mints Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/f17f19c1-7545-4716-b366-780827deaebb/data/latest')
    elif query == 'Mints Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/b781bb55-3bfd-40d4-80ec-138e07710549/data/latest')
    elif query == 'Sales Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/fd0718fd-fd34-4df7-b59a-bb4c225be7ef/data/latest')
    elif query == 'Sales Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/515b0273-d969-47e3-884c-c40a17dbd4e6/data/latest')
    elif query == 'Sales Heatmap':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/9d928ade-69ad-443f-a554-f12676896763/data/latest')
    elif query == 'Marketplaces Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/680898bc-6bce-4aac-b013-8cf4a308b971/data/latest')
    elif query == 'Marketplaces Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/3120378b-1778-43aa-8194-7e3274f1c521/data/latest')
    elif query == 'Collections Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/e932af65-3295-4294-8b8a-796b702375d6/data/latest')
    elif query == 'Collections Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/84a104d7-e759-43cb-9b2e-4e6bfa218052/data/latest')
    elif query == 'Washed Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/a5044912-5248-4b80-862a-e8fba60e61e2/data/latest')
    elif query == 'Washed Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/5a52f1a9-e121-4967-b0df-cbc35d8a5c13/data/latest')
    return None

mints_overview = get_data('Mints Overview')
mints_weekly = get_data('Mints Weekly')
sales_overview = get_data('Sales Overview')
sales_weekly = get_data('Sales Weekly')
sales_heatmap = get_data('Sales Heatmap')
marketplaces_overview = get_data('Marketplaces Overview')
marketplaces_weekly = get_data('Marketplaces Weekly')
collections_overview = get_data('Collections Overview')
collections_weekly = get_data('Collections Weekly')
washed_overview = get_data('Washed Overview')
washed_weekly = get_data('Washed Weekly')

# Content
st.write(
    """
    NFTs (non-fungible tokens) on Polygon are unique digital assets that are stored on the Polygon
    blockchain network. NFTs represent ownership of a specific asset or collectible, such as digital
    art, music, videos, and other digital content. Polygon provides a low-cost and fast way to mint,
    transfer, and trade NFTs, making it an ideal platform for creators and collectors to exchange
    and showcase their digital assets. The growing popularity of NFTs has led to an explosion of
    innovative use cases, such as NFT gaming, virtual real estate, and even social media profiles.
    Overall, NFTs on Polygon offer an exciting new way to own, trade, and experience unique digital
    assets.
    """
)

with st.expander('**Methodology**'):
    st.write(
        """
        The data for this dashboard was selected from the [**Flipside Crypto**](https://flipsidecrypto.xyz)
        data platform by using its **REST API**. The code for this tool is saved and accessible
        in its [**GitHub Repository**](https://github.com/alitaslimi/polygon-dashboard).

        The links to the SQL queries are provided in the readme of the GitHub repo, as well as the description
        of the methodology and the limitation of measuring the NFT sales (primary and secondary) from the
        data available through Flipside.

        This dashboard is designed and structured in multiple **Tabs** that are accessible under the **Analysis**
        section. Each of these Tabs addresses a different segment of the Polygon NFT ecosystem (Mints, Sales, etc.).
        """
    )

st.header('Analysis')

tab_mints, tab_sales, tab_prices, tab_heatmap, tab_marketplaces, tab_collections, tab_wash = st.tabs(
    ['**Mints**', '**Sales**', '**Price Analysis**', '**Heatmap**', '**Marketplaces**', '**Collections**', '**Wash Trades**'])

with tab_mints:
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

with tab_sales:
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

with tab_marketplaces:
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
    
with tab_collections:
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
        fig = px.bar(df, x='Date', y='Volume', color='Collection', custom_data=['Collection'], title='Daily Sales Volume of Top Marketplaces By Volume')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Volume [USD]', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: $%{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

        fig = px.bar(df, x='Date', y='Sales', color='Collection', custom_data=['Collection'], title='Daily Sales of Top Marketplaces By Volume')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Sales', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df, x='Date', y='Buyers', color='Collection', custom_data=['Collection'], title='Daily Buyers of Top Marketplaces By Volume')
        fig.update_layout(legend_title=None, xaxis_title=None, yaxis_title='Buyers', hovermode='x unified')
        fig.update_traces(hovertemplate='%{customdata}: %{y:,.0f}<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
        
        fig = px.bar(df, x='Date', y='NFTs', color='Collection', custom_data=['Collection'], title='Daily Traded NFTs of Top Marketplaces By Volume')
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
    
with tab_wash:
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

# Whitespace
st.write("""
    #
    #
    #
""")

# Credits
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.info('**Data Analyst: [@AliTslm](https://twitter.com/AliTslm)**', icon="💡")
with c2:
    st.info('**GitHub: [@alitaslimi](https://github.com/alitaslimi)**', icon="💻")
with c3:
    st.info('**Data: [Flipside Crypto](https://flipsidecrypto.xyz)**', icon="🧠")
with c4:
    st.info('**Bounty Program: [MetricsDAO](https://metricsdao.xyz)**', icon="🏦")