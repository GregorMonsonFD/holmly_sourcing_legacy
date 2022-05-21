DROP TABLE IF EXISTS staging.address_extraction;
CREATE TEMPORARY TABLE staging.address_extraction
SELECT
    ID AS _ID,
    address AS _address,
    reverse(SUBSTRING_INDEX(reverse(address), 'HE', 1)) AS _postcode
FROM landing.edinburgh{{ ds_nodash }};

SELECT count(*) FROM staging.address_extraction
WHERE LENGTH(_postcode) <6;

UPDATE
    staging.edinburgh STG,
    staging.address_extraction TMP
SET
    full_address = _address,
    postcode =
    IF
    (
        LENGTH(_postcode) < 6,
        CONCAT('EH', _postcode),
        null
    )
WHERE
    ID = _ID
;
