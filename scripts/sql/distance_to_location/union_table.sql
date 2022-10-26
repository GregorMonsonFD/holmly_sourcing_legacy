DROP TABLE IF EXISTS reporting.all_locations;
CREATE TABLE reporting.all_locations (
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