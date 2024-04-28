import boto3
from datetime import datetime
from tmdbv3api import TMDb, Movie, Discover
import json
import os
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create timestamp
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Current year
current_year = datetime.now().year

# Last year (subtract 1 year from the current year)
last_year = datetime.now().year - 1

# Convert integers to strings if needed (optional, based on how you want to use these variables)
current_year_str = str(current_year)
last_year_str = str(last_year)


# Genre dictionary for movies and TV shows
movie_genre_dict = {
    28: 'Action',
    12: 'Adventure',
    16: 'Animation',
    35: 'Comedy',
    80: 'Crime',
    99: 'Documentary',
    18: 'Drama',
    10751: 'Family',
    14: 'Fantasy',
    36: 'History',
    27: 'Horror',
    10402: 'Music',
    9648: 'Mystery',
    10749: 'Romance',
    878: 'Science Fiction',
    10770: 'TV Movie',
    53: 'Thriller',
    10752: 'War',
    37: 'Western'
}

tv_genre_dict = {
    10759: 'Action & Adventure',
    16: 'Animation',
    35: 'Comedy',
    80: 'Crime',
    99: 'Documentary',
    18: 'Drama',
    10751: 'Family',
    10762: 'Kids',
    9648: 'Mystery',
    10763: 'News',
    10764: 'Reality',
    10765: 'Sci-Fi & Fantasy',
    10766: 'Soap',
    10767: 'Talk',
    10768: 'War & Politics',
    37: 'Western'
}

def lambda_handler(event, context):
    # Parse input event
    genre_id = event['genre_id']
    period = event['period']

    # TMDb API setup
    tmdb = TMDb()
    tmdb.api_key = '2646252fc48752036a6782c52ce74b94'
    discover = Discover()

    # Define parameters for discovering movies
    movie_params = {
        'sort_by': 'popularity.desc',
        'with_genres': str(genre_id),
        'primary_release_year': period
    }

    # Fetch movies data
    movies_data = []
    max_pages = 500
    page = 1
    while page <= max_pages:
        movie_params['page'] = page
        response = discover.discover_movies(params=movie_params)
        movies = response['results']
        
        if not movies:
            break
        
        for movie in movies:
            # Filter movies based on vote count
            if movie['vote_count'] >= 10:
                vote_score = movie['vote_average'] * movie['vote_count']
                alg1 = vote_score * movie['popularity']
                movies_data.append({
                    'Title': movie['title'],
                    'Overview': movie['overview'],
                    'Poster Path': movie['poster_path'],
                    'Release Date': movie['release_date'],
                    'Popularity': movie['popularity'],
                    'Vote Average': movie['vote_average'],
                    'Original Language': movie['original_language'],
                    'Vote Count': movie['vote_count'],
                    'Vote Score': vote_score,
                    'Algorithm Score': alg1
                })
        
        page += 1

    # Specify the S3 bucket name and key
    bucket_name = 'horror.craighoad.com'
    genre_name = movie_genre_dict.get(genre_id, 'unknown_genre')
    bucket_key = f'{genre_name.lower()}/{genre_name.lower()}_movies_{period}.json'

    # Upload the JSON data to S3
    s3 = boto3.client('s3')
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=bucket_key,
            Body=json.dumps(movies_data, indent=4),
            ContentType='application/json'
        )
        logging.info(f"Filtered {genre_name} movies for {period} have been uploaded to S3 bucket {bucket_name} with key {bucket_key}")
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")

    return {
        'statusCode': 200,
        'body': 'JSON file uploaded to S3'
    }
