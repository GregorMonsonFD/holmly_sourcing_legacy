INSERT INTO staging.rental_{{ params.region_name }}(ID)
SELECT DISTINCT ID from landing.rental_{{ params.region_name }}{{ ds_nodash }};
