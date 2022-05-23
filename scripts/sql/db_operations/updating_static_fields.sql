UPDATE
    staging.{{ params.region_name }} STG,
    landing.{{ params.region_name }}{{ ds_nodash }} LDN
SET
    STG.number_of_beds = LDN.number_of_beds,
    STG.links = LDN.links,
    STG.description = LDN.description,
    STG.city = '{{ params.region_name }}'
WHERE
    STG.ID = LDN.ID
;
