from geoalchemy2 import Geometry  # <= not used but must be imported
from sqlalchemy import create_engine, Table, Column, Integer, VARCHAR, Numeric, MetaData

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgis_db")

conn = engine.connect()
# initialize the Metadata Object
meta = MetaData()

# create a table schema
france = Table('france', meta, schema='france', autoload_with=engine)

result = conn.execute(france.select().where(france.c.id == 6522894))

# Print the results
for row in result:
    print(row)

result = conn.execute(france.select().where(france.c.crop == 'wheat_winter'))

# Print the results
for row in result:
    print(row)