from django.test import TestCase

# Create your tests here.
class SearchTest(TestCase):
    def test_displays_result_for_found_places(self):
        result = {
            "ID": "f5e45a1cb67f5581896d92388b6402c552e4d5f0", 
            "Provider": "GOOGLE", 
            "Name": "Lagos", 
            "Location": {"Lat": 6.5243793, "Lng": 3.3792057}, 
            "Address": "Lagos, Nigeria", 
            "URI": "https://maps.google.com/?q=Lagos,+Nigeria&ftid=0x103b8b2ae68280c1:0xdc9e87a367c3d9cb"
        }

        response = self.client.get('/lagos')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'OK')
        self.assertEqual(data['result'], result)

    def test_displays_empty_result_if_place_not_found(self):
        result = []
        response = self.client.get('/xxxx')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ZERO_RESULTS')
        self.assertEqual(data['result'], result)
