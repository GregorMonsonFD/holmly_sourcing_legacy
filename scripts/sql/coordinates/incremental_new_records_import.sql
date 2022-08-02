DROP TABLE IF EXISTS  landing.coordinates_import_{{ ds_nodash }};
CREATE TABLE landing.coordinates_import_{{ ds_nodash }}
(
    ID                      bigint not null,
    longitude               double,
    latitude                double
);

LOAD DATA INFILE '/var/lib/mysql-files/coordinates_export_{{ ds_nodash }}_filled.csv'
INTO TABLE landing.coordinates_import_{{ ds_nodash }}
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
;

UPDATE      refined.ingested_for_sale_houses ifs
LEFT JOIN   landing.coordinates_import_{{ ds_nodash }} co
ON          co.ID = ifs.ID
SET
    ifs.longitude   = co.longitude,
    ifs.latitude    = co.latitude
WHERE
    co.ID = ifs.ID
;