import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("📈 Stock Market Analytics Dashboard")

# Connect to Snowflake
session = get_active_session()

# Dropdown picker for Ticker
ticker = st.selectbox("Select Ticker", ["AAPL", "MSFT", "GOOGL", "AMZN"])

# Run query based on selection
df = session.sql(f"""
    SELECT API_FETCH_TIME, CURRENT_PRICE, VOLUME_TRADED 
    FROM stock_market_db.raw_data.silver_stock_quotes 
    WHERE TICKER = '{ticker}' 
    ORDER BY API_FETCH_TIME DESC
""").to_pandas()

# Display a native Streamlit Line Chart
if not df.empty:
    st.metric(label="Current Price", value=f"${df['CURRENT_PRICE'].iloc[0]}")
    st.line_chart(data=df, x="API_FETCH_TIME", y="CURRENT_PRICE")
else:
    st.write("No data found for this ticker today.")