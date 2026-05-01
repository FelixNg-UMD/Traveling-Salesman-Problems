import numpy as np
import sys
import time
import os
import random

def read_adjacency_matrix(filename):
    try:
        adj_matrix = np.loadtxt(filename)
        return adj_matrix
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def calculate_total_distance(route, adj_matrix):
    total_distance = 0
    for i in range(len(route)-1):
        total_distance += adj_matrix[route[i]][route[i+1]]
    return total_distance

def nearest_neighbor(adj_matrix):
    route = []
    unvisited = list(range(len(adj_matrix)))

    #Start with 0
    current_node = 0
    route.append(current_node)
    unvisited.remove(current_node)

    while unvisited:
        for each_node in unvisited:
            closest_node = None
            closest_distance = float('inf')
            if adj_matrix[current_node][each_node] < closest_distance:
                closest_distance = adj_matrix[current_node][each_node]
                closest_node = each_node

        current_node = closest_node
        route.append(current_node)
        unvisited.remove(current_node)
    
    route.append(route[0])
    return route

def two_opt(adj_matrix):
    route = nearest_neighbor(adj_matrix)
    improved = True

    while improved:
        improved = False
        best_distance = calculate_total_distance(route, adj_matrix)

        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]

                new_distance = calculate_total_distance(new_route, adj_matrix)

                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    break  
            if improved:
                break

    return route

def two_opt_route(route, adj_matrix):
    improved = True


    while improved:
        improved = False
        best_distance = calculate_total_distance(route, adj_matrix)
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route) - 1):
                new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]

                new_distance = calculate_total_distance(new_route, adj_matrix)

                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True
                    break 
            if improved:
                break

    return route, best_distance


def RRNN (adj_matrix, k=3, n_repeat=5):
    best_route = None
    best_distance = float('inf')
    for _ in range(n_repeat):
        route = []
        unvisited = list(range(len(adj_matrix)))

        #Start with 0
        current_node = 0
        route.append(current_node)
        unvisited.remove(current_node)

        while unvisited:
            distances = []

            for each_node in unvisited:
                dist = adj_matrix[current_node][each_node]
                distances.append((dist,each_node))

            distances.sort()

            k_closest = [each_node for (_, each_node) in distances[:k]]
            next_random_node = random.choice(k_closest)
            route.append(next_random_node)
            unvisited.remove(next_random_node)
            current_node = next_random_node

        route.append(route[0])
        improved_route, improved_distance = two_opt_route(route, adj_matrix)


        if improved_distance < best_distance:
            best_distance = improved_distance
            best_route = improved_route
           
    return best_route , best_distance

def RRNN_another (adj_matrix, k=5, n_repeat=10):
    best_route = None
    best_distance = float('inf')
    for _ in range(n_repeat):
        route = []
        unvisited = list(range(len(adj_matrix)))

        #Start with 0
        current_node = 0
        route.append(current_node)
        unvisited.remove(current_node)

        while unvisited:
            distances = []

            for each_node in unvisited:
                dist = adj_matrix[current_node][each_node]
                distances.append((dist,each_node))

            distances.sort()

            k_closest = [each_node for (_, each_node) in distances[:k]]
            next_random_node = random.choice(k_closest)
            route.append(next_random_node)
            unvisited.remove(next_random_node)
            current_node = next_random_node

        route.append(route[0])
        improved_route, improved_distance = two_opt_route(route, adj_matrix)


        if improved_distance < best_distance:
            best_distance = improved_distance
            best_route = improved_route
           
    return best_route , best_distance

def list_matrix_files(folder_path):
    #List all matrix files in the folder
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return []
    
    matrix_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    return matrix_files

def measure_with_repeat(func, *args, **kwargs):
    attempts = 0
    total_runtime = 0.0
    total_cpu_time = 0.0
    result = None

    while True:
        start_time = time.time()
        start_cpu = time.process_time()
        
        result = func(*args, **kwargs)  
        
        end_time = time.time()
        end_cpu = time.process_time()
        
        runtime = end_time - start_time
        cpu_time = end_cpu - start_cpu

        attempts += 1
        total_runtime += runtime
        total_cpu_time += cpu_time

        if cpu_time > 0.0:
            break 

    return result, total_runtime / attempts, total_cpu_time / attempts

def main():
    # Check if matrix folder path is provided
    if len(sys.argv) != 2:
        print("Usage: python part1.py <matrix_folder_path>")
        print("Example: python part1.py mats_911")
        sys.exit(1)
    
    matrix_folder = sys.argv[1]
    
    # List all matrix files
    matrix_files = list_matrix_files(matrix_folder)
    
    if not matrix_files:
        print(f"No .txt files found in '{matrix_folder}'")
        sys.exit(1)
    
    print(f"Found {len(matrix_files)} matrix files in '{matrix_folder}':")
    for file in matrix_files:
        print(f"  {file}")
    
    # Let user input the full filename
    while True:
        filename = input("\nEnter the full filename you want to process (or 'q' to quit): ").strip()
        
        if filename.lower() == 'q':
            print("Goodbye!")
            sys.exit(0)
        
        # Check if file exists
        file_path = os.path.join(matrix_folder, filename)
        
        if not os.path.exists(file_path):
            print(f"Error: File '{filename}' not found in '{matrix_folder}'")
            print("Available files:")
            for file in matrix_files:
                print(f"  {file}")
            continue
        
        if not filename.endswith('.txt'):
            print("Error: Please enter a .txt file")
            continue
            
        break
    
    print(f"\nProcessing {filename}...")
    
    # Read the matrix
    adj_matrix = read_adjacency_matrix(file_path)
    if adj_matrix is None:
        sys.exit(1)
    
    n_cities = len(adj_matrix)
    print(f"Matrix size: {n_cities}x{n_cities}")
    

    print("\nRunning Nearest Neighbor algorithm...")
    route, runtime, cpu_time = measure_with_repeat(nearest_neighbor, adj_matrix)
    distance = calculate_total_distance(route, adj_matrix)

    print(f"RESULTS for {filename}:")
    print(f"Route: {route}")
    print(f"Total distance: {distance:.6f}")
    print(f"Runtime: {runtime:.6f} seconds")
    print(f"CPU Time: {cpu_time:.6f} seconds")
    

    print("\nRunning Nearest Neighbor 2-Opt algorithm...")
    two_opt_route_result, runtime, cpu_time = measure_with_repeat(two_opt, adj_matrix)
    distance = calculate_total_distance(two_opt_route_result, adj_matrix)

    print(f"RESULTS for {filename}:")
    print(f"Route: {two_opt_route_result}")
    print(f"Total distance: {distance:.6f}")
    print(f"Runtime: {runtime:.6f} seconds")
    print(f"CPU Time: {cpu_time:.6f} seconds")


    print("\nRunning RRNN algorithm...")
    (rrnn_result, distance), runtime, cpu_time = measure_with_repeat(RRNN, adj_matrix)
    route = rrnn_result

    print(f"RESULTS for {filename}:")
    print(f"Route: {route}")
    print(f"Total distance: {distance:.6f}")
    print(f"Runtime: {runtime:.6f} seconds")
    print(f"CPU Time: {cpu_time:.6f} seconds")


    print("\nRunning RRNN algorithm with larger k and num_repeats...")
    (rrnn_result, distance), runtime, cpu_time = measure_with_repeat(RRNN_another, adj_matrix)
    route = rrnn_result

    print(f"RESULTS for {filename}:")
    print(f"Route: {route}")
    print(f"Total distance: {distance:.6f}")
    print(f"Runtime: {runtime:.6f} seconds")
    print(f"CPU Time: {cpu_time:.6f} seconds")
if __name__ == "__main__":
    main()