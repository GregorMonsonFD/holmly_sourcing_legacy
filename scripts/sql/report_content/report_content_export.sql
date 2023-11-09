DROP TABLE IF EXISTS  report_content;
CREATE TEMPORARY TABLE report_content AS
    (
        SELECT
            row_number() over (order by yield_percentage desc) as rank,
            full_address,
            round(price, 0) as price,
            round(down_payment, 0) as down_payment,
            round(monthly_interest, 0) as monthly_interest,
            round(rental_price_per_month, 0) as rental_price_per_month,
            round(profit, 0) profit,
            yield_percentage,
            links
        FROM reporting.rental_projections_in_desirable_areas
        WHERE yield_percentage > 3
    )
;

COPY report_content
TO '/tmp/report_content/report_content_{{ ds_nodash }}.csv'
DELIMITER ','
ESCAPE '"'
NULL '\N'
CSV;
