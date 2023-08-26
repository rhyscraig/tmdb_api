from tmdbv3api import Discover
from tmdbv3api import TMDb
import os
import csv
from datetime import datetime

# Set your TMDB API key here
tmdb = TMDb()
tmdb.api_key = 'YOUR_API_KEY_HERE'

# Initialize the Discover class
discover = Discover()

# Get the current year
current_year = str(datetime.now().year)

# Define parameters for discovering horror movies of this year
horror_movie_params = {
    'sort_by': 'popularity.desc',
    'with_genres': '27',  # Horror genre ID
    'primary_release_year': current_year
}

# Specify the CSV file path
output_dir = r'C:\projects\tmdb_api\results'
os.makedirs(output_dir, exist_ok=True)
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
csv_file_path = os.path.join(output_dir, f'movies_{current_datetime}-v3.csv')

# Write horror movies to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header row
    csv_writer.writerow(['Title', 'Overview', 'Poster Path', 'Release Date', 'Popularity', 'Vote Average', 'Original Language', 'Vote Count', 'Vote Score', 'Algorithm Score'])
    
    page = 1
    while True:
        # Discover horror movies based on the parameters
        horror_movies = discover.discover_movies(params=horror_movie_params, page=page)
        
        if not horror_movies:
            break
        
        # Write movie data to the CSV file
        for movie in horror_movies:
            vote_score = movie.vote_average * movie.vote_count
            alg1 = vote_score * movie.popularity
            csv_writer.writerow([
                movie.title, 
                movie.overview,
                movie.poster_path,
                movie.release_date, 
                movie.popularity, 
                movie.vote_average, 
                movie.original_language,
                movie.vote_count,
                vote_score,
                alg1
            ])
        
        page += 1

print(f"Horror movies have been written to {csv_file_path}")
