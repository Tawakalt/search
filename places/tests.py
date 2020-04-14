from django.test import TestCase
from .mock import *
import responses, requests


# Create your tests here.
class SearchTest(TestCase):
    
    @responses.activate
    def test_displays_result_for_found_places_without_location_params(self):
        responses.add(responses.GET, SEARCH_URL,
                    json=candidate, status=200)
        responses.add(responses.GET, DETAILS_URL,
                    json=details, status=200)

        response = self.client.get('/?q=lagos&source=google')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, RESULT)
     
    @responses.activate
    def test_displays_result_for_found_places_with_location_params(self):
        responses.add(responses.GET, SEARCH_URL_WITH_LOCATION,
                    json=candidate, status=200)
        responses.add(responses.GET, DETAILS_URL,
                    json=details, status=200)

        response = self.client.get('/?q=lagos&source=google&lng=3.3792057&lat=6.5243793')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, RESULT)

    @responses.activate
    def test_displays_empty_result_if_place_not_found(self):
        responses.add(responses.GET, ZERO_SEARCH_URL,
                    json=no_candidate, status=200)
        
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

    def test_all_undefined_endpoints_return_404_error(self):
        response = self.client.get('/aaaa')
        error = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(error, {'error': 'PAGE NOT FOUND'})

    @responses.activate
    def test_app_exits_gracefully_with_bad_url(self):
        responses.add(responses.GET, SEARCH_URL,
                    json=candidate, status=200)
        responses.add(responses.GET, DETAILS_URL,
                    json=wrong, status=500)
        response = self.client.get('/?q=lagos&source=google')
        data = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['status'], 'INTERNAL SERVER ERROR')
        self.assertEqual(data['error'], 'There was an issue while trying to use google API')    
