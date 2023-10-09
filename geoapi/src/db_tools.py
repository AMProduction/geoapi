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
        return results.first()[0]


def get_nearby_fields_db(x: float, y: float, distance: int):
    with engine.connect() as conn:
        # # initialize the Metadata Object
        # meta = MetaData()
        # # create a table schema
        # france = Table('france', meta, schema='france', autoload_with=engine)
        sql = text(f"""
            Select *
            FROM {os.getenv('DB_SCHEMA_NAME')}.{os.getenv('DB_TABLE_NAME')} as fr
            WHERE ST_DWithin(fr.wkb_geometry::geography, (ST_SetSRID(ST_MakePoint({x}, {y}), 4326))::geography, {distance});
        """)
        result = conn.execute(sql)
        return result.fetchall()
