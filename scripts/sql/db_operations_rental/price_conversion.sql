DROP TABLE IF EXISTS staging.rental_price_conversion_{{ params.region_name }};

CREATE TEMPORARY TABLE staging.rental_price_conversion_{{ params.region_name }}
SELECT
    ID AS _ID,
    REPLACE(REPLACE(REPLACE(price, ' pcm', ''), '£', ''), ',', '') AS price_formatted
FROM landing.rental_{{ params.region_name }}{{ ds_nodash }}
;

UPDATE
    staging.rental_{{ params.region_name }} STG,
    staging.rental_price_conversion_{{ params.region_name }} TMP
SET
    price =
        IF
        (
            TMP.price_formatted REGEXP '^-?[0-9]+$',
            price_formatted,
            null
        )
WHERE
    STG.ID = TMP._ID
;
