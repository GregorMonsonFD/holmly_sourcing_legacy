DROP TABLE IF EXISTS price_conversion_{{ params.region_name }};

CREATE TEMPORARY TABLE price_conversion_{{ params.region_name }} AS
SELECT
    ID AS _ID,
    REPLACE(REPLACE(price, '£', ''), ',', '') AS price_formatted
FROM landing.{{ params.region_name }}{{ ds_nodash }}
;

UPDATE staging.{{ params.region_name }} STG
SET
    price =
        CASE
            WHEN price_formatted ~ '^-?[0-9]+$' THEN CAST(price_formatted AS decimal(11, 2))
        END
FROM price_conversion_{{ params.region_name }} TMP
WHERE
    STG.ID = TMP._ID
;
