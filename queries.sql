SELECT sum(cast(area_ha as double precision))
FROM france.france
where region = 'FR-01'
group by region;

WITH harvest as (SELECT productivity * cast(area_ha as double precision) as harvest
                 FROM france.france
                 where productivity is not NULL
                   and region = 'FR-01')
SELECT sum(harvest) as gross_yield
FROM harvest;

WITH harvest as (SELECT productivity * cast(area_ha as double precision) as harvest,
                        cast(area_ha as double precision)                as area_ha
                 FROM france.france
                 where productivity is not NULL
                   and region = 'FR-01')
SELECT sum(harvest) / sum(area_ha) as weighted_average_yield_per_hectare
FROM harvest;
