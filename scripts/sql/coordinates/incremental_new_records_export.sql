DROP TABLE IF EXISTS  refined.coordinates_export;
CREATE TEMPORARY TABLE refined.coordinates_export AS
    (
        SELECT
            ID,
            full_address
        FROM refined.ingested_for_sale_houses
        WHERE longitude is null
    )
;

SELECT
    *
FROM refined.coordinates_export
INTO OUTFILE '/var/lib/mysql-files/coordinates_export_{{ ds_nodash }}.csv'
FIELDS OPTIONALLY ENCLOSED BY '"'
TERMINATED BY ','
ESCAPED BY ''
LINES TERMINATED BY '\r\n';
