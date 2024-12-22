import requests
from typing import Dict, List, Optional, Union
import logging
from .exceptions import TMDBAPIError
from .constants import BASE_URL, DEFAULT_LANGUAGE, SORT_OPTIONS

class TMDB:
    """
    A wrapper class for The Movie Database (TMDB) API.
    
    This class provides methods to interact with TMDB's API endpoints for movies,
    TV shows, and people.
    
    Examples:
        >>> tmdb = TMDB("your_api_key_here")
        >>> movies = tmdb.search_movies("The Matrix")
        >>> movie_details = tmdb.get_movie_details(603)
    """
    
    def __init__(self, api_key: str, language: str = DEFAULT_LANGUAGE):
        """
        Initialize the TMDB API wrapper.
        
        Args:
            api_key (str): Your TMDB API key
            language (str, optional): Preferred language for responses. Defaults to "en-US"
            
        Raises:
            TMDBException: If the API key is invalid
        """
        self.api_key = api_key
        self.base_url = BASE_URL
        self.language = language
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json;charset=utf-8"
        }
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Validate API key
        try:
            self._make_request("/authentication/token/new")
        except TMDBAPIError as e:
            if e.status_code == 401:
                raise TMDBException("Invalid API key provided")
            raise

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make an HTTP GET request to the TMDB API.
        
        Args:
            endpoint (str): API endpoint to call
            params (Dict, optional): Query parameters for the request
            
        Returns:
            Dict: JSON response from the API
            
        Raises:
            TMDBAPIError: If the request fails
        """
        if params is None:
            params = {}
            
        params["language"] = self.language
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_message = str(e)
            if response.content:
                try:
                    error_data = response.json()
                    error_message = error_data.get("status_message", str(e))
                except ValueError:
                    pass
            raise TMDBAPIError(response.status_code, error_message)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise TMDBException(f"Request failed: {str(e)}")
    
    def search_movies(self, query: str, page: int = 1) -> Dict:
        """
        Search for movies by title.
        
        Args:
            query (str): The movie title to search for
            page (int, optional): Page number for results. Defaults to 1
            
        Returns:
            Dict: Search results including movie details
            
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> results = tmdb.search_movies("Inception")
            >>> print(results["results"][0]["title"])
        """
        endpoint = "/search/movie"
        params = {"query": query, "page": page}
        return self._make_request(endpoint, params)

    def get_movie_details(self, movie_id: int, append_to_response: str = None) -> Dict:
        """
        Get detailed information about a specific movie.
        
        Args:
            movie_id (int): TMDB movie ID
            append_to_response (str, optional): Additional data to append to response
                (e.g., "credits,videos,images")
                
        Returns:
            Dict: Detailed movie information
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> movie = tmdb.get_movie_details(603)
            >>> print(movie["title"])
        """
        endpoint = f"/movie/{movie_id}"
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        return self._make_request(endpoint, params)

    def get_movie_credits(self, movie_id: int) -> Dict:
        """
        Get cast and crew information for a movie.
        
        Args:
            movie_id (int): TMDB movie ID
            
        Returns:
            Dict: Cast and crew information
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> credits = tmdb.get_movie_credits(603)
            >>> print(credits["cast"][0]["name"])
        """
        endpoint = f"/movie/{movie_id}/credits"
        return self._make_request(endpoint)

    def get_popular_movies(self, page: int = 1) -> Dict:
        """
        Get a list of currently popular movies.
        
        Args:
            page (int, optional): Page number for results. Defaults to 1
            
        Returns:
            Dict: List of popular movies
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> popular_movies = tmdb.get_popular_movies()
            >>> print(popular_movies["results"][0]["title"])
        """
        endpoint = "/movie/popular"
        params = {"page": page}
        return self._make_request(endpoint, params)

    def search_tv_shows(self, query: str, page: int = 1) -> Dict:
        """
        Search for TV shows by title.
        
        Args:
            query (str): The TV show title to search for
            page (int, optional): Page number for results. Defaults to 1
            
        Returns:
            Dict: Search results including TV show details
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> results = tmdb.search_tv_shows("Breaking Bad")
            >>> print(results["results"][0]["name"])
        """
        endpoint = "/search/tv"
        params = {"query": query, "page": page}
        return self._make_request(endpoint, params)

    def get_tv_show_details(self, tv_id: int, append_to_response: str = None) -> Dict:
        """
        Get detailed information about a specific TV show.
        
        Args:
            tv_id (int): TMDB TV show ID
            append_to_response (str, optional): Additional data to append to response
                (e.g., "credits,videos,images")
                
        Returns:
            Dict: Detailed TV show information
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> tv_show = tmdb.get_tv_show_details(1396)
            >>> print(tv_show["name"])
        """
        endpoint = f"/tv/{tv_id}"
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        return self._make_request(endpoint, params)

    def get_person_details(self, person_id: int) -> Dict:
        """
        Get detailed information about a specific person.
        
        Args:
            person_id (int): TMDB person ID
            
        Returns:
            Dict: Detailed person information
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> person = tmdb.get_person_details(287)
            >>> print(person["name"])
        """
        endpoint = f"/person/{person_id}"
        return self._make_request(endpoint)

    def discover_movies(self, 
                       sort_by: str = "popularity.desc",
                       year: Optional[int] = None,
                       genre_ids: Optional[List[int]] = None,
                       page: int = 1) -> Dict:
        """
        Discover movies based on various criteria.
        
        Args:
            sort_by (str, optional): Sorting criteria. Defaults to "popularity.desc"
            year (int, optional): Filter by year
            genre_ids (List[int], optional): Filter by genre IDs
            page (int, optional): Page number for results. Defaults to 1
            
        Returns:
            Dict: List of discovered movies
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> movies = tmdb.discover_movies(sort_by="vote_average.desc", year=2020)
            >>> print(movies["results"][0]["title"])
        """
        endpoint = "/discover/movie"
        params = {"sort_by": sort_by, "page": page}
        
        if year:
            params["year"] = year
        if genre_ids:
            params["with_genres"] = ",".join(map(str, genre_ids))
            
        return self._make_request(endpoint, params)

    def get_movie_recommendations(self, movie_id: int, page: int = 1) -> Dict:
        """
        Get movie recommendations based on a movie.
        
        Args:
            movie_id (int): TMDB movie ID
            page (int, optional): Page number for results. Defaults to 1
            
        Returns:
            Dict: List of recommended movies
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> recommendations = tmdb.get_movie_recommendations(603)
            >>> print(recommendations["results"][0]["title"])
        """
        endpoint = f"/movie/{movie_id}/recommendations"
        params = {"page": page}
        return self._make_request(endpoint, params)

    def get_genre_list(self, media_type: str = "movie") -> Dict:
        """
        Get the list of official genres.
        
        Args:
            media_type (str): Type of media ("movie" or "tv")
            
        Returns:
            Dict: List of genres with their IDs
        
        Examples:
            >>> tmdb = TMDB("your_api_key")
            >>> genres = tmdb.get_genre_list("tv")
            >>> print(genres["genres"][0]["name"])
        """
        endpoint = f"/genre/{media_type}/list"
        return self._make_request(endpoint)
