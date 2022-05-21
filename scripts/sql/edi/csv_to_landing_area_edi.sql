LOAD DATA INFILE '/var/lib/mysql-files/sales_data_{{ var.value.edinburgh_id }}_{{ ds }}.csv'
INTO TABLE landing.edinburgh{{ ds_nodash }}
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
