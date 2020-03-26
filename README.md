[![Build Status](https://travis-ci.com/Tawakalt/search.svg?branch=develop)](https://travis-ci.com/Tawakalt/search) [![Coverage Status](https://coveralls.io/repos/github/Tawakalt/search/badge.svg?branch=develop)](https://coveralls.io/github/Tawakalt/search?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/25d9fc24d6db937636c3/maintainability)](https://codeclimate.com/github/Tawakalt/search/maintainability)

# Search
This service exposes a RESTful API for different clients (Web, Mobile, and more).
It lists places along with their details which match a given query. The places are retrieved from multiple providers on the internet (e.g. Google Places, Yelp, and/or Foursquare). 

### The application currently has the following features;
- It accepts query parameter(s) and search for places with the Google Places API.
- TIt also accepts location parameters (latitude, longitude) in the query and take these into consideration when querying providers.

### The response contains the following information:
- ID
- Provider
- Name
- Location (lat, lng) (if applicable)
- Address (if applicable)
- URL of the place where more details are available

## Installation and Running Locally

- Navigate to a directory using your favourite terminal
​  
- Clone this repository into that directory  
  - Using SSH: `git clone git@github.com:Tawakalt/search.git`  
  - Using HTTP: `git clone https://github.com/Tawakalt/search.git`  
 
- Navigate to the repository's directory  
  - `cd search` 

- Add a .env file in your root directory with the following
    - `API_KEY=YourGoogleAPIKey`
    - `SECRET_KEY=YourAppsSecretKey`
    - `DJANGO_DEBUG=True`
    
- Install the app's dependencies  
  - `pip install requirements` 

- Run the application  
  - `python manage.py runserver`
  - Visit `http://127.0.0.1:8000/` with the following query parameters using postman or your favourite browser
  - Input your search query parameters
    - `q - search query`
    - `source - google (others are under development)`
    - `lat and lng - (latitude and longitude optional)`

- Run Tests 
  - `python manage.py test` or
  - `coverage run manage.py test`

## Disclaimer
- This application and its functions are limited by time constraint and is in no way at its best.

## Author
- Olaniyi Tawakalt Taiwo
