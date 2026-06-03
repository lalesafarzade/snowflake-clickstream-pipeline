CREATE OR REPLACE STAGE stock_market_db.raw_data.s3_stock_stage
  STORAGE_INTEGRATION = s3_stock_integration
  URL = 's3://stock-market-alpha-vantage/stocks/'
  FILE_FORMAT = stock_market_db.raw_data.json_lines_format;

-- Test that Snowflake can see your S3 data files from VS Code:
LIST @stock_market_db.raw_data.s3_stock_stage;