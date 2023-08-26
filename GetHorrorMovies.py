from datetime import datetime
from tmdbv3api import TMDb
import csv
import time
import os
from tmdbv3api import Movie
from tmdbv3api import Genre
from tmdbv3api import Discover

# var assignations
tmdb = TMDb()
tmdb.api_key = '2646252fc48752036a6782c52ce74b94'
movie = Movie()
genre = Genre()
discover = Discover()
date = datetime.now().strftime("%Y%m%d-%H%M%S")

output_dir = r'C:\projects\tmdb_api\results'
os.makedirs(output_dir, exist_ok=True)
# Generate dynamic filename with date and time
current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_filename = os.path.join(output_dir, f'movies_{current_datetime}.xlsx')
    
i = 1
print("Starting value is {i}")
movies_collection = []

# 27 = HORROR
# 53 = THRILLLER

while True:

    if i < 500:
        
        print("Parsing movies page", int(i))
        
        movies_set = discover.discover_movies({
            'primary_release_date.gte': '2023-01-01',
            'primary_release_date.lte': '2023-12-31',
            'sort_by': 'popularity.desc',
            'with_genres': 27,
            'page': i
        })
        # horrormovies = horrormovies + movie
        movies_collection.extend(movies_set)
        i+=1
        
        # Break if all the movies have been been found (1639)
        if (len(movies_collection) == len(movies_collection) + len(movies_set)):
            print("Finished fetching horror movies")
            break
        
        print("Found horror movies - ", len(movies_collection))
    
    else:
        print("Break condition activated...")
        break

# Export horror movies to csv file
print(f"Exporting results to csv file {output_filename}")
for horror in movies_collection:
    # Export CSV file
    keys = movies_collection[0].keys()
    with open(output_filename, "w") as file:
        csvwriter = csv.DictWriter(file, keys)
        csvwriter.writeheader()
        csvwriter.writerows(movies_collection)


