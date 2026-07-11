-- 1. Average price by neighbourhood
SELECT
    n.neighbourhood,
    ROUND(AVG(l.price), 2) AS avg_price,
    COUNT(*) AS listing_count
FROM dw.dim_listing l
JOIN dw.dim_neighbourhood n
    ON l.neighbourhood = n.neighbourhood
WHERE l.is_valid_price = TRUE
GROUP BY n.neighbourhood
ORDER BY avg_price DESC;

-- 2. Top 10 hosts by listing count
SELECT
    h.host_id,
    h.host_name,
    h.host_is_superhost,
    h.host_listings_count,
    COUNT(l.listing_id) AS listings_in_dataset
FROM dw.dim_host h
JOIN dw.dim_listing l
    ON h.host_id = l.host_id
GROUP BY
    h.host_id,
    h.host_name,
    h.host_is_superhost,
    h.host_listings_count
ORDER BY listings_in_dataset DESC
LIMIT 10;

-- 3. Occupancy proxy by room type
SELECT
    room_type,
    ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy,
    ROUND(AVG(estimated_revenue_proxy), 2) AS avg_estimated_revenue_proxy,
    COUNT(*) AS listing_count
FROM dw.fact_listing_performance
GROUP BY room_type
ORDER BY avg_occupancy_proxy DESC;

-- 4. Review score vs price correlation
SELECT
    ROUND(CORR(price, review_scores_rating), 4) AS price_review_score_correlation
FROM dw.fact_listing_performance
WHERE price IS NOT NULL
  AND review_scores_rating IS NOT NULL
  AND is_valid_price = TRUE;

-- 5. Highest-performing neighbourhoods by average review score
SELECT
    n.neighbourhood,
    ROUND(AVG(f.review_scores_rating), 2) AS avg_review_score,
    ROUND(AVG(f.price), 2) AS avg_price,
    COUNT(*) AS listing_count
FROM dw.fact_listing_performance f
JOIN dw.dim_neighbourhood n
    ON f.neighbourhood_key = n.neighbourhood_key
WHERE f.review_scores_rating IS NOT NULL
GROUP BY n.neighbourhood
ORDER BY avg_review_score DESC
LIMIT 10;