class TMDBException(Exception):
    """Base exception for TMDB API errors."""
    pass

class TMDBAPIError(TMDBException):
    """Raised when the TMDB API returns an error."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"TMDB API Error ({status_code}): {message}")