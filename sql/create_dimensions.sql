-- Date dimension
CREATE OR REPLACE TABLE dw.dim_date AS
SELECT DISTINCT
    CAST(date AS DATE) AS date_key,
    EXTRACT(year FROM date) AS year,
    EXTRACT(month FROM date) AS month,
    EXTRACT(day FROM date) AS day,
    DAYNAME(date) AS day_name,
    CASE
        WHEN DAYOFWEEK(date) IN (6, 7) THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM (
    SELECT date FROM staging_calendar
    UNION
    SELECT date FROM staging_reviews
);

-- Neighbourhood dimension
CREATE OR REPLACE TABLE dw.dim_neighbourhood AS
SELECT
    ROW_NUMBER() OVER (ORDER BY neighbourhood) AS neighbourhood_key,
    neighbourhood,
    neighbourhood_group
FROM staging_neighbourhoods;

-- Host dimension
CREATE OR REPLACE TABLE dw.dim_host AS
SELECT DISTINCT
    host_id,
    host_name,
    host_is_superhost,
    host_response_rate,
    host_acceptance_rate,
    host_listings_count,
    host_total_listings_count,
    host_identity_verified,
    hosts_time_as_host_years AS host_tenure_years
FROM staging_listings
WHERE host_id IS NOT NULL;

-- Listing dimension
CREATE OR REPLACE TABLE dw.dim_listing AS
SELECT
    id AS listing_id,
    host_id,
    name AS listing_name,
    neighbourhood_cleansed AS neighbourhood,
    latitude,
    longitude,
    property_type,
    room_type,
    accommodates,
    bedrooms,
    beds,
    bathrooms,
    price,
    minimum_nights,
    availability_365,
    number_of_reviews,
    review_scores_rating,
    review_scores_cleanliness,
    review_scores_location,
    review_scores_value,
    instant_bookable,
    is_valid_price,
    is_valid_location
FROM staging_listings;