DROP TABLE IF EXISTS  landing.area_import_{{ ds_nodash }};
CREATE TABLE landing.area_import_{{ ds_nodash }}
(
    ID                      bigint not null,
    links                   varchar(256),
    number_of_floorplans    smallint,
    area                    smallint,
    raw_floorplan_output    varchar(2048)
);

LOAD DATA INFILE '/var/lib/mysql-files/area_export_{{ ds_nodash }}_filled.csv'
INTO TABLE landing.area_import_{{ ds_nodash }}
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '"\n'
;

UPDATE      refined.ingested_for_sale_houses ifs
LEFT JOIN   landing.area_import_{{ ds_nodash }} ai
ON          ai.ID = ifs.ID
SET
    ifs.number_of_floorplans  = ai.number_of_floorplans
    ifs.area                  = ai.area
    ifs.raw_floorplan_output  = ai.raw_floorplan_output
WHERE
    ai.ID = ifs.ID
;