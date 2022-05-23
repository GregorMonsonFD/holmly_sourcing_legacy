INSERT INTO staging.{{ params.region_name }}(ID)
SELECT DISTINCT ID from landing.{{ params.region_name }}{{ ds_nodash }};
