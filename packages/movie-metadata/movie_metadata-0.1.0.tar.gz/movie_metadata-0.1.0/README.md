# Movie Metadata

A Python wrapper for The Movie Database (TMDB) API that provides easy access to movie, TV show, and person information.

## Installation

```bash
pip install movie-metadata
```

## Usage

```python
from movie_metadata import TMDB

# Initialize the client
tmdb = TMDB("your_api_key_here")

# Search for movies
results = tmdb.search_movies("The Matrix")

# Get movie details
movie_details = tmdb.get_movie_details(603)

# Get popular movies
popular_movies = tmdb.get_popular_movies()
```

## Features

- Search movies and TV shows
- Get detailed information about movies, TV shows, and people
- Discover movies based on various criteria
- Get movie recommendations
- Get cast and crew information
- Error handling and logging
- Type hints for better IDE support

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
