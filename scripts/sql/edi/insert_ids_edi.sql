INSERT INTO staging.edinburgh(ID)
SELECT DISTINCT ID from landing.edinburgh{{ ds_nodash }};
