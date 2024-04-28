import boto3
import json
import logging
from datetime import datetime
from tmdbv3api import TMDb, TV, Discover

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TMDb API key
TMDB_API_KEY = '2646252fc48752036a6782c52ce74b94'

# Genre dictionary for TV shows
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

# Function to fetch TV shows from TMDb
def fetch_tv_shows(genre_id, period, min_vote_count, max_pages):
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    discover = Discover()
    
    tv_params = {
        'sort_by': 'vote_count.desc',
        'with_genres': str(genre_id),
        'first_air_date_year': period
    }
    
    tv_data = []
    page = 1
    while page <= max_pages:
        tv_params['page'] = page
        response = discover.discover_tv_shows(params=tv_params)
        tv_shows = response['results']
        
        if not tv_shows:
            break
        
        for tv in tv_shows:
            if tv['vote_count'] >= min_vote_count:
                vote_score = tv['vote_average'] * tv['vote_count']
                alg1 = vote_score * tv['popularity']
                tv_data.append({
                    'Title': tv['name'],
                    'Overview': tv['overview'],
                    'Poster Path': tv['poster_path'],
                    'First Air Date': tv['first_air_date'],
                    'Popularity': tv['popularity'],
                    'Vote Average': tv['vote_average'],
                    'Original Language': tv['original_language'],
                    'Vote Count': tv['vote_count'],
                    'Vote Score': vote_score,
                    'Algorithm Score': alg1
                })
            else:
                # Stop API call once the minimum vote count threshold is reached
                return tv_data
        
        page += 1
    
    return tv_data

# Lambda handler
def lambda_handler(event, context):
    # Parse input event
    genre_id = event['genre_id']
    period = event['period']
    min_vote_count = event.get('min_vote_count', 10)
    max_pages = event.get('max_pages', 500)
    
    # Determine the period based on the input
    if period == 'current_year':
        period = str(datetime.now().year)
    elif period == 'last_year':
        period = str(datetime.now().year - 1)
    elif not period.isdigit():
        raise ValueError("Invalid period value")
    
    # Fetch TV shows data
    tv_data = fetch_tv_shows(genre_id, period, min_vote_count, max_pages)

    # Specify the S3 bucket name and key
    bucket_name = event.get('bucket_name', 'horror.craighoad.com')
    genre_name = tv_genre_dict.get(genre_id, 'unknown_genre')
    bucket_key = f'tv/{genre_name.lower()}/{period}/{genre_name.lower()}_tv_{period}.json'

    # Upload the JSON data to S3
    s3 = boto3.client('s3')
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=bucket_key,
            Body=json.dumps(tv_data, indent=4),
            ContentType='application/json'
        )
        logger.info(f"Filtered {genre_name} TV shows for {period} have been uploaded to S3 bucket {bucket_name} with key {bucket_key}")
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")

    return {
        'statusCode': 200,
        'body': 'JSON file uploaded to S3'
    }
