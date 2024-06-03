from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import heapq
from datetime import datetime

def get_fasted_path_with_pedestrian(data, source, destination, datetime_obj):
    # Debug: Print initial parameters
    datetime_obj = datetime.strptime(datetime_obj, '%Y-%m-%d %H:%M:%S')
  
    df = data.copy()
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

    # Drop rows with NaT in 'Date' column (if any)
    df = df.dropna(subset=['Date'])

    # Add a new column for the day of the week
    df['Day_of_Week'] = df['Date'].dt.day_name()

    # Ensure there are no gaps in the data
    df['Date_Diff'] = df['Date'].diff()
    min_gap = pd.Timedelta(days=2)
    gaps = df[df['Date_Diff'] >= min_gap]
    df = df.drop(columns=['Date_Diff'])

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    Pedestrian_data = df[(df['Type'] == 'Pedestrian')]
    car_data = df[(df['Type'] == 'Car')]

    # Define features (X) and target variable (y)
    X = Pedestrian_data[['Start', 'End', 'Day_of_Week']]
    y = Pedestrian_data['Travel time']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), ['Start', 'End', 'Day_of_Week'])
        ],
        remainder='passthrough'
    )

    # Append the linear regression model to the preprocessing pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Fit the model
    model.fit(X_train, y_train)

    # Make predictions 
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)



    class Graph:
        def __init__(self):
            self.adjacency_list = {}

        def add_edge(self, start, end, travel_time):
            if start not in self.adjacency_list:
                self.adjacency_list[start] = []
            self.adjacency_list[start].append((end, travel_time))

        def add_node(self, node):
            if node not in self.adjacency_list:
                self.adjacency_list[node] = []

        def dijkstra(self, start, end, start_time):
            distances = {node: float('inf') for node in self.adjacency_list}
            distances[start] = 0
            priority_queue = [(0, start, start_time)]
            previous_node = {node: None for node in self.adjacency_list}

            while priority_queue:
                current_distance, current_node, current_time = heapq.heappop(priority_queue)

                if current_node == end:
                    path = self.reconstruct_path(previous_node, start, end)
                    return distances[end], path

                if current_distance > distances[current_node]:
                    continue

                for neighbor, travel_time in self.adjacency_list[current_node]:
                    adjusted_travel_time = self.get_adjusted_travel_time(current_time, travel_time)

                    if current_distance + adjusted_travel_time < distances[neighbor]:
                        distances[neighbor] = current_distance + adjusted_travel_time
                        previous_node[neighbor] = current_node
                        heapq.heappush(priority_queue, (distances[neighbor], neighbor, current_time + timedelta(seconds=adjusted_travel_time)))

            return float('inf'), None

        def get_adjusted_travel_time(self, current_time, travel_time):
            day_of_week = current_time.strftime("%A")
            if day_of_week == "Tuesday" and current_time.hour == 14:
                return travel_time - 20
            else:
                return travel_time

        def reconstruct_path(self, previous_node, start, end):
            path = []
            current_node = end
            while current_node != start:
                path.append(current_node)
                current_node = previous_node[current_node]
            path.append(start)
            path.reverse()
            return path

    graph = Graph()

    # Add nodes
    for index, row in df.iterrows():
        graph.add_node(row['Start'])
        graph.add_node(row['End'])

    # Add edges
    for index, row in df.iterrows():
        graph.add_edge(row['Start'], row['End'], row['Travel time'])

    # shortest_time, route = graph.dijkstra(source, destination, datetime_obj)
    shortest_time, route = graph.dijkstra(source, destination, datetime_obj)

    
    # Debug: print the route and time
    print(f"Shortest route time from {source} to {destination} starting at {datetime_obj}: {shortest_time} seconds")
    print("Route:", route)
    
    return route

# data = pd.read_csv('data_clean.csv')
# source = 'Gadolinium'
# destination = 'Promethium'
# dateandtime = '2024-06-01 20:00:00'

# print(get_fasted_path_with_car(data, source, destination, dateandtime))