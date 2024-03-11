import heapq

# Sample dataset (part of it)
dataset = [
    [40, "Thunder Bay International Airport", "Thunder Bay", "Canada", "YQT", "CYQT",
        48.37189865112305, -89.32389831542969, 653, -5, "A", "America/Toronto", "airport", "OurAirports"],
    [41, "Regina International Airport", "Regina", "Canada", "YQR", "CYQR", 50.43190002441406, -
        104.66699981689453, 1894, -6, "A", "America/Regina", "airport", "OurAirports"],
    [42, "Saskatoon John G. Diefenbaker International Airport", "Saskatoon", "Canada", "YXE", "CYXE",
        52.170799255371094, -106.69999694824219, 1653, -6, "A", "America/Regina", "airport", "OurAirports"],
    [43, "St. John's International Airport", "St. John's", "Canada", "YYT", "CYYT",
        47.618598938, -52.7518997192, 461, -3.5, "A", "America/St_Johns", "airport", "OurAirports"],
    [44, "Kelowna International Airport", "Kelowna", "Canada", "YLW", "CYLW", 49.9561004639, -
        119.377998352, 1409, -8, "A", "America/Vancouver", "airport", "OurAirports"],
    [45, "Fort McMurray International Airport", "Fort Mcmurray", "Canada", "YMM", "CYMM",
        56.653301239, -111.221000671, 1211, -7, "A", "America/Edmonton", "airport", "OurAirports"],
    [46, "Kelowna International Airport", "Kelowna", "Canada", "YLW", "CYLW", 49.9561004639, -
        119.377998352, 1409, -8, "A", "America/Vancouver", "airport", "OurAirports"],
    [47, "Yellowknife Airport", "Yellowknife", "Canada", "YZF", "CYZF", 62.462799072265625, -
        114.44000244140625, 675, -7, "A", "America/Edmonton", "airport", "OurAirports"],
    [48, "Halifax / CFB Shearwater Heliport", "Halifax", "Canada", " ", "CYAW",
        44.639702, -63.499401, 144, -4, "A", "America/Halifax", "airport", "OurAirports"],
    [49, "St. Anthony Airport", "St. Anthony", "Canada", "YAY", "CYAY", 51.3918991089, -
        56.083099365200006, 108, -3.5, "A", "America/St_Johns", "airport", "OurAirports"],
    [50, "Tofino / Long Beach Airport", "Tofino", "Canada", "YAZ", "CYAZ", 49.079833, -
        125.775583, 80, -8, "A", "America/Vancouver", "airport", "OurAirports"],
    [51, "Kugaaruk Airport", "Pelly Bay", "Canada", "YBB", "CYBB", 68.534401, -
        89.808098, 56, -7, "A", "America/Edmonton", "airport", "OurAirports"],
    [52, "Toronto Pearson International Airport", "Toronto", "Canada", "YYZ", "CYYZ",
        43.6772003174, -79.63059997559999, 569, -5, "A", "America/Toronto", "airport", "OurAirports"],
    [53, "Vancouver International Airport", "Vancouver", "Canada", "YVR", "CYVR",
        49.193901062, -123.179000854, 14, -8, "A", "America/Vancouver", "airport", "OurAirports"]
]

# Displaying the list of cities
city_country_list = [f"{airport[4]}, {airport[3]}" for airport in dataset]
print("List of Cities:")
for i, city_country in enumerate(city_country_list, 1):
    print(f"[{i}] {city_country}")

# Constructing the graph
graph = {}
for airport in dataset:
    graph[airport[4]] = {  # Use the city name as the key
        'coordinates': (airport[6], airport[7]),
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
        city1, city2 = dataset[i][4], dataset[j][4]
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
