import json

from src import db_tools


def get_region_stats(region: str) -> dict:
    # TODO: add region string validation (REGEXP)
    area = db_tools.get_area_db(region)
    gross_yield = db_tools.get_gross_yield_db(region)
    weighted_average_yield_per_hectare = db_tools.get_weighted_average_yield_per_hectare_db(region)
    return {"total_area": area, "total_yield": gross_yield, "average_yield": weighted_average_yield_per_hectare}


def get_nearby_fields(x: float, y: float, distance: int) -> dict:
    query_result = db_tools.get_nearby_fields_db(x, y, distance)
    GeoJSON = create_GeoJSON(query_result)
    return GeoJSON


def create_GeoJSON(query_result) -> dict:
    features = []
    for row in query_result:
        geometry = json.loads(row[5])
        properties = {"crop": row[1], "productivity_estimation": row[2], "region_code": row[4], "area_ha": row[3]}
        feature = {"type": "Feature", "id": row[0], "geometry": geometry, "properties": properties}
        features.append(feature)
    GeoJSON = {"type": "FeatureCollection", "features": features}
    return GeoJSON
