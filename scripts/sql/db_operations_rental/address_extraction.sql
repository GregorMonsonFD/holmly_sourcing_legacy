DROP TABLE IF EXISTS staging.rental_address_extraction_{{ params.region_name }};
CREATE TEMPORARY TABLE staging.rental_address_extraction_{{ params.region_name }}
SELECT
    ID AS _ID,
    address AS _address,
    convert(reverse(SUBSTRING_INDEX(reverse(address), reverse('{{ params.postcode_prefix }}'), 1)), CHAR(256)) AS _postcode
FROM landing.rental_{{ params.region_name }}{{ ds_nodash }};


UPDATE staging.rental_address_extraction_{{ params.region_name }}
SET _postcode =
    IF
    (
        _postcode REGEXP '[0-9]',
        _postcode,
        null
    );


UPDATE
    staging.rental_{{ params.region_name }} STG,
    staging.rental_address_extraction_{{ params.region_name }} TMP
SET
    full_address = _address,
    postcode =
    IF
    (
        LENGTH(_postcode) < 10,
        CONCAT(REPLACE('{{ params.postcode_prefix }}', ' ', ''), _postcode),
        null
    )
WHERE
    ID = _ID
;
