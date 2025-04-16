import requests

def get_lat_lon(address):
    """Fetch latitude and longitude for a given address using OpenStreetMap Nominatim API."""
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'limit': 1}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        return None, None
    except requests.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def get_address(lat, lon):
    """Fetch the address for given latitude and longitude using OpenStreetMap Nominatim API."""
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {'lat': lat, 'lon': lon, 'format': 'json'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('display_name', None)
    except requests.RequestException as e:
        print(f"Error fetching address: {e}")
        return None
