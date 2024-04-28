from tmdbv3api import Discover, TMDb, Movie
import os
import csv
from datetime import datetime

tmdb = TMDb()
tmdb.api_key = '2646252fc48752036a6782c52ce74b94'

# Initialize the Discover class
discover = Discover()

# Get the current year
current_year = '2023'

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
csv_file_path = os.path.join(output_dir, f'movies_{current_datetime}-v6.csv')

# Write horror movies to a CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header row using available attributes from the first movie
    # first_movie = discover.discover_movies(params=horror_movie_params)[0]
    # header = [attr for attr in dir(first_movie) if not callable(getattr(first_movie, attr)) and not attr.startswith("__")]
    # csv_writer.writerow(header)


    # Write the header row
    csv_writer.writerow(['Title', 'Overview', 'Poster Path', 'Release Date', 'Popularity', 'Vote Average', 'Original Language', 'Vote Count'])

    
    # Initialize pagination variables
    max_pages = 500
    page = 1
    
    while page <= max_pages:

        horror_movies = discover.discover_movies(params=horror_movie_params)
        if not horror_movies:
            break     
            

    for movie in horror_movies:

        # Discover horror movies based on the parameters and page number
        detailed_movie = Movie()
        detailed_movie_info = detailed_movie.details(movie.id)
        
        # Convert string values to integers
        vote_average = int(detailed_movie_info.vote_average) if detailed_movie_info.vote_average else 0
        vote_count = int(detailed_movie_info.vote_count) if detailed_movie_info.vote_count else 0
        
        # Calculate vote_score and alg1
        vote_score = vote_average * vote_count
        alg1 = vote_score * detailed_movie_info.popularity

        csv_writer.writerow([
            movie.title, 
            movie.overview,
            movie.poster_path,
            movie.release_date, 
            movie.popularity, 
            movie.vote_average, 
            movie.original_language,
            movie.vote_count
        ])
        

        # Break the loop if no more movies are available
        if not horror_movies:
            break

        # Move to the next page
        page += 1

print(f"Horror movies have been written to {csv_file_path}-v5")
