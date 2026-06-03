CREATE OR REPLACE TABLE stock_market_db.raw_data.bronze_stock_quotes (
    raw_payload VARIANT,
    snowflake_ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


