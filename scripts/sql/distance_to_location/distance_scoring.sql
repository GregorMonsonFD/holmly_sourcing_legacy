DROP TABLE IF EXISTS reporting.{{ params.location }};
CREATE TABLE reporting.{{ params.location }} (
    score                   double precision
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

DROP TABLE IF EXISTS staging.{{ params.location }}_analysis_staging;
CREATE TEMPORARY TABLE staging.{{ params.location }}_analysis_staging AS
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
        WHERE     seen_last_ingestion = 1
        ORDER BY distance_in_km asc
    );

DROP TABLE IF EXISTS staging.{{ params.location }}_analysis_final;
CREATE TEMPORARY TABLE staging.{{ params.location }}_analysis_final AS
    (
        SELECT (1/(price_per_sq_ft * distance_in_km)) as score,
               price_per_sq_ft,
               distance_in_km,
               price,
               full_address,
               number_of_   qbeds,
               links,
               postcode,
               seen_last_ingestion,
               area,
               longitude,
               latitude
        FROM staging.{{ params.location }}_analysis_staging
        WHERE distance_in_km < 3
    );

INSERT INTO reporting.{{ params.location }}
SELECT * FROM staging.{{ params.location }}_analysis_final
ORDER BY score desc
;


