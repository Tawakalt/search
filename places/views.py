from django.http import JsonResponse
import requests, json, os
from . import sources


def index(request): 
    q = request.GET.get("q", False)
    source = request.GET.get("source", False)
    if not (q and source):
        data = {
        'status': 'INVALID REQUEST',
        'error': 'Parameters q and source are required'
        }
        return JsonResponse(data, status=400) 
    
    if source.lower() == 'google':
        return sources.google(request)
    
    data = {
        'status': 'INVALID REQUEST',
        'error': 'Other Sources are still under development, please choose google as source'
    }
    return JsonResponse(data, status=400) 

def others(request):
    return JsonResponse({'error': 'PAGE NOT FOUND'}, status=404)
    

 