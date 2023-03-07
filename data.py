# Libraries
import streamlit as st
import pandas as pd

# Data Sources
collections_csv = pd.read_csv('collections.csv')
collection_dict = pd.Series(collections_csv.Name.values,index=collections_csv.Collection).to_dict()

# @st.cache(ttl=1000, allow_output_mutation=True)
def get_data(query):
    if query == 'Mints Overview':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/f17f19c1-7545-4716-b366-780827deaebb/data/latest')
    
    if query == 'Mints Collections':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/07761e94-4c1f-462c-a646-2be49ffb4fdb/data/latest')
    
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
    
    elif query == 'Washed Collections':
        df = pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/e9192f19-4c3f-46b5-ac76-10c4496b6def/data/latest')
        df["Collection"] = df["Collection"].map(collection_dict)
        return df
    
    elif query == 'Washed Weekly':
        return pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/5a52f1a9-e121-4967-b0df-cbc35d8a5c13/data/latest')

    return None