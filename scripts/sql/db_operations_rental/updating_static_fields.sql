UPDATE staging.rental_{{ params.region_name }} STG
SET
    number_of_beds = LDN.number_of_beds,
    links = LDN.links,
    description = LDN.description,
    city = '{{ params.region_name }}'
FROM landing.rental_{{ params.region_name }}{{ ds_nodash }} LDN
WHERE
    STG.ID = LDN.ID
;
