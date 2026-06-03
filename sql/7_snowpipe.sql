CREATE OR REPLACE PIPE stock_market_db.raw_data.stock_snowpipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO stock_market_db.raw_data.bronze_stock_quotes (raw_payload)
  FROM (
    SELECT $1 
    FROM @stock_market_db.raw_data.s3_stock_stage
  );

-- IMPORTANT: Force Snowpipe to scan the bucket and load any files already sitting there right now
ALTER PIPE stock_market_db.raw_data.stock_snowpipe REFRESH;