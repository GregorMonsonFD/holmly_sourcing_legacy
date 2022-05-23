DROP TABLE IF EXISTS staging.address_extraction_{{ params.region_name }};
CREATE TEMPORARY TABLE staging.address_extraction_{{ params.region_name }}
SELECT
    ID AS _ID,
    address AS _address,
    reverse(SUBSTRING_INDEX(reverse(address), reverse('{{ params.postcode_prefix }}'), 1)) AS _postcode
FROM landing.{{ params.region_name }}{{ ds_nodash }};

SELECT count(*) FROM staging.address_extraction_{{ params.region_name }}
WHERE LENGTH(_postcode) <6;

UPDATE
    staging.{{ params.region_name }} STG,
    staging.address_extraction_{{ params.region_name }} TMP
SET
    full_address = _address,
    postcode =
    IF
    (
        LENGTH(_postcode) < 10 AND LIKE '%[0-9]%',
        CONCAT(REPLACE('{{ params.postcode_prefix }}', ' ', ''), _postcode),
        null
    )
WHERE
    ID = _ID
;
