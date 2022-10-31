DROP TABLE IF EXISTS  area_export;
CREATE TEMPORARY TABLE area_export AS
    (
        SELECT
            ID,
            links,
            number_of_floorplans,
            area
        FROM refined.ingested_for_sale_houses
        WHERE number_of_floorplans is null
    )
;

INSERT INTO area_export
SELECT
    ID,
    links,
    number_of_floorplans,
    area
FROM refined.ingested_to_rent_houses
WHERE number_of_floorplans is null
;

COPY area_export
TO '/tmp/area_export/area_export_{{ ds_nodash }}.csv'
DELIMITER ','
ESCAPE '"'
NULL '\N'
CSV;
