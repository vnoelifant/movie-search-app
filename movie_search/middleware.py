from .tmdb_api import TMDBApi
from .media import MediaService
from django.conf import settings

class TMDBApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Only create TMDBApi instance once
        self.tmdb_api = TMDBApi()
    
    def __call__(self, request):
        print("Calling before view......")
        # Attach the shared TMDBApi instance to the request
        request.tmdb_api = self.tmdb_api
        # Proceed with request processing
        response = self.get_response(request)
        print("Calling after view......")
        return response