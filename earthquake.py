""" Using python's built-in data manipulation facilities. You just gotta love'em. """
import bz2
import json
import logging as log
from datetime import date
from pprint import pp as prettyprint
from collections import Counter
# from itertools import groupby   # group by groups censecutively


# pylint: disable=pointless-string-statement
"""
{
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": 1.09,
        "place": "6km NW of The Geysers, CA",
        "time": 1678089235550,
        "updated": 1678089330139,
        "tz": null,
        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/nc73856011",
        "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/nc73856011.geojson",
        "felt": null,
        "cdi": null,
        "mmi": null,
        "alert": null,
        "status": "automatic",
        "tsunami": 0,
        "sig": 18,
        "net": "nc",
        "code": "73856011",
        "ids": ",nc73856011,",
        "sources": ",nc,",
        "types": ",nearby-cities,origin,phase-data,",
        "nst": 24,
        "dmin": 0.008006,
        "rms": 0.02,
        "gap": 40,
        "magType": "md",
        "type": "earthquake",
        "title": "M 1.1 - 6km NW of The Geysers, CA"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          -122.8066635,
          38.815834,
          1.51
        ]
      },
      "id": "nc73856011"
    }
  ]
}
"""

log.basicConfig(level=log.DEBUG, format="%(levelname)s: %(filename)s#%(lineno)d: %(message)s")
with bz2.open('earthquake.bz2') as fp:
    data = json.load(fp)

info = f"{data['metadata']['title']} - #{data['metadata']['count']} items\n\
{data['metadata']['url']}"
log.info(info)

data = data['features']


def get_mag(dat):
    return float(dat['properties'].get('mag', 0))


def pluck_data(dat):
    return {
        "place": dat['properties']['place'],
        "magnitude": get_mag(dat),
        "date": str(date.fromtimestamp(dat['properties']['time']/1000))
    }


# min and max by using key fn
print("minimum magnitude\n", min(data, key=get_mag))
print("maximum magnitude\n", max(data, key=get_mag))

# any earthquakes felt by more than 800 people?
print(any(q['properties']['felt'] is not None and q['properties']['felt'] > 800
          for q in data))

# nr of quakes bigger than 6
print(sum(get_mag(q) >= 6 for q in data))

# transform
print('some items where magnitude is >= 6.0:')
prettyprint([pluck_data(x) for x in data if get_mag(x) >= 6])

# sorting
print(*[f"{x['properties']['mag']} -- {x['properties']['title']}"
      for x in sorted(data, key=get_mag, reverse=1)[:10]], sep="\n")


# filtering -- or [x for x in data if x['x'] != 'z']
print('Not earthquakes #:', len(
        [*filter(lambda x: x['properties']['type'] != 'earthquake', data)]
    ))

print('Count of events:',
      *Counter(x['properties']['type'] for x in data).items())
