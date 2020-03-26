from django.test import TestCase
from . import mock
import responses, requests, os

API_KEY = os.getenv('API_KEY')
Q = 'lagos'
SOURCE = 'google'
LNG = 3.3792057
LAT = 6.5243793
PLACE_ID = "ChIJwYCC5iqLOxARy9nDZ6OHntw"
COMMON = "https://maps.googleapis.com/maps/api/place/"
URL = f"{COMMON}findplacefromtext/json?inputtype=textquery&key={API_KEY}&input="
ZERO_SEARCH_URL = f"{URL}xxxx"
SEARCH_URL = f"{URL}{Q}"
SEARCH_URL_WITH_LOCATION = f"{SEARCH_URL}&locationbias=point:{LNG},{LAT}"
DETAILS_URL = f"{COMMON}details/json?place_id={PLACE_ID}&key={API_KEY}"
DETAILS = mock.details
NO_CANDIDATE = mock.no_candidate
CANDIDATE = mock.candidate
RESULT = {
    'status': 'OK',
    'result': {
        "ID": "f5e45a1cb67f5581896d92388b6402c552e4d5f0", 
        "Provider": "GOOGLE", 
        "Name": "Lagos", 
        "Location": {"Lat": LAT, "Lng": LNG}, 
        "Address": "Lagos, Nigeria", 
        "URI": "https://maps.google.com/?q=Lagos,+Nigeria&ftid=0x103b8b2ae68280c1:0xdc9e87a367c3d9cb"
    }
}
ZERO_RESULT = {'status': 'ZERO_RESULTS', 'result': []}


# Create your tests here.
class SearchTest(TestCase):
    
    @responses.activate
    def test_displays_result_for_found_places_without_location_params(self):
        responses.add(responses.GET, SEARCH_URL,
                    json=CANDIDATE, status=200)
        responses.add(responses.GET, DETAILS_URL,
                    json=DETAILS, status=200)

        response = self.client.get('/?q=lagos&source=google')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, RESULT)
     
    @responses.activate
    def test_displays_result_for_found_places_with_location_params(self):
        responses.add(responses.GET, SEARCH_URL_WITH_LOCATION,
                    json=CANDIDATE, status=200)
        responses.add(responses.GET, DETAILS_URL,
                    json=DETAILS, status=200)

        response = self.client.get('/?q=lagos&source=google&lng=3.3792057&lat=6.5243793')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, RESULT)

    @responses.activate
    def test_displays_empty_result_if_place_not_found(self):
        responses.add(responses.GET, ZERO_SEARCH_URL,
                    json=NO_CANDIDATE, status=200)
        
        response = self.client.get('/?q=xxxx&source=google')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, ZERO_RESULT)

    def test_displays_error_if_search_params_and_source_not_included(self):
        response = self.client.get('/')
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'INVALID REQUEST')
        self.assertEqual(data['error'], 'Parameters q and source are required')

    def test_displays_error_if_source_is_not_google(self):
        response = self.client.get('/?q=lagos&source=yelp')
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'INVALID REQUEST')
        self.assertEqual(data['error'], 'Other Sources are still under development, please choose google as source')
