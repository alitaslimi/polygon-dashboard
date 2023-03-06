# Polygon NFTs Dashboard
This [Polygon NFTs Dashboard](https://alitaslimi-polygon.streamlit.app) was originally created for [MetricsDAO](https://metricsdao.xyz) using the [Flipside Crypto](https://flipsidecrypto.xyz) data.

## SQL queries
- **Mints**: [Overview](https://flipsidecrypto.xyz/edit/queries/f17f19c1-7545-4716-b366-780827deaebb) | [Weekly](https://flipsidecrypto.xyz/edit/queries/b781bb55-3bfd-40d4-80ec-138e07710549)
- **Sales**: [Overview](https://flipsidecrypto.xyz/edit/queries/fd0718fd-fd34-4df7-b59a-bb4c225be7ef) | [Weekly](https://flipsidecrypto.xyz/edit/queries/515b0273-d969-47e3-884c-c40a17dbd4e6) | [Heatmap](https://flipsidecrypto.xyz/edit/queries/9d928ade-69ad-443f-a554-f12676896763)
- **Marketplaces**: [Overview](https://flipsidecrypto.xyz/edit/queries/680898bc-6bce-4aac-b013-8cf4a308b971) | [Weekly](https://flipsidecrypto.xyz/edit/queries/3120378b-1778-43aa-8194-7e3274f1c521)
- **Collections**: [Overview](https://flipsidecrypto.xyz/edit/queries/e932af65-3295-4294-8b8a-796b702375d6) | [Weekly](https://flipsidecrypto.xyz/edit/queries/84a104d7-e759-43cb-9b2e-4e6bfa218052)
- **Wash Trades**: [Overview](https://flipsidecrypto.xyz/edit/queries/a5044912-5248-4b80-862a-e8fba60e61e2) | [Weekly](https://flipsidecrypto.xyz/edit/queries/5a52f1a9-e121-4967-b0df-cbc35d8a5c13)

## Methodology
To be able to find NFT sale transactions, various assumptions were made to select the proper data from the tables. These transactions had a **Transfer** *event_name* with a **tokenId** key in their *event_inputs* column. Also, only the **from** and **to** addresses without a **NULL** value were selected to remove the NFT mints and burns. Those with a NULL from address were considered the **mint** transactions. All the NFT collections were manually labeled by checking the details of their contract addresses on polygonscan.

Two types of wash trades, including the self-financed and recursive wash trades, were considered in this analysis. First, all of the sales were selected. Then, the tx_hash of wash trades was determined, using the method explained in the next two sections. Next, all of the sales were filtered with and without these transaction hashes to obtain washed and legit sales, respectively. Finally, these two were either joined or unionized to be able to compare them simultaneously.

**Self-financed** wash trades happen when address A provides funds for address B, then address B buys an NFT from address A and returns the fund. To detect these wash trades, the following conditions were considered:

```sql
sales.buyer = transfers.matic_to_address
AND sales.seller = transfers.matic_from_address
AND sales.amount <= transfers.amount
AND sales.block_timestamp > transfers.block_timestamp
```

**Recursive** wash trades (no official naming) happen when address A sells an NFT to address B, which sells back the NFT to address A. To detect these wash trades, the following conditions were considered:

```sql
sales_first.token = sales_second.token
AND sales_first.collection = sales_second.collection
AND sales_first.seller = sales_second.buyer
AND sales_first.buyer = sales_second.seller
AND sales_first.block_timestamp < sales_second.block_timestamp
```
