# Constants
SAMPLE_GEOJSON_1_PATH = "test/sample_data/sample_1.geojson"


# simple json reader
def load_json_as_str(path: str) -> str:
    with open(path, "r") as f:
        data = f.read()
    return data
