# padus-land-interactions
API for querying land interactions with PADUS database. Details on the PADUS dataset can be found [here](https://services.arcgis.com/v01gqwM5QqNysAAi/ArcGIS/rest/services/Manager_Type/FeatureServer).

## Installation
### Docker
Running in a docker container is the easiest method. Build the container with
```
docker build -t padus-interactions-api .
```
Then run with
```
docker run -p 8000:8000 padus-interactions-api
```
By default the API is accessible via localhost (`0.0.0.0`).

### Local Install
[Poetry](https://python-poetry.org/) is used for dependency managment. It will both create a virtual environment and install the necessary dependencies. This project requires python 3.9 to be installed beforehand. To initialize the project, navigate to the repo directory and enter
```
poetry install
```
The API can then be initialized with the command
```
poetry run python padus_land_interactions/server.py
```
which takes the following optional arguments:
- `--debug` - Start in flask debug mode.
- `--ngrok` - Open an ngrok tunnel, requires ngrok to be installed on the machine.

## API Usage
The API contains a single endpoint `interactions` that is called with the `POST` method (For example, `http://localhost:8000/interactions`). The body of the API request should be a polygon in GeoJson format using WGS84 coordinates. For example:
```json
{
    "type": "Polygon",
    "coordinates": [
        [
            [
                -121.71614033828271,
                37.30714743764795
            ],
            [
                -121.7158901320238,
                37.30177388040344
            ],
            [
                -121.7049748839787,
                37.30182363732432
            ],
            [
                -121.71614033828271,
                37.30714743764795
            ]
        ]
    ]
}
```
It also accepts the url parameter `geojson` which will trigger the inclusion of intersecting features in GeoJson format.

An example return is
```json
{
    "intersecting_features": [
        {
            "designation_type": "LP",
            "feature_class": "Fee",
            "intersection_area": 14286.273550175329,
            "intersection_geom": "MULTIPOLYGON (((-121.70961364223804 37.30403548946145, -121.71206470806717 37.30520418021373, -121.71116303488051 37.30402599740995, -121.70961364223804 37.30403548946145)))",
            "manager_type": "LOC",
            "name": "Joseph D. Grant Park",
            "overlap_area_pct": 0.031,
            "padus_id": 250462
        },
        {
            "designation_type": "CONE",
            "feature_class": "Easement",
            "intersection_area": 95652.71757405238,
            "intersection_geom": "MULTIPOLYGON (((-121.70497488404465 37.301823637585876, -121.70954484655861 37.30400268671565, -121.71090269502635 37.304012768986595, -121.70920163532286 37.30180436995412, -121.70497488404465 37.301823637585876)))",
            "manager_type": "NGO",
            "name": "Mount Hamilton Range West Easement",
            "overlap_area_pct": 0.209,
            "padus_id": 431357
        }
    ]
}
```
Where:
- `padus_id` is the `OBJECTID` of the intersecting feature from the PADUS dataset.
- `designation_type`, `feature_class`, `manager_type`, and name are attrubutes in the PADUS dataset
- `intersection_area` is the area in square meters that the polygon from the request overlaps with the feature.
- `intersection_geom` is the geomery of the intersection in SRID 4326.
- `overlap_ara_pct` is the percent of the request geometry area that overlaps with the intersecting PADUS feature.

If `geojson` is set to `true` in the request then the return body will also feature a `feature_set_geojson` element containing a list of the full geometries of intersecting features.

## Errors
If an error is encountered, the return body will contain a single element `error` with a description of the issue. For example:
```json
{"error": "invalid geojson input"}
```
