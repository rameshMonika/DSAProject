import heapq
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('airports.csv', header=None)

# Convert the DataFrame to a list of lists
dataset = df.values.tolist()

# Constructing the graph
graph = {}
for airport in dataset:
    graph[airport[3]] = {  # Use the city name as the key
        'coordinates': (airport[4], airport[5]),
        'connections': {}
    }

# Implementing A* algorithm


def heuristic(coordinates1, coordinates2):
    # A simple Euclidean distance as heuristic
    return ((coordinates1[0] - coordinates2[0]) ** 2 + (coordinates1[1] - coordinates2[1]) ** 2) ** 0.5


def astar(graph, start, goal):
    priority_queue = [(0, start, [start])]
    visited = set()

    while priority_queue:
        current_cost, current_node, current_path = heapq.heappop(
            priority_queue)

        if current_node == goal:
            return current_cost, current_path

        if current_node not in visited:
            visited.add(current_node)

            for neighbor, cost in graph[current_node]['connections'].items():
                if neighbor not in visited:
                    total_cost = current_cost + cost + \
                        heuristic(graph[neighbor]['coordinates'],
                                  graph[goal]['coordinates'])
                    heapq.heappush(priority_queue, (total_cost,
                                   neighbor, current_path + [neighbor]))

    return float('inf'), []


# Manually define connections based on geographic proximity
# Note: You may want to use a more sophisticated method to determine connections in a real-world scenario
for i in range(len(dataset)):
    for j in range(i + 1, len(dataset)):
        city1, city2 = dataset[i][3], dataset[j][3]
        distance = heuristic(
            graph[city1]['coordinates'], graph[city2]['coordinates'])
        graph[city1]['connections'][city2] = distance
        graph[city2]['connections'][city1] = distance

# User input
start_city = input("\nEnter the starting city: ")
goal_city = input("Enter the destination city: ")

# Validate input cities
invalid_cities = [city for city in [
    start_city, goal_city] if city not in graph]
if invalid_cities:
    print(
        f"Invalid city names: {', '.join(invalid_cities)}. Please enter valid city names.")
else:
    shortest_distance, shortest_route = astar(graph, start_city, goal_city)

    if shortest_distance == float('inf'):
        print(f"No route found between {start_city} and {goal_city}.")
    else:
        # Convert distance to kilometers
        # Assuming 1 degree of latitude is approximately 111 km
        shortest_distance_km = shortest_distance * 111

        print(
            f"\nShortest Distance from {start_city} to {goal_city} : {round(shortest_distance_km, 5)} km")
