import os

from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine(os.getenv('DB_CONNECTION_STRING'))


def get_area_db(region: str) -> float:
    with engine.connect() as conn:
        sql = text(f"""
        SELECT sum(cast(area_ha as double precision)) FROM {os.getenv('DB_SCHEMA_NAME')}.{os.getenv('DB_TABLE_NAME')}
        where region='{region}'
        group by region;
        """)
        results = conn.execute(sql)
        if len(results.fetchall()) > 0:
            return results.first()[0]


def get_gross_yield_db(region: str) -> float:
    with engine.connect() as conn:
        sql = text(f"""
                WITH harvest as (SELECT productivity * cast(area_ha as double precision) as harvest
                                 FROM {os.getenv('DB_SCHEMA_NAME')}.{os.getenv('DB_TABLE_NAME')}
                                 where productivity is not NULL
                                   and region = '{region}')
                SELECT sum(harvest) as gross_yield
                FROM harvest;
                """)
        results = conn.execute(sql)
        if len(results.fetchall()) > 0:
            return results.first()[0]


def get_weighted_average_yield_per_hectare_db(region: str) -> float:
    with engine.connect() as conn:
        sql = text(f"""
                WITH harvest as (SELECT productivity * cast(area_ha as double precision) as harvest,
                                        cast(area_ha as double precision)                as area_ha
                                 FROM {os.getenv('DB_SCHEMA_NAME')}.{os.getenv('DB_TABLE_NAME')}
                                 where productivity is not NULL
                                   and region = '{region}')
                SELECT sum(harvest) / sum(area_ha) as weighted_average_yield_per_hectare
                FROM harvest;
        """)
        results = conn.execute(sql)
        if len(results.fetchall()) > 0:
            return results.first()[0]


def get_nearby_fields_db(x: float, y: float, distance: int, crop: str):
    query = f"""Select id, crop, productivity, area_ha, region, ST_AsGeoJSON(fr.wkb_geometry)
                FROM {os.getenv('DB_SCHEMA_NAME')}.{os.getenv('DB_TABLE_NAME')} as fr
                WHERE ST_DWithin(fr.wkb_geometry::geography, (ST_SetSRID(ST_MakePoint({x}, {y}), 4326))::geography, {distance})"""
    if crop:
        query += f" AND fr.crop='{crop}'"
    query += ";"
    print(query)
    return run_query(query)


def get_fields_inside_parallelogram_db(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float,
                                       y3: float, crop: str):
    query = f"""Select id, crop, productivity, area_ha, region, ST_AsGeoJSON(fr.wkb_geometry)
                FROM {os.getenv('DB_SCHEMA_NAME')}.{os.getenv('DB_TABLE_NAME')} as fr
                WHERE ST_Contains(ST_Polygon('LINESTRING({x0} {y0},{x1} {y1},{x2} {y2},{x3} {y3},{x0} {y0})'::geometry, 4326), fr.wkb_geometry)"""
    if crop:
        query += f" AND fr.crop='{crop}'"
    query += ";"
    print(query)
    return run_query(query)


def get_intersect_fields_db(geometry: str, crop: str):
    query = f"""Select id, crop, productivity, area_ha, region, ST_AsGeoJSON(fr.wkb_geometry)
                FROM {os.getenv('DB_SCHEMA_NAME')}.{os.getenv('DB_TABLE_NAME')} as fr
                WHERE ST_Intersects(fr.wkb_geometry, ST_GeomFromText('{geometry}'))"""
    if crop:
        query += f" AND fr.crop='{crop}'"
    query += ";"
    print(query)
    return run_query(query)


def run_query(query: str):
    with engine.connect() as conn:
        sql = text(query)
        result = conn.execute(sql)
        if result.rowcount() > 0:
            return result.fetchall()


def is_valid(geom: str) -> bool:
    with engine.connect() as conn:
        sql = text(f"""
            SELECT ST_IsValid(ST_GeomFromText('{geom}'));
        """)
        result = conn.execute(sql)
        return result.first()[0]
