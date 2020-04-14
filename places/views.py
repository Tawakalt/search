from django.http import JsonResponse
from .sources import google
import requests, json, os


def index(request): 
    q = request.GET.get("q", '')
    source = request.GET.get("source", '')
    lng = request.GET.get("lng", '')
    lat = request.GET.get("lat", '')
    if not (q and source):
        data = {
        'status': 'INVALID REQUEST',
        'error': 'Parameters q and source are required'
        }
        return JsonResponse(data, status=400) 
    
    if source.lower() == 'google':
        return google(q, source, lng, lat)
    
    data = {
        'status': 'INVALID REQUEST',
        'error': 'Other Sources are still under development, please choose google as source'
    }
    return JsonResponse(data, status=400) 

def others(request):
    return JsonResponse({'error': 'PAGE NOT FOUND'}, status=404)
