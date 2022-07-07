DROP TABLE IF EXISTS  refined.area_export;
CREATE TEMPORARY TABLE refined.area_export AS
    (
        SELECT
            ID,
            links,
            number_of_floorplans,
            area,
            raw_floorplan_output
        FROM refined.ingested_for_sale_houses
        WHERE number_of_floorplans is null
    )
;

SELECT
    *
FROM refined.area_export
INTO OUTFILE '/var/lib/mysql-files/area_export_{{ ds_nodash }}.csv'
FIELDS OPTIONALLY ENCLOSED BY '"'
TERMINATED BY ','
ESCAPED BY ''
LINES TERMINATED BY '\r\n';

SYSTEM sudo chown eggzo:eggzo area_export_{{ ds_nodash }}.csv;