DROP TABLE IF EXISTS  coordinates_export;
CREATE TEMPORARY TABLE coordinates_export AS
    (
        SELECT
            ID,
            full_address
        FROM refined.ingested_for_sale_houses
        WHERE longitude is null
        LIMIT 2000

        UNION

        SELECT
            ID,
            full_address
        FROM refined.ingested_to_rent_houses
        WHERE longitude is null
        LIMIT 2000
    )
;

COPY coordinates_export
TO '/tmp/coordinates_export/coordinates_export_{{ ds_nodash }}.csv'
DELIMITER ','
ESCAPE '"'
NULL '\N'
CSV
;
