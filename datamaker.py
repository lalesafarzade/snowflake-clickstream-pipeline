import json
import time
from datetime import datetime, timezone
import requests
import boto3
from botocore.exceptions import NoCredentialsError
from config import API_KEY

S3_BUCKET_NAME = "stock-market-alpha-vantage"  
ALPHA_VANTAGE_KEY = API_KEY     
BATCH_SIZE = 5  


TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX"]

# Initialize S3 Client
s3_client = boto3.client('s3')

def fetch_stock_quote(symbol):
    """Fetches real-time global quote data for a ticker symbol."""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            raw_data = response.json()
            
            # Alpha Vantage returns data under a "Global Quote" key
            if "Global Quote" in raw_data and raw_data["Global Quote"]:
                quote = raw_data["Global Quote"]
                
                # Transform into clean JSON fields
                clean_record = {
                    "symbol": quote.get("01. symbol"),
                    "open": float(quote.get("02. open", 0)),
                    "high": float(quote.get("03. high", 0)),
                    "low": float(quote.get("04. low", 0)),
                    "price": float(quote.get("05. price", 0)),
                    "volume": int(quote.get("06. volume", 0)),
                    "latest_trading_day": quote.get("07. latest trading day"),
                    "previous_close": float(quote.get("08. previous close", 0)),
                    "change": float(quote.get("09. change", 0)),
                    "change_percent": quote.get("10. change percent"),
                    "ingested_at": datetime.now(timezone.utc).isoformat() # Critical DE metadata
                }
                return clean_record
            else:
                print(f"⚠️ API Note for {symbol}: Might be hitting rate limits or market is closed. {raw_data}")
        else:
            print(f"❌ HTTP Error {response.status_code} for {symbol}")
    except Exception as e:
        print(f"❌ Failed to fetch {symbol}: {e}")
    return None

def upload_batch_to_s3(batch_data):
    """Saves the stock batch as a JSON-Lines file to S3."""
    now = datetime.now(timezone.utc)
    s3_key = f"stocks/year={now.year}/month={now.strftime('%m')}/day={now.strftime('%d')}/market_data_{int(now.timestamp())}.json"
    
    json_lines_body = "\n".join([json.dumps(record) for record in batch_data])
    
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json_lines_body,
            ContentType='application/json'
        )
        print(f"Successfully uploaded {len(batch_data)} stock records to S3: {s3_key}")
    except NoCredentialsError:
        print("AWS Credentials not found.")
    except Exception as e:
        print(f"S3 Upload failed: {e}")

def main():
    print(f"Starting Real Stock Data Stream to S3...")
    
    stock_batch = []
    ticker_index = 0
    
    try:
        while True:
            symbol = TICKERS[ticker_index]
            print(f"Fetching live data for {symbol}...")
            
            stock_data = fetch_stock_quote(symbol)
            if stock_data:
                stock_batch.append(stock_data)
                print(f"Added {symbol} at ${stock_data['price']} to batch.")
            
          
            if len(stock_batch) >= BATCH_SIZE:
                upload_batch_to_s3(stock_batch)
                stock_batch = []
            
         
            ticker_index = (ticker_index + 1) % len(TICKERS)
            
           
            print(" Sleeping 15 seconds to respect free API limits...")
            time.sleep(15)
            
    except KeyboardInterrupt:
        if stock_batch:
            print("\nFlushing final stock records to S3...")
            upload_batch_to_s3(stock_batch)
        print("Stock stream paused.")

if __name__ == "__main__":
    main()