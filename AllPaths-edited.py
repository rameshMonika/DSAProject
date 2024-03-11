import pandas as pd
from geopy.distance import geodesic

# Read the data from the file
airports_cols =['Index','Airport Name', 'Country', 'IATA', 'Latitude', 'Longitude', 'Altitude', 'DST']
routes_cols = ['Source airport', 'Destination airport', 'Stops']
airports = pd.read_csv('airports.csv', names=airports_cols, header=None, index_col=None, na_values='\\N')
routes = pd.read_csv('routes-edited.csv', names=routes_cols, header=None, index_col=None, na_values='\\N')
source_airports = airports[['IATA', 'Latitude', 'Longitude']].rename(columns={'IATA': 'Source airport'})
destination_airports = airports[['IATA', 'Latitude', 'Longitude']].rename(columns={'IATA': 'Destination airport'})

routes_with_source = pd.merge(routes, source_airports, on='Source airport', how='left')

routes_with_coordinates = pd.merge(routes_with_source, destination_airports, on='Destination airport', how='left')

# The dataset somehow have null values for the coordinates for some airports.
# This part is to remove them so that the distance can be calculated.
# Remove entries with null values for coordinates
routes_with_coordinates = routes_with_coordinates.dropna(subset=['Latitude_x', 'Longitude_x', 'Latitude_y', 'Longitude_y'])

#This part is to check if there are still null values in the dataset not needed in the actual code
null_inf_index = routes_with_coordinates[['Latitude_x', 'Longitude_x', 'Latitude_y', 'Longitude_y']].isnull().values.any() 

# Calculate the distance between the source and destination airports in km
def calculate_distance(row):
    source = (row['Latitude_x'], row['Longitude_x'])
    dest = (row['Latitude_y'], row['Longitude_y'])
    return geodesic(source, dest).kilometers

# Apply the function to the routes_with_coordinates dataset
# This part takes quite awhile to run
routes_with_coordinates['Distance'] = routes_with_coordinates.apply(calculate_distance, axis=1)
print(routes_with_coordinates[['Source airport', 'Destination airport', 'Distance']])
routes_with_coordinates[['Source airport', 'Latitude_x', 'Longitude_x', 'Destination airport', 'Latitude_y', 'Longitude_y', 'Distance']].to_csv('routes_with_distance.csv', index=False)
