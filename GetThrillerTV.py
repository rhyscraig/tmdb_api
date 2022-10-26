from datetime import datetime
from tmdbv3api import TMDb, TV
import csv
import time
from tmdbv3api import Movie
from tmdbv3api import Genre
from tmdbv3api import Discover

# var assignations
tmdb = TMDb()
tmdb.api_key = '2646252fc48752036a6782c52ce74b94'
show = Movie()
genre = Genre()
tv = TV()
discover = Discover()
date = datetime.now().strftime("%Y%m%d-%H%M%S")

# Prepare filename
filename = f'/root/projects/results/thriller-tv-shows-{date}.csv'
    
i = 1
print("Starting value is {i}")
tvshows = []

# "27-horror"
# 53 = THRILLLER

while True:

  if i < 500:
        
    print("Parsing movies page", int(i))
          
    show = discover.discover_tv_shows({
        "primary_release_year": "2015",
        "with_genres": "27-horror", 
        "vote_average.gte": "0", 
        "page": i
    })
    print(show)
    tvshows = tvshows + show
    i+=1
    
    # Break if all the movies have been been found (1639)
    if (len(tvshows) == len(tvshows + show)):
        print("Finished fetching TV shows")
        break
  
    print("Found TV shows", len(tvshows))

  else:
    print("Break condition activated...")
    break

# Export horror movies to csv file
print(f"Exporting {len(tvshows)} results to csv file {filename}")
for horror in tvshows:
    # Export CSV file
    keys = tvshows[0].keys()
    with open(filename, "w") as file:
        csvwriter = csv.DictWriter(file, keys)
        csvwriter.writeheader()
        csvwriter.writerows(tvshows)