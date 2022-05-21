INSERT INTO staging.edinburgh(ID)
SELECT ID from landing.edinburgh{{ ds_nodash }};
