import logging
from argparse import ArgumentParser, Namespace

import ngrok
from flask import Flask, request
from shapely.errors import GEOSException

from padus_land_interactions.PadusConnector import PadusConnector

class AreaTooLargeException(Exception):
    "Raised if the area of the polygon is too large to process"
    pass

def getOptions() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument("--debug", action="store_true", help="Enable flask debug mode")
    parser.add_argument("--ngrok", action="store_true", help="Start ngrok tunnel")

    args, uknown = parser.parse_known_args()

    return args


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

padus = PadusConnector()


# endpoint for querying land interactions
@app.route("/interactions", methods=["POST"])
def getPadusInteractions():
    request_geom = PadusConnector().readGeoJson(request.data)  # type: ignore

    if PadusConnector().checkArea(request_geom):
        raise AreaTooLargeException

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

# handle area too large error
@app.errorhandler(AreaTooLargeException)
def areaTooLarge(e):
    return {"error": "requested polygon area too large"}, 400


if __name__ == "__main__":
    args = getOptions()
    debug = False
    if args.debug:
        debug = True
    if args.ngrok:
        tunnel = ngrok.werkzeug_develop()
    app.run("0.0.0.0", port=8000, debug=debug)
