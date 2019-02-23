import csv
from h3 import h3
import requests
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json


city = 'Lviv'
URL = 'https://nominatim.openstreetmap.org/search.php?q=' + city + '+Ukraine&polygon_geojson=1&format=json'
r = requests.get(url=URL)
data = r.json()

coords = data[0]["geojson"]["coordinates"]
for coord in coords[0]:
    coord[0], coord[1] = coord[1], coord[0]

geoJson = {'type': 'Polygon',
           'coordinates': coords}
polygons = list(h3.polyfill(geoJson, 7))
hexagons = []
for hexagon in polygons:
    borders = h3.h3_to_geo_boundary(hexagon)
    hexagons.append({'id': hexagon,
                     'borders': Polygon(tuple(borders))})

with open('test.csv', 'r') as f:
    reader = csv.reader(f, delimiter='|')
    headers = next(reader, None)
    rides = []
    for row in reader:
        column = {}

        for h in headers:
            column[h] = []

        for h, v in zip(headers, row):
            column[h].append(v)
        rides.append(column)

for hexagon in hexagons:
    points = []
    for ride in rides:
        point_cortege = Point(tuple([float(ride['pickup_lat'][0]), float(ride['pickup_lng'][0])]))
        if point_cortege.within(hexagon['borders']):
            points.append(ride['created_at'][0])
    filename = './clusters/' + hexagon['id'] + '.json'
    f = open(filename, "w")
    f.write(json.dumps(points))