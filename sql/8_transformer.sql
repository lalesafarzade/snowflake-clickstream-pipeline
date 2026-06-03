CREATE OR REPLACE VIEW stock_market_db.raw_data.silver_stock_quotes AS
SELECT
    raw_payload:symbol::STRING AS ticker,
    raw_payload:open::FLOAT AS open_price,
    raw_payload:high::FLOAT AS daily_high,
    raw_payload:low::FLOAT AS daily_low,
    raw_payload:price::FLOAT AS current_price,
    raw_payload:volume::INT AS volume_traded,
    raw_payload:latest_trading_day::DATE AS trading_date,
    raw_payload:previous_close::FLOAT AS previous_close,
    raw_payload:change::FLOAT AS price_change,
    REPLACE(raw_payload:change_percent::STRING, '%', '')::FLOAT AS change_percent,
    raw_payload:ingested_at::TIMESTAMP_TZ AS api_fetch_time,
    snowflake_ingested_at
FROM stock_market_db.raw_data.bronze_stock_quotes;