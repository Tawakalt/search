from django.http import JsonResponse
from urllib.parse import urlencode, quote_plus
import requests, json, os


def google(q, source, lng, lat):
    API_KEY = os.getenv('API_KEY')
    searchUrl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    location = ''

    if lng and lat:
        location = f'&locationbias=point:{lat},{lng}'
    searchParameters = {
        'inputtype': 'textquery',
        'input': q,
        'key': API_KEY
    }
    encodedSearchUrl = urlencode(searchParameters, quote_via=quote_plus)
    searchResponse = requests.get(f'{searchUrl}{encodedSearchUrl}{location}')
    placeSearch = searchResponse.json()

    if placeSearch['candidates']:
        places = placeSearch['candidates']
        place_id = places[0]['place_id']
        detailsUrl = "https://maps.googleapis.com/maps/api/place/details/json?"
        detailsParameters = {
            'place_id': place_id,
            'key': API_KEY
        }
        encodedDetailsUrl = urlencode(detailsParameters, quote_via=quote_plus)
        detailsResponse = requests.get(f'{detailsUrl}{encodedDetailsUrl}')
        details = detailsResponse.json()

        if (details['status'] == "OK"):
            result = details['result']
            needed = {
                'ID': result['id'],
                'Provider': result['scope'],
                'Name': result['name'],
                'Location': {
                    'Lat': result['geometry']['location']['lat'],
                    'Lng': result['geometry']['location']['lng'],
                },
                'Address': result['formatted_address'],
                'URI': result['url']
            }
            status = 'OK'
            data = {
                'status': status,
                'result': needed
            }
            return JsonResponse(data)
        data = {
                'status': 'INTERNAL SERVER ERROR',
                'error': 'There was an issue while trying to use google API'
            }
        return JsonResponse(data, status=500)
    data = {
        'status': placeSearch['status'],
        'result': []
    }
    return JsonResponse(data)  
