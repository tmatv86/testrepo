import os

from geopy import GoogleV3, Yandex, Nominatim
import geopy
import certifi, ssl
from dotenv import load_dotenv
from geopy.distance import geodesic as GD

class Service:
    def __init__(self):
        ctx = ssl.create_default_context(cafile=certifi.where())
        geopy.geocoders.options.default_ssl_context = ctx
        load_dotenv()

    def get_my_location(self, KEY, map_location, multiple):
        pass

    def get_my_coords(self):
        pass

    def get_distance(self, coord1, coord2):
        return GD((coord1[0], coord1[1]), (coord2[0], coord2[1])).km

    def ret_location(self, location):

        coords = {}

        if len(location) <= 1:
            coords[location[0].address] = (location[0].latitude, location[0].longitude)
        else:
            for loc in location:
                coords[loc.address] = (loc.latitude, loc.longitude)
        return coords

class YService(Service):

    def __init__(self):
        super().__init__()

    def get_my_location(self, KEY, map_location, multiple):
        print('Empty since Yandex counter - 1...')
        load_dotenv()
        API_KEY = os.getenv('API_KEY')
        location = Yandex(user_agent="python-requests/2.31.0", api_key=API_KEY)
        try:
            coords = self.ret_location(location)
        except TypeError:
            print('TypeError: not found :-(')
            return {}
        return coords
class GService(Service):
    def __init__(self):
        super().__init__()

    def get_my_location(self, KEY, map_location, multiple):
        GAPI_KEY = os.getenv(KEY)

        ctx = ssl.create_default_context(cafile=certifi.where())
        geopy.geocoders.options.default_ssl_context = ctx

        location = GoogleV3(api_key=GAPI_KEY).geocode(map_location)

        try:
            coords = self.ret_location(location)
        except TypeError:
            print('TypeError: not found :-(')
            return {}
        return coords

class NService(Service):
    def __init__(self):
        super().__init__()

    def get_my_location(self, KEY, map_location, non_one):

        geolocator = Nominatim(scheme='http', user_agent="python-requests/2.31.0")
        location = geolocator.geocode(map_location, exactly_one=non_one)

        try:
            coords = self.ret_location(location)
        except TypeError:
            print('TypeError: not found :-(')
            return None
        return coords

def get_first_key(addresses, val):

    key_list = list(addresses.keys())
    val_list = list(addresses.values())
    ind = val_list.index(val)

    return key_list[ind]

def search_closest_location(lat1, long1, destination_address, geo_object):

    API = None
    if isinstance(geo_object, NService):
        API = ''
    elif isinstance(geo_object, YService):
        API = 'API_KEY'
    elif isinstance(geo_object, GService):
        API = 'GAPI_KEY'

    addresses = geo_object.get_my_location(API, destination_address, False)

    if not addresses:
        return '', ''

    min_dist = geo_object.get_distance([lat1, long1], addresses[list(addresses)[0]])
    addr = get_first_key(addresses, addresses[list(addresses)[0]])

    for k, v in addresses.items():
        dst = geo_object.get_distance([lat1, long1], [v[0], v[1]])
        if dst < min_dist:
            min_dist = dst
            addr = k

    min_dist = str(min_dist)[:4]

    return addr, min_dist
