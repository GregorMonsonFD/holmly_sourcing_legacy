DROP TABLE IF EXISTS landing.edinburgh{{ ds_nodash }};
CREATE TABLE landing.edinburgh{{ ds_nodash }}
    (
    ID bigint not null,
    address varchar(128) not null,
    number_of_beds smallint null,
    links varchar(256) not null,
    description varchar(128) not null,
    price varchar(64) not null
    );