DROP TABLE IF EXISTS staging.price_conversion_{{ params.region_name }};

CREATE TEMPORARY TABLE staging.price_conversion_{{ params.region_name }}
SELECT
    ID AS _ID,
    REPLACE(REPLACE(price, '£', ''), ',', '') AS price_formatted
FROM landing.{{ params.region_name }}{{ ds_nodash }}
;

UPDATE
    staging.{{ params.region_name }} STG,
    staging.price_conversion_{{ params.region_name }} TMP
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
