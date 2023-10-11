from typing import Union

from fastapi import FastAPI, HTTPException

from src import api_functions as af

tags_metadata = [{"name": "nearby",
                  "description": "Get the set of fields that are 'nearby' given point within a given distance."},
                 {"name": "inside",
                  "description": "Get the set of fields that are inside the parallelogram with given vertices"},
                 {"name": "intersect",
                  "description": "Get the set of fields that intersect with the requested geometry"},
                 {"name": "stats",
                  "description": "Get the area, gross yield, and weighted average yield per hectare in a region"}]

description = """

## Nearby

Get the set of fields that are "nearby" given point within a given distance. Point and distance are sent by the user. 
Radius is meant to be in meters.

## Inside

Get the set of fields that are inside the parallelogram with given vertices. Vertices are sent by the user.

## Intersect

Get the set of fields that intersect with the requested geometry. Geometry is sent by the user.

## Stats

Get the area, gross yield, and weighted average yield per hectare in a region that was sent by the user.

"""

app = FastAPI(title="GeoAPI", description=description, openapi_tags=tags_metadata,
              summary="Designed and implemented the API that allows customers to retrieve geometries from the "
                      "Database by given parameters", version="1.0.0",
              contact={"name": "Andrii Malchyk", "url": "https://www.linkedin.com/in/andrii-malchyk/",
                       "email": "snooki17@gmail.com", }, license_info={"name": "Apache 2.0", "identifier": "MIT", }, )


@app.get("/")
async def root():
    return {"message": "Welcome to the GeoApi v1.0"}


@app.get("/nearby/", tags=["nearby"])
async def get_nearby_fields(x: float, y: float, distance: int, crop: Union[str, None] = None):
    result = af.get_nearby_fields(x, y, distance, crop)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The fields that are 'nearby' given point within a given distance are not found")


@app.get("/inside/", tags=["inside"])
async def get_fields_inside_parallelogram(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float,
                                          y3: float, crop: Union[str, None] = None):
    result = af.get_fields_inside_parallelogram(x0, y0, x1, y1, x2, y2, x3, y3, crop)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The fields that are inside the parallelogram with given vertices are not found")


@app.get("/intersect/", tags=["intersect"])
async def get_intersect_fields(geometry: str, crop: Union[str, None] = None):
    result = af.get_intersect_fields(geometry, crop)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The fields that intersect with the requested geometry are not found")


@app.get("/stats/", tags=["stats"])
async def get_region_stats(region: str):
    result = af.get_region_stats(region)
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail="The area, gross yield, and weighted average yield per hectare in a region are not "
                                   "found")
