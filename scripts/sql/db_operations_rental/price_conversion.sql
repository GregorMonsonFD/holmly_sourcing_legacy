DROP TABLE IF EXISTS rental_price_conversion_{{ params.region_name }};

CREATE TEMPORARY TABLE rental_price_conversion_{{ params.region_name }} AS
SELECT
    ID AS _ID,
    REPLACE(REPLACE(REPLACE(price, ' pcm', ''), '£', ''), ',', '') AS price_formatted
FROM landing.rental_{{ params.region_name }}{{ ds_nodash }}
;

UPDATE staging.rental_{{ params.region_name }} STG
SET
    price =
        CASE
            WHEN price_formatted ~ '^-?[0-9]+$' THEN CAST(price_formatted AS decimal(11, 2))
        END
FROM rental_price_conversion_{{ params.region_name }} TMP
WHERE
    STG.ID = TMP._ID
;
