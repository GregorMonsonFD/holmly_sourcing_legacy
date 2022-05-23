DROP TABLE IF EXISTS staging.address_extraction_{{ params.region_name }}_stage_1;
CREATE TEMPORARY TABLE staging.address_extraction_{{ params.region_name }}_stage_1
SELECT
    ID AS _ID,
    address AS _address,
    reverse(SUBSTRING_INDEX(reverse(address), reverse('{{ params.postcode_prefix }}'), 1)) AS _postcode
FROM landing.{{ params.region_name }}{{ ds_nodash }};

CREATE TEMPORARY TABLE staging.address_extraction_{{ params.region_name }}_stage_2
SELECT * FROM staging.address_extraction_{{ params.region_name }}_stage_1
WHERE _postcode REGEXP '[0-9]';

UPDATE
    staging.{{ params.region_name }} STG,
    staging.address_extraction_{{ params.region_name }}_stage_2 TMP
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
