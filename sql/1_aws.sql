CREATE OR REPLACE STORAGE INTEGRATION s3_stock_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('s3://my-snowflake-project-bucket-name/stocks/')
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::mine:role/SnowflakeStockProjectRole'; -- Use your real ARN

-- Run this command in Snowflake to view the security keys Snowflake generated for your specific trial account:
  DESC EXTENDED STORAGE INTEGRATION s3_stock_integration;

--   Update the AWS IAM Role Trust Relationship (Final Step)