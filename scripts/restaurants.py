
# coding: utf-8

import pandas as pd
from yelpapi import *

from data import config

#get client_id and client_secret from your Yelp app
client_id = config.client_id
client_secret = config.client_secret

#4 limits: 
#left: 38.904272, -77.499988
#down: 38.689836, -77.040657
#right: 38.905468, -76.905657
#up: 39.111392, -77.040263


# In[ ]:


def find_1000(yelp_api, latitude, longitude):
    ###return the up to 1000 restaurants in a list 
    total_search_results = list()
    for i in range(20):
        temp_result = yelp_api.search_query(latitude = latitude,
                                        longitude = longitude,
                                        term = "restaurants",
                                        limit = 50, 
                                        offset = 50 * i,
                                        radius = 8000)
        total_search_results.extend(temp_result["businesses"])
    return total_search_results

##get the coordinates of the centers based on which we do the business search

#define limits of the square
left = -77.499988
right = -76.905657
up = 39.111392
down = 38.689836
longitude_list = [left + (right - left)/8 * i for i in range(8)]
latitude_list = [down + (up - down)/8 * i for i in range(8)]
coordinate_list = [(longitude_list[i], latitude_list[j]) for i in range(len(longitude_list)) 
                   for j in range(len(latitude_list))]


#pull all restaurants based on every coordinates we defined.
yelp_api = YelpAPI(client_id=client_id, client_secret=client_secret)
restaurant_list = list()
for coordinate in coordinate_list:
    restaurant_list_temp = find_1000(yelp_api, latitude = coordinate[1], longitude = coordinate[0])
    restaurant_list.extend(restaurant_list_temp)



clean_restaurant_list = map(lambda restaurant: [
                        restaurant["id"],
                        restaurant["name"],
                        restaurant.get("price",""),
                        restaurant["rating"],
                        restaurant["review_count"],
                        restaurant["coordinates"]["longitude"], 
                        restaurant["coordinates"]["latitude"]],
                        restaurant_list)
restaurant_df = pd.DataFrame(clean_restaurant_list, 
                             columns=["id","name", "price", "rating", "review_count", "longitude", "latitude"])
unique_restaurants = restaurant_df.drop_duplicates()
unique_restaurants.to_csv("/Users/lawrence/PycharmProjects/yelp/data/restaurants.csv", 
                          sep="|", 
                          encoding="utf-8",
                         index=False)



