LOAD DATA INFILE '/var/lib/mysql-files/sales_data_5E475_2022-05-16.csv'
INTO TABLE landing.import_edinburgh
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

DROP TABLE IF EXISTS staging.edinburgh;

create table staging.edinburgh
(
    ID             int          not null,
    address        varchar(128) not null,
    number_of_beds smallint     null,
    links          varchar(256) not null,
    description    varchar(128) not null,
    price           varchar(64) not null
);

INSERT INTO staging.edinburgh
SELECT * FROM landing.import_edinburgh;

UPDATE staging.edinburgh
SET price =
    REPLACE(
        REPLACE(
            REPLACE(
                IFNULL(price,'0')
                    ,',','')
            ,'£','')
        ,'POA', '0')
;

SELECT * FROM landing.import_edinburgh
WHERE number_of_beds >= 3;

ALTER TABLE landing.import_edinburgh CONVERT TO money;

SELECT average


