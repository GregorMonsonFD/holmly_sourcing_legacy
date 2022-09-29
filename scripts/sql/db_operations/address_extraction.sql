DROP TABLE IF EXISTS address_extraction_{{ params.region_name }};
CREATE TEMPORARY TABLE address_extraction_{{ params.region_name }} AS
SELECT
    ID AS _ID,
    address AS _address,
    convert(reverse(SUBSTRING_INDEX(reverse(address), reverse('{{ params.postcode_prefix }}'), 1)), CHAR(256)) AS _postcode
FROM landing.{{ params.region_name }}{{ ds_nodash }};


UPDATE address_extraction_{{ params.region_name }}
SET _postcode =
    CASE
        WHEN _postcode like'[0-9]' THEN _postcode
        ELSE THEN null
    END
;


UPDATE staging.{{ params.region_name }} STG
SET
    full_address = _address,
    postcode =
    CASE
        WHEN LENGTH(_postcode) < 10 THEN CONCAT(REPLACE('{{ params.postcode_prefix }}', ' ', ''), _postcode),
        ELSE THEN null
    END
FROM staging.address_extraction_{{ params.region_name }} TMP
WHERE
    ID = _ID
;
