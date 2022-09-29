UPDATE staging.{{ params.region_name }} STG,
SET
    STG.number_of_beds = LDN.number_of_beds,
    STG.links = LDN.links,
    STG.description = LDN.description,
    STG.city = '{{ params.region_name }}'
FROM landing.{{ params.region_name }}{{ ds_nodash }} LDN
WHERE
    STG.ID = LDN.ID
;
