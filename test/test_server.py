from urllib import response
from helpers import SAMPLE_GEOJSON_1_PATH, load_json_as_str

from padus_land_interactions.server import app

test_json = load_json_as_str(SAMPLE_GEOJSON_1_PATH)


# test if expected data is returned from interaction query
def test_interactions():
    with app.test_client() as test_client:
        response = test_client.post("/interactions", data=test_json)
        assert response.status_code == 200
        assert len(response.json["intersecting_features"]) == 2
        assert "Joseph D. Grant Park" in [
            i["name"] for i in response.json["intersecting_features"]
        ]
        assert "feature_set_geojson" not in response.json.keys()


# ensure invalid json format returns 400
def test_invalid_geojson():
    invalid_json = load_json_as_str("test/sample_data/invalid.geojson")

    with app.test_client() as test_client:
        response = test_client.post("/interactions", data=invalid_json)
        assert response.status_code == 400
        assert response.json["error"] == "invalid geojson input"


def test_return_geojson():
    with app.test_client() as test_client:
        response = test_client.post("/interactions?geojson=true", data=test_json)
        assert "feature_set_geojson" in response.json.keys()

# return error if requested polygon is too large
def test_area_too_large():
    too_large_json = load_json_as_str("test/sample_data/too_large.geojson")

    with app.test_client() as test_client:
        response = test_client.post("interactions?geojson=true", data=too_large_json)
        assert response.status_code == 400
        assert response.json["error"] == "requested polygon area too large"