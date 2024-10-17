import requests
import json
import logging

logging.basicConfig(
    filename='restaurantlogs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Function to get restaurant data from Google Places API
def get_restaurants(city_name, api_key):
    logging.info("Initiating the retrieval of restaurant information from the Google Places API using the city name : %s",{city_name});
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={api_key}"
    geocode_response = requests.get(geocode_url)
    logging.info("Received the Gecode response : %s from the Google Places API for the provided city name : %s",{city_name},{geocode_response})
    logging.info("Checking the status of the response received from the Google Places API.")
    if geocode_response.status_code == 200:
        geocode_data = geocode_response.json()

        if geocode_data['status'] == "OK":
            # Get city coordinates
            location = geocode_data['results'][0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            logging.info("Started to filter for the top restaurants in the city based on the received Geocode Data.")
            # Now, search for top restaurants in this city
            places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"

            params = {
                "location": f"{lat},{lng}",
                "radius": 10000,
                "type": "restaurant",
                "key": api_key,
                "rankby": "prominence"
            }
            logging.info("Initiating the retrieval of restaurant information from the Google Places API By creating a request Object which containes the lat : %s, lag : %s and by considering radius of 10KM :",{lat},{lng});
            # Make request to Places API
            places_response = requests.get(places_url, params=params)
            logging.info("Checking the status of the response received from the Google Places API .")
            if places_response.status_code == 200:
                logging.info("Recived a Success Status Code : %s Returning a Restaurant to the Caller Response: %s",{places_response.status_code},{places_response})
                return places_response.json()
            else:
                logging.error("Error in Places API request: %s",{places_response.status_code})
                print(f"Error in Places API request: {places_response.status_code}")
                return None
        else:
            logging.error("Error in Geocoding: %s", {geocode_data['status']})
            print(f"Error in Geocoding: {geocode_data['status']}")
            return None
    else:
        logging.error("Error in Geocoding request: %s", {geocode_response.status_code})
        print(f"Error in Geocoding request: {geocode_response.status_code}")
        return None


# Function to process the restaurant data and save to a JSON file
def save_restaurant_data(restaurants, city_name):
    restaurant_info = {}
    logging.info("Initiating the Process of adding restaurant information To a JSON File in Key as Restaurant Name ANd Value as Rating,Total Reviews and Address  : %s",restaurants);
    if 'results' in restaurants:
        for restaurant in restaurants['results']:
            name = restaurant.get('name', 'N/A')
            rating = restaurant.get('rating', 'N/A')
            user_ratings_total = restaurant.get('user_ratings_total', 'N/A')
            address = restaurant.get('vicinity', 'N/A')

            # Create a dictionary of restaurant details
            restaurant_info[name] = {
                "Rating": rating,
                "Total Reviews": user_ratings_total,
                "Address": address
            }

        # Save the data to a JSON file
        filename = f"{city_name}_top_restaurants.json"
        with open(filename, 'w') as json_file:
            json.dump(restaurant_info, json_file, indent=4)
        logging.info("Data saved to %s",{filename})
        print(f"Data saved to {filename}")
    else:
        logging.error("No restaurants found.")
        print("No restaurants found.")


# Main function to prompt user input and execute the search
def main():
    logging.info("Reading the City Name From the User")
    city_name = input("Enter the name of the city: ")
    logging.info("City Name Enter by User : %s",{city_name})
    api_key = "AIzaSyBZhBukvZPYaoIYe4hyvscI1miWASBfK7k"  # Replace with your Google API key


    # Fetch top restaurants using Google Places API
    restaurants = get_restaurants(city_name, api_key)

    if restaurants:
        save_restaurant_data(restaurants, city_name)


if __name__ == "__main__":
    main()
