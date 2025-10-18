import requests
from datetime import datetime
from django.core.cache import cache
from .models import Film


class SWAPIService:
    """
    Service class to interact with SWAPI
    """
    BASE_URL = "https://swapi.dev/api"
    CACHE_TIMEOUT = 3600  # 1 hour
    
    def get_films(self):
        """
        Fetch all films from SWAPI with caching
        """
        cache_key = 'swapi_films'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            response = requests.get(f"{self.BASE_URL}/films/", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            cache.set(cache_key, data['results'], self.CACHE_TIMEOUT)
            return data['results']
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch films from SWAPI: {str(e)}")
    
    def sync_films(self):
        """
        Sync films from SWAPI to local database
        """
        films_data = self.get_films()
        films_synced = 0
        
        for film_data in films_data:
            # Extract film ID from URL
            swapi_id = int(film_data['url'].rstrip('/').split('/')[-1])
            
            # Parse release date
            release_date = datetime.strptime(
                film_data['release_date'], 
                '%Y-%m-%d'
            ).date()
            
            # Create or update film
            film, created = Film.objects.update_or_create(
                swapi_id=swapi_id,
                defaults={
                    'title': film_data['title'],
                    'episode_id': film_data['episode_id'],
                    'opening_crawl': film_data['opening_crawl'],
                    'director': film_data['director'],
                    'producer': film_data['producer'],
                    'release_date': release_date,
                }
            )
            
            if created or film:
                films_synced += 1
        
        return films_synced