UPDATE
    staging.edinburgh STG,
    landing.edinburgh20220521 LDN
SET
    STG.number_of_beds = LDN.number_of_beds,
    STG.links = LDN.links,
    STG.description = LDN.description
WHERE
    STG.ID = LDN.ID
;
