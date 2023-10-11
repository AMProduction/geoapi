from typing import Union

from fastapi import FastAPI, HTTPException

from src import api_functions as af

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the GeoApi v1.0"}


@app.get("/nearby/")
async def get_nearby_fields(x: float, y: float, distance: int, crop: Union[str, None] = None):
    result = af.get_nearby_fields(x, y, distance, crop)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The fields that are 'nearby' given point within a given distance are not found")


@app.get("/inside/")
async def get_fields_inside_parallelogram(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float,
                                          y3: float, crop: Union[str, None] = None):
    result = af.get_fields_inside_parallelogram(x0, y0, x1, y1, x2, y2, x3, y3, crop)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The fields that are inside the parallelogram with given vertices are not found")


@app.get("/intersect/")
async def get_intersect_fields(geometry: str, crop: Union[str, None] = None):
    result = af.get_intersect_fields(geometry, crop)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The fields that intersect with the requested geometry are not found")


@app.get("/stats/")
async def get_region_stats(region: str):
    result = af.get_region_stats(region)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The area, gross yield, and weighted average yield per hectare in a region are not "
                                   "found")
