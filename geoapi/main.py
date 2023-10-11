from fastapi import FastAPI

from src import api_functions as af

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/nearby/")
async def get_nearby_fields(x: float, y: float, distance: int):
    return af.get_nearby_fields(x, y, distance)


@app.get("/inside/")
async def get_fields_inside_parallelogram(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float,
                                          y3: float):
    return af.get_fields_inside_parallelogram(x0, y0, x1, y1, x2, y2, x3, y3)


@app.get("/intersect/")
async def get_intersect_fields(geometry: str):
    return af.get_intersect_fields(geometry)


@app.get("/stats/")
async def get_region_stats(region: str):
    return af.get_region_stats(region)
