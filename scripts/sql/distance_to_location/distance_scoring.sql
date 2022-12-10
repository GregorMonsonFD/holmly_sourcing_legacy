DROP TABLE IF EXISTS reporting.{{ params.location }};
CREATE TABLE reporting.{{ params.location }} (
    score                   double precision
    , id                    bigint
    , price_per_sq_ft       double precision
    , distance_in_km        double precision
    , price                 decimal(11,2)
    , full_address          varchar(256)
    , number_of_beds        smallint
    , links                 varchar(256)
    , postcode              varchar(10)
    , seen_last_ingestion   boolean
    , area                  double precision
    , longitude             double precision
    , latitude              double precision
);

DROP TABLE IF EXISTS {{ params.location }}_analysis_staging;
CREATE TEMPORARY TABLE {{ params.location }}_analysis_staging AS
    (
        SELECT
            (price/area) as price_per_sq_ft,
            (
                111.111 *
                DEGREES(ACOS(LEAST(1.0, COS(RADIANS({{ params.lat }}))
                 * COS(RADIANS(latitude))
                 * COS(RADIANS({{ params.long }} - longitude))
                 + SIN(RADIANS({{ params.lat }}))
                 * SIN(RADIANS(latitude)))))
            ) AS distance_in_km,
            id,
            price,
            full_address,
            number_of_beds,
            links,
            postcode,
            seen_last_ingestion,
            area,
            longitude,
            latitude
        FROM refined.ingested_for_sale_houses
        WHERE     seen_last_ingestion = True
        ORDER BY distance_in_km asc
    );

DROP TABLE IF EXISTS {{ params.location }}_analysis_final;
CREATE TEMPORARY TABLE {{ params.location }}_analysis_final AS
    (
        SELECT (price_per_sq_ft * distance_in_km) as score,
               id,
               price_per_sq_ft,
               distance_in_km,
               price,
               full_address,
               number_of_beds,
               links,
               postcode,
               seen_last_ingestion,
               area,
               longitude,
               latitude
        FROM {{ params.location }}_analysis_staging
        WHERE distance_in_km < {{ params.distance }}
    );

INSERT INTO reporting.{{ params.location }}
SELECT * FROM {{ params.location }}_analysis_final
ORDER BY score asc
;

INSERT INTO reporting.all_locations
SELECT * FROM {{ params.location }}_analysis_final
ORDER BY score asc
ON CONFLICT DO NOTHING
;

