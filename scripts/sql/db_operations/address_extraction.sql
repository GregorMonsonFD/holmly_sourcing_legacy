DROP TABLE IF EXISTS address_extraction_{{ params.region_name }};
CREATE TEMPORARY TABLE address_extraction_{{ params.region_name }} AS
SELECT
    ID AS _ID,
    address AS _address,
    reverse(split_part(reverse(address), reverse('{{ params.postcode_prefix }}'), 1)) AS _postcode
FROM landing.{{ params.region_name }}{{ ds_nodash }};


UPDATE address_extraction_{{ params.region_name }}
SET _postcode =
    CASE
        WHEN _postcode ~ '[0-9]' THEN _postcode
    END
;


UPDATE staging.{{ params.region_name }} STG
SET
    full_address = _address,
    postcode =
    CASE
        WHEN LENGTH(_postcode) < 8 THEN CONCAT(REPLACE('{{ params.postcode_prefix }}', ' ', ''), _postcode)
        ELSE null
    END
FROM address_extraction_{{ params.region_name }} TMP
WHERE
    ID = _ID
;
