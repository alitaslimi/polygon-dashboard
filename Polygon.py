# Libraries
import streamlit as st
import PIL

# Page Favicon
favicon = PIL.Image.open('favicon.ico')

# Config
st.set_page_config(page_title='Polygon Mega Dashboard', page_icon=favicon, layout='wide')

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Content
logo = PIL.Image.open('polygon-logo.png')
c1, c2, c3 = st.columns(3)
with c2:
    st.image(logo)

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