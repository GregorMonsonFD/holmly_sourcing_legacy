UPDATE     refined.ingested_for_sale_houses
SET seen_last_ingestion = FALSE
WHERE city = '{{ params.region_name }}';

UPDATE      refined.ingested_for_sale_houses TGT
SET
    ID                  = STG.ID,
    full_address        = STG.full_address,
    postcode            = STG.postcode,
    city                = STG.city,
    number_of_beds      = STG.number_of_beds,
    links               = STG.links,
    description         = STG.description,
    price               = STG.price,
    last_seen           = '{{ dag.timezone.convert(execution_date).strftime("%Y-%m-%d %H:%M:%S") }}',
    seen_last_ingestion = TRUE
FROM staging.{{ params.region_name }} STG
WHERE
    STG.ID = TGT.ID
;

DROP TABLE IF EXISTS staging_to_refined_new_{{ params.region_name }};
CREATE TEMPORARY TABLE staging_to_refined_new_{{ params.region_name }} AS
SELECT 
    STG.*, 
    TGT.ID as refined_id
FROM staging.{{ params.region_name }} STG
LEFT JOIN refined.ingested_for_sale_houses TGT
ON STG.ID = TGT.ID
WHERE TGT.ID IS NULL
;

INSERT INTO refined.ingested_for_sale_houses(ID, full_address, postcode, city, number_of_beds, links, description, price, first_seen, last_seen, seen_last_ingestion)
SELECT
    STG.ID,
    STG.full_address,
    STG.postcode,
    STG.city,
    STG.number_of_beds,
    STG.links,
    STG.description,
    STG.price,
    '{{ dag.timezone.convert(execution_date).strftime("%Y-%m-%d %H:%M:%S") }}',
    '{{ dag.timezone.convert(execution_date).strftime("%Y-%m-%d %H:%M:%S") }}',
    TRUE
FROM staging.staging_to_refined_new_{{ params.region_name }} STG
;