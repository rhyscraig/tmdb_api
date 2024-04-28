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
filename = f'/root/projects/results/horror-tv-shows-{date}.csv'
    
i = 1
print("Starting value is {i}")
horrorshows = []

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
    horrorshows = horrorshows + show
    i+=1
    
    # Break if all the movies have been been found (1639)
    if (len(horrorshows) == len(horrorshows + show)):
        print("Finished fetching horror movies")
        break
  
    print("Found horror movies - ", len(horrorshows))

  else:
    print("Break condition activated...")
    break

# Export horror movies to csv file
print(f"Exporting {len(horrorshows)} results to csv file {filename}")
for horror in horrorshows:
    # Export CSV file
    keys = horrorshows[0].keys()
    with open(filename, "w") as file:
        csvwriter = csv.DictWriter(file, keys)
        csvwriter.writeheader()
        csvwriter.writerows(horrorshows)