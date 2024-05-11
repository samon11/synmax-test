from flask import Flask, request, jsonify
from shapely.geometry import Point, Polygon
from db import WellRepository

repo = WellRepository()
app = Flask(__name__)

@app.route("/well", methods=["GET"])
def get_well_data():
    api = request.args.get("api")
    value = repo.get_well(api)
    
    if value:
        return jsonify(value)
    
    return jsonify({"message": "Well API not found"}), 404

@app.route("/polygon", methods=["GET"])
def get_wells_in_polygon():
    body = request.get_json()
    polygon_coords = body["polygon"]

    # most DBMs have a spatial query that can be used to do this more efficiently
    # here, I'll get all and search the 480 wells linearly for our purposes
    results = []
    polygon = Polygon(polygon_coords)
    for well in repo.get_all_coords():
        point = Point(well["Latitude"], well["Longitude"])

        if point.within(polygon):
            results.append(well['API'])

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
