DROP TABLE IF EXISTS  landing.area_import_{{ ds_nodash }};
CREATE TABLE landing.area_import_{{ ds_nodash }}
(
    ID                      bigint not null,
    links                   varchar(256),
    number_of_floorplans    smallint,
    area                    double precision
);

COPY landing.area_import_{{ ds_nodash }}
FROM '/tmp/area_export_filled/area_export_{{ ds_nodash }}_filled.csv'
DELIMITER ','
ESCAPE '"'
NULL 'null'
CSV
;

UPDATE refined.ingested_for_sale_houses ifs
SET
    number_of_floorplans  = ai.number_of_floorplans,
    area = ai.area
FROM    landing.area_import_{{ ds_nodash }} ai
WHERE   ai.ID = ifs.ID
;

UPDATE refined.ingested_to_rent_houses itr
SET
    number_of_floorplans  = ai.number_of_floorplans,
    area = ai.area
FROM        landing.area_import_{{ ds_nodash }} ai
WHERE       ai.ID = itr.ID
;
