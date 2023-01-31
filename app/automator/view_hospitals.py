from pykml import parser

filename = 'templates/hospitals.kml'

with open(filename) as file:
    root = parser.parse(file).getroot()
    pms = root.findall('.//{http://earth.google.com/kml/2.1}Placemark')

    for pm in pms:
        print(pm.name)
        print(pm.Point.coordinates.text.split(','))
