DROP TABLE IF EXISTS address_extraction_{{ params.region_name }};
CREATE TEMPORARY TABLE address_extraction_{{ params.region_name }}
SELECT
    ID AS _ID,
    address AS _address,
    convert(reverse(SUBSTRING_INDEX(reverse(address), reverse('{{ params.postcode_prefix }}'), 1)), CHAR(256)) AS _postcode
FROM landing.{{ params.region_name }}{{ ds_nodash }};


UPDATE address_extraction_{{ params.region_name }}
SET _postcode =
    IF
    (
        _postcode REGEXP '[0-9]',
        _postcode,
        null
    );


UPDATE staging.{{ params.region_name }} STG
SET
    full_address = _address,
    postcode =
    IF
    (
        LENGTH(_postcode) < 10,
        CONCAT(REPLACE('{{ params.postcode_prefix }}', ' ', ''), _postcode),
        null
    )
FROM staging.address_extraction_{{ params.region_name }} TMP
WHERE
    ID = _ID
;
