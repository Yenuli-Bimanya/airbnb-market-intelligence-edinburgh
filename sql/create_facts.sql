-- Calendar fact table
CREATE OR REPLACE TABLE dw.fact_calendar AS
SELECT
    c.listing_id,
    CAST(c.date AS DATE) AS date_key,
    c.available,
    c.minimum_nights,
    c.maximum_nights,
    d.year,
    d.month,
    d.is_weekend
FROM staging_calendar c
LEFT JOIN dw.dim_date d
    ON CAST(c.date AS DATE) = d.date_key;

-- Reviews fact table
CREATE OR REPLACE TABLE dw.fact_reviews AS
SELECT
    r.id AS review_id,
    r.listing_id,
    CAST(r.date AS DATE) AS date_key,
    r.reviewer_id,
    r.reviewer_name,
    LENGTH(r.comments) AS comment_length,
    d.year,
    d.month,
    d.is_weekend
FROM staging_reviews r
LEFT JOIN dw.dim_date d
    ON CAST(r.date AS DATE) = d.date_key;

-- Listing performance fact table
CREATE OR REPLACE TABLE dw.fact_listing_performance AS
SELECT
    l.id AS listing_id,
    l.host_id,
    n.neighbourhood_key,
    l.price,
    l.room_type,
    l.property_type,
    l.number_of_reviews,
    l.review_scores_rating,
    l.availability_365,
    l.calendar_days,
    l.unavailable_days,
    l.occupancy_proxy,
    l.avg_minimum_nights,
    l.review_count_detailed,
    l.latest_review_date,
    l.review_frequency_per_year,
    l.neighbourhood_median_price,
    l.neighbourhood_listing_count,
    l.neighbourhood_avg_rating,
    l.host_tenure_years,
    l.price_per_bedroom,
    l.estimated_revenue_proxy,
    l.is_valid_price,
    l.is_valid_location
FROM staging_listings l
LEFT JOIN dw.dim_neighbourhood n
    ON l.neighbourhood_cleansed = n.neighbourhood;