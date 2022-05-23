LOAD DATA INFILE '/var/lib/mysql-files/sales_data_{{ params.rightmove_region }}_{{ ds }}.csv'
INTO TABLE landing.{{ params.region_name }}{{ ds_nodash }}
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
