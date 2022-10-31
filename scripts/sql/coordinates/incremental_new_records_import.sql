DROP TABLE IF EXISTS  landing.coordinates_import_{{ ds_nodash }};
CREATE TABLE landing.coordinates_import_{{ ds_nodash }}
(
    ID                      bigint not null,
    longitude               double precision,
    latitude                double precision
);

COPY landing.coordinates_import_{{ ds_nodash }}
FROM '/tmp/coordinates_export_filled/coordinates_export_{{ ds_nodash }}_filled.csv'
DELIMITER ','
ESCAPE '"'
NULL 'null'
CSV
;

UPDATE refined.ingested_for_sale_houses ifs
SET
    longitude   = co.longitude,
    latitude    = co.latitude
FROM        landing.coordinates_import_{{ ds_nodash }} co
WHERE       co.ID = ifs.ID
;

UPDATE refined.ingested_to_rent_houses itr
SET
    longitude   = co.longitude,
    latitude    = co.latitude
FROM        landing.coordinates_import_{{ ds_nodash }} co
WHERE       co.ID = itr.ID
;
