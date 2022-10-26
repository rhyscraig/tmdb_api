from datetime import datetime
from tmdbv3api import TMDb
import csv
import time
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

# Prepare filename
filename = f'/root/projects/results/horror-movies-{date}.csv'
    
i = 1
print("Starting value is {i}")
horrormovies = []

# 27 = HORROR
# 53 = THRILLLER

while True:

    if i < 500:
        
        print("Parsing movies page", int(i))
        
        movie = discover.discover_movies({
            'primary_release_date.gte': '2022-01-01',
            'primary_release_date.lte': '2022-12-31',
            'sort_by': 'popularity.desc',
            'with_genres': 27,
            'page': i
        })
        horrormovies = horrormovies + movie
        i+=1
        
        # Break if all the movies have been been found (1639)
        if (len(horrormovies) == len(horrormovies + movie)):
            print("Finished fetching horror movies")
            break
        
        print("Found horror movies - ", len(horrormovies))
    
    else:
        print("Break condition activated...")
        break
# Export horror movies to csv file
print(f"Exporting results to csv file {filename}")
for horror in horrormovies:
    # Export CSV file
    keys = horrormovies[0].keys()
    with open(filename, "w") as file:
        csvwriter = csv.DictWriter(file, keys)
        csvwriter.writeheader()
        csvwriter.writerows(horrormovies)


