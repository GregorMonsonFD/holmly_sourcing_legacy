DROP TABLE IF EXISTS  landing.area_import_{{ ds_nodash }};
CREATE TABLE landing.area_import_{{ ds_nodash }}
(
    ID                      bigint not null,
    links                   varchar(256),
    number_of_floorplans    smallint,
    area                    varchar(128)
);

COPY landing.area_import_{{ ds_nodash }}
FROM '/tmp/area_export_filled/area_export_{{ ds_nodash }}_filled.csv'
DELIMITER ','
ESCAPE '"'
NULL '\N'
CSV
;

UPDATE      refined.ingested_for_sale_houses ifs
LEFT JOIN   landing.area_import_{{ ds_nodash }} ai
ON          ai.ID = ifs.ID
SET
    ifs.number_of_floorplans  = ai.number_of_floorplans,
    ifs.area = IF (
        ai.area = 'null',
        null,
        CAST(ai.area AS DOUBLE PRECISION)
    )
WHERE
    ai.ID = ifs.ID
;