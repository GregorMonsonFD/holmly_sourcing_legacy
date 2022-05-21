DROP TABLE IF EXISTS staging.price_conversion_edi;

CREATE TEMPORARY TABLE staging.price_conversion_edi
SELECT
    ID AS _ID,
    REPLACE(REPLACE(price, '£', ''), ',', '') AS price_formatted
FROM landing.edinburgh{{ ds_nodash }}
;

UPDATE
    staging.edinburgh STG,
    staging.price_conversion_edi TMP
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
