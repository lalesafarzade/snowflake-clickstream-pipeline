CREATE DATABASE stock_market_db;
CREATE SCHEMA stock_market_db.raw_data;

USE DATABASE stock_market_db;
USE SCHEMA raw_data;

-- Define a Named File Format to tell Snowflake how to read the S3 JSON Lines files
CREATE OR REPLACE FILE FORMAT stock_market_db.raw_data.json_lines_format
  TYPE = 'JSON'
  STRIP_OUTER_ARRAY = TRUE
  COMPRESSION = 'AUTO';