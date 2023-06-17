import sys

from arcgis.features import FeatureSet, Feature
from arcgis.geometry import Polygon, intersect
from arcgis.geometry.filters import intersects
from arcgis.gis import GIS
from shapely import from_geojson

# manager type layer: https://services.arcgis.com/v01gqwM5QqNysAAi/ArcGIS/rest/services/Manager_Type/FeatureServer


# Class for interfacing with the PADUS dataset hosted on ArcGIS online
class PadusConnector(object):
    def __init__(self) -> None:
        # Item ID points to ArcGIS online layer
        MANAGER_TYPE_ITEM_ID = "f0c68c83c88a46dcbb80fd33780ee9f5"

        gis = GIS()
        self.manager_type_layer = gis.content.get(MANAGER_TYPE_ITEM_ID).layers[0]

    @staticmethod
    def readGeoJson(geojson_str: str) -> Polygon:
        return Polygon().from_shapely(from_geojson(geojson_str))

    # Return PADUS features that intersect a given area
    def queryPadusIntersection(self, area: Polygon) -> FeatureSet:
        geom_filter = intersects(area)
        return self.manager_type_layer.query(geometry_filter=geom_filter)

    # Return intersection polygon in desired srid
    def getIntersectionArea(
        self, area1: Polygon, area2: Polygon, srid: int = 3857
    ) -> Polygon:
        area1Transformed = area1.project_as(srid)  # type: ignore
        area2Transformed = area2.project_as(srid)  # type: ignore

        intersection_result = intersect(srid, [area2Transformed], area1Transformed)  # type: ignore
        intersection_area = intersection_result[0]  # type: ignore

        return intersection_area

    def __processIntersectingFeature(
        self, area: Polygon, feature: Feature
    ) -> list[dict]:
        feature_poly = Polygon(feature.geometry)
        intersection_geom = self.getIntersectionArea(area, feature_poly)
        intersection_area = intersection_geom.project_as(3857).area
        intersection_area_pct = round(intersection_area / area.project_as(3857).area, 3)  # type: ignore

        return {
            "padus_id": feature.attributes["OBJECTID"],
            "manager_type": feature.attributes["Mang_Type"],
            "feature_class": feature.attributes["FeatClass"],
            "designation_type": feature.attributes["Des_Tp"],
            "name": feature.attributes["Loc_Nm"],
            "intersection_geom": intersection_geom.WKT,
            "intersection_area": intersection_area,
            "overlap_area_pct": intersection_area_pct,
        }  # type: ignore

    def getAllIntersectingAreas(self, area: Polygon) -> list[dict]:
        query_feature_set = self.queryPadusIntersection(area)
        intersecting_geoms = [
            self.__processIntersectingFeature(area, f)
            for f in query_feature_set.features
        ]

        return intersecting_geoms


if __name__ == "__main__":
    sys.exit()
