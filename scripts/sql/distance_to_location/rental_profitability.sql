drop table if exists rental;
create temp table rental as
    select
        distinct(ifs.id)
        , ifs.city
        , ifs.number_of_beds
        , ifs.price as price
        , ifs.links
        , count(distinct itr.id) as data_count
        , avg((itr.price / itr.number_of_beds)) as price_per_bed
        , avg((itr.price / itr.number_of_beds)) * ifs.number_of_beds as rental_price_per_month
        , 0.25 * ifs.price as down_payment
        , ifs.price * 0.75 * 0.00608 as monthly_interest
        , (avg((itr.price / itr.number_of_beds)) * ifs.number_of_beds)
        - (ifs.price * 0.75 * 0.00608) as profit
        , ROUND((((avg((itr.price / itr.number_of_beds)) * ifs.number_of_beds)
        - (ifs.price * 0.75 * 0.00608)) / ifs.price) * 100, 2) as yield_percentage
    from refined.ingested_for_sale_houses ifs
    left join refined.ingested_to_rent_houses itr
    on (
            111.111 *
            DEGREES(ACOS(LEAST(1.0, COS(RADIANS(itr.latitude))
            * COS(RADIANS(ifs.latitude))
            * COS(RADIANS(itr.longitude - ifs.longitude))
            + SIN(RADIANS(itr.latitude))
            * SIN(RADIANS(ifs.latitude)))))
        )
        < 0.5
    where   ifs.longitude is not null
    and     itr.longitude is not null
    and     ifs.seen_last_ingestion = true
    group by ifs.id
    order by profit desc
;

drop table if exists reporting.rental_projections_in_desirable_areas;
create table reporting.rental_projections_in_desirable_areas as
    (
        select
            re.*
        from rental re
        inner join reporting.all_locations al
        on      re.id = al.id
        where   re.profit is not null
        and     re.data_count > 3
        order by profit desc
    )
;

drop table if exists reporting.rental_projections_all;
create table reporting.rental_projections_all as
    (
        select
            re.*
        from rental re
        where   re.profit is not null
        and     re.data_count > 3
        order by profit desc
    )
;