from fastapi import FastAPI
from src import api_functions as af

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/nearby/")
async def get_nearby_fields(point: int, distance: int):
    return {"point": point, "distance": distance}


@app.get("/inside/")
async def get_fields_inside_parallelogram(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int):
    return {"message": "inside"}


@app.get("/intersect/")
async def get_intersect_fields(geometry: str):
    return {"geometry": geometry}


@app.get("/stats/")
async def get_region_stats(region: str):
    return af.get_region_stats(region)
