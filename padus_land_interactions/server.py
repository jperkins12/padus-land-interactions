import logging
import ngrok
from flask import Flask, request
from shapely.errors import GEOSException

from padus_land_interactions.PadusConnector import PadusConnector

logging.basicConfig(level=logging.INFO)
# tunnel = ngrok.werkzeug_develop()

app = Flask(__name__)

padus = PadusConnector()


# endpoint for querying land interactions
@app.route("/interactions", methods=["POST"])
def getPadusInteractions():
    request_geom = PadusConnector().readGeoJson(request.data)  # type: ignore

    get_geojson = False
    if request.args.get("geojson", "false").lower() == "true":
        get_geojson = True

    intersections = padus.getAllIntersectingAreas(request_geom, geojson=get_geojson)
    print(intersections)
    return intersections


# handle invalid json error
@app.errorhandler(GEOSException)
def invalidGeojson(e):
    return {"error": "invalid geojson input"}, 400


if __name__ == "__main__":
    app.run("localhost", port=8000, debug=True)
