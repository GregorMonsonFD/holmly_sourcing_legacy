COPY landing.rental_{{ params.region_name }}{{ ds_nodash }}
FROM '/tmp/rightmove_scrape/rental_data_{{ params.rightmove_region }}_{{ ds }}.csv'
DELIMITER ','
ESCAPE '"'
NULL 'NULL'
CSV
HEADER
;
