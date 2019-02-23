
import sys
from h3 import h3
import requests
import json
import folium
import os
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from IPython.display import display


URL = 'https://nominatim.openstreetmap.org/search.php?q=' + 'Lviv' + '+Ukraine&polygon_geojson=1&format=json'
r = requests.get(url=URL)
data = r.json()

print(data)

coords = data[0]["geojson"]["coordinates"]
for coord in coords[0]:
    coord[0], coord[1] = coord[1], coord[0]
print(coords)

geoJson = {'type': 'Polygon',
           'coordinates': coords}

# geoJson = {'type': 'Polygon',
#  'coordinates': [[[37.813318999983238, -122.4089866999972145], [ 37.7866302000007224, -122.3805436999997056 ], [37.7198061999978478, -122.3544736999993603], [ 37.7076131999975672, -122.5123436999983966 ], [37.7835871999971715, -122.5247187000021967],  [37.8151571999998453, -122.4798767000009008]]] }

polyline = geoJson['coordinates'][0]
polyline.append(polyline[0])

lat = [p[0] for p in polyline]
lng = [p[1] for p in polyline]

m = folium.Map(location=[sum(lat) / len(lat), sum(lng) / len(lng)], zoom_start=13, tiles='cartodbpositron')
my_PolyLine = folium.PolyLine(locations=polyline, weight=8, color="blue")
m.add_child(my_PolyLine)

hexagons = list(h3.polyfill(geoJson, 7))
polylines = []
lat = []
lng = []
for hex in hexagons:
    polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
    # flatten polygons into loops.
    outlines = [loop for polygon in polygons for loop in polygon]
    polyline = [outline + [outline[0]] for outline in outlines][0]
    lat.extend(map(lambda v: v[0], polyline))
    lng.extend(map(lambda v: v[1], polyline))
    polylines.append(polyline)

for polyline in polylines:
    my_PolyLine = folium.PolyLine(locations=polyline, weight=8, color='red')
    m.add_child(my_PolyLine)
display(m)
