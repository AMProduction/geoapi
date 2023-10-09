from src import db_tools


def get_region_stats(region: str) -> dict:
    # TODO: add region string validation (REGEXP)
    area = db_tools.get_area_db(region)
    gross_yield = db_tools.get_gross_yield_db(region)
    weighted_average_yield_per_hectare = db_tools.get_weighted_average_yield_per_hectare_db(region)
    return {"total_area": area, "total_yield": gross_yield, "average_yield": weighted_average_yield_per_hectare}


def get_nearby_fields(x: float, y: float, distance: int) -> dict:
    for row in db_tools.get_nearby_fields_db(x, y, distance):
        print(row)
        print(type(row))