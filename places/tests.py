from django.test import TestCase

# Create your tests here.
class SearchTest(TestCase):
    result = {
            "ID": "f5e45a1cb67f5581896d92388b6402c552e4d5f0", 
            "Provider": "GOOGLE", 
            "Name": "Lagos", 
            "Location": {"Lat": 6.5243793, "Lng": 3.3792057}, 
            "Address": "Lagos, Nigeria", 
            "URI": "https://maps.google.com/?q=Lagos,+Nigeria&ftid=0x103b8b2ae68280c1:0xdc9e87a367c3d9cb"
        }
    def test_displays_result_for_found_places_without_location_params(self):
        response = self.client.get('/?q=lagos&source=google')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['result'], self.result)

    def test_displays_result_for_found_places_with_location_params(self):
        response = self.client.get('/?q=lagos&source=google&lng=3.3792057&lat=6.5243793')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['result'], self.result)

    def test_displays_empty_result_if_place_not_found(self):
        result = []
        response = self.client.get('/?q=xxxx&source=google')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ZERO_RESULTS')
        self.assertEqual(data['result'], result)

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
