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

SELECT id, crop, ST_AsText(fr.wkb_geometry), ST_AsGeoJSON(fr.wkb_geometry)
FROM france.france as fr
ORDER BY id
LIMIT 10;

SELECT Find_SRID('france', 'france', 'wkb_geometry');
--4326

---task 1
Select *
FROM france.france as fr
WHERE ST_DWithin(fr.wkb_geometry::geography, (ST_SetSRID(ST_MakePoint(1.3373403, 49.9948281), 4326))::geography, 500);