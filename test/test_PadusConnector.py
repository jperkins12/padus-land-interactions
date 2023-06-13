from arcgis.geometry import Polygon
from shapely import wkt

from padus_land_interactions.PadusConnector import PadusConnector


# Sample query should return 2 features
def test_sample_query() -> None:
    test_wkt_string = "Polygon ((-121.71614033828271317 37.30714743764794861, -121.71589013202380158 37.301773880403438, -121.7049748839786929 37.30182363732431838, -121.71614033828271317 37.30714743764794861))"
    test_area = Polygon().from_shapely(wkt.loads(test_wkt_string))

    padus = PadusConnector()
    query_result = padus.queryPadusIntersection(test_area)

    assert len(query_result.features) == 2 # type: ignore