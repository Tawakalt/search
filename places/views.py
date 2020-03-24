from django.http import JsonResponse
import requests, json, os
from dotenv import load_dotenv

# reading .env file
load_dotenv()


def index(request, pk): 
    API_KEY = os.getenv('API_KEY')
    searchUrl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&"
    searchResponse = requests.get(f'{searchUrl}input={pk}&key={API_KEY}') 
    placeSearch = searchResponse.json()

    if placeSearch['candidates']:
        places = placeSearch['candidates']
        place_id = places[0]['place_id']
        detailsUrl = "https://maps.googleapis.com/maps/api/place/details/json?place_id="
        detailsResponse = requests.get(f'{detailsUrl}{place_id}&key={API_KEY}')
        details = detailsResponse.json()
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
    else:
        needed = []
        status = placeSearch['status']
    
    data = {
        'status': status,
        'result': needed
    }
        
    return JsonResponse(data)
