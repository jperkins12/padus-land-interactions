from arcgis.geometry import Polygon
from shapely import wkt

from padus_land_interactions.PadusConnector import PadusConnector


test_wkt_string = "Polygon ((-121.71614033828271317 37.30714743764794861, -121.71589013202380158 37.301773880403438, -121.7049748839786929 37.30182363732431838, -121.71614033828271317 37.30714743764794861))"
test_area = Polygon().from_shapely(wkt.loads(test_wkt_string))


def test_readGeoJson() -> None:
    test_geojson = """{"type": "Polygon", "coordinates": [ [ [ -121.71614033828271, 37.30714743764795 ], [ -121.7158901320238, 37.30177388040344 ], [ -121.7049748839787, 37.30182363732432 ], [ -121.71614033828271, 37.30714743764795 ] ] ] }"""

    assert PadusConnector().readGeoJson(test_geojson) == test_area


# Sample query should return 2 features
def test_sample_query() -> None:
    padus = PadusConnector()
    query_result = padus.queryPadusIntersection(test_area)

    assert len(query_result.features) == 2  # type: ignore


def test_getIntersectionArea() -> None:
    padus = PadusConnector()
    query_result = padus.queryPadusIntersection(test_area)
    feature_list = query_result.features
    test_area2 = Polygon(feature_list[0].geometry)
    intersection_area = padus.getIntersectionArea(test_area, test_area2).area

    assert isinstance(intersection_area, float) and intersection_area > 0


def test_getAllIntersectingAreas() -> None:
    padus = PadusConnector()
    intersecting_areas_return = padus.getAllIntersectingAreas(test_area)

    assert len(intersecting_areas_return) == 2
