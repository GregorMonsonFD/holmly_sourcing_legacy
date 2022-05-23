DROP TABLE IF EXISTS landing.{{ params.region_name }}{{ ds_nodash }};
CREATE TABLE landing.{{ params.region_name }}{{ ds_nodash }}
    (
    ID bigint not null,
    address varchar(256) not null,
    number_of_beds smallint null,
    links varchar(256) not null,
    description varchar(128) not null,
    price varchar(64) not null
    );

DROP TABLE IF EXISTS staging.{{ params.region_name }};
CREATE TABLE staging.{{ params.region_name }}
(
    ID bigint,
    full_address varchar(256),
    postcode varchar(8),
    number_of_beds smallint,
    links varchar(256),
    description varchar(128),
    price decimal(11,2)
)
;
