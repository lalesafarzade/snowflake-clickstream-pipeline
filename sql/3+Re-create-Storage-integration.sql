-- 1. Re-create the integration to reset the connection
CREATE OR REPLACE STORAGE INTEGRATION s3_stock_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('s3://stock-market-alpha-vantage/stocks/')
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::myaccount_id:role/SnowflakeStockProjectRole';

-- 2. Check the NEW details
DESC STORAGE INTEGRATION s3_stock_integration;