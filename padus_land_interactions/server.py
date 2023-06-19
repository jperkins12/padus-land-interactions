from flask import Flask, request
from shapely.errors import GEOSException

from padus_land_interactions.PadusConnector import PadusConnector

app = Flask(__name__)

padus = PadusConnector()


# endpoint for querying land interactions
@app.route("/interactions", methods=["POST"])
def getPadusInteractions():
    request_geom = PadusConnector().readGeoJson(request.data)  # type: ignore

    intersections = padus.getAllIntersectingAreas(request_geom)
    return [i.dict() for i in intersections]


# handle invalid json error
@app.errorhandler(GEOSException)
def invalidGeojson(e):
    return {"error": "invalid geojson input"}, 400


if __name__ == "__main__":
    app.run("localhost", port=8000, debug=True)
