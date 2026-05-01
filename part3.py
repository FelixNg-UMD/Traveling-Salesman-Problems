import numpy as np
import sys
import time
import os
import random
import math

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

def hill_climbing (adj_matrix, num_restarts):   
    n = len(adj_matrix)

    current_route = [0] + random.sample(range(1, n), n - 1) + [0]
    current_dist = calculate_total_distance(current_route, adj_matrix)


    for iter in range(num_restarts):

        i, j = random.sample(range(1, n), 2)
        random_route = current_route[:]
        random_route[i], random_route[j] = random_route[j], random_route[i]

        random_route_dist = calculate_total_distance(random_route, adj_matrix)


        if random_route_dist < current_dist:
            current_route = random_route 
            current_dist = random_route_dist 


    return current_route, current_dist

def simulated_annealing (adj_matrix, alpha, initial_temperature, max_iterations):
    n = len(adj_matrix)
    current_route = [0] + random.sample(range(1, n), n - 1) + [0]   
    current_dist = calculate_total_distance(current_route, adj_matrix)

    temp = initial_temperature
    for iter in range(max_iterations):

        i, j = random.sample(range(1, n), 2)
        new_route = current_route[:]
        new_route[i], new_route[j] = new_route[j], new_route[i]

        new_route_dist = calculate_total_distance(new_route, adj_matrix)

        if new_route_dist < current_dist:
            current_route = new_route 
            current_dist = new_route_dist
        else:
            delta = current_dist - new_route_dist
            if random.random() < math.exp(delta/temp):
                current_dist = new_route_dist
                current_route = new_route
        
        temp *= alpha

    return current_route, current_dist


def order_crossover (parent1, parent2):
    n = len(parent1)

    i, j = sorted(random.sample(range(1,n), 2))

    child = [-1] * n

    child[i:j] = parent1[i:j]

    remaining = [city for city in parent2 if city not in child]
    
    pos = 1
    for city in remaining:
        while pos < n - 1 and child[pos] != -1:  
            pos += 1
        if pos >= n - 1: 
            break
        child[pos] = city
        pos += 1 
    
    child[0] = 0
    child[n-1] = 0

    return child


def mutate(route):
    i, j = random.sample(range(1, len(route)-1), 2)
    route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm (adj_matrix, mutation_chance, population_size, num_generations):
    n = len(adj_matrix) 

    total_population = [[0] + random.sample(range(1, n), n-1) + [0] for _ in range(population_size)]

    best_dist = float('inf')
    best_route = None

    new_population = [] 
    for gen in range(num_generations):
    
        parent1 = random.choice(total_population) 
        parent2 = random.choice(total_population) 
        child = order_crossover(parent1, parent2)
            
        if random.random() < mutation_chance:
                child = mutate(child)
        
        child_dist = calculate_total_distance(child, adj_matrix)
        if child_dist < best_dist:
            best_dist = child_dist
            best_route = child

        new_population.append(child)
    
    final = total_population + new_population 
        
    scored = [(calculate_total_distance(route, adj_matrix), route) for route in final]
    scored.sort(key=lambda x: x[0])
    total_population = [route for dist, route in scored[:population_size]]

    if scored[0][0] < best_dist:
        best_dist = scored[0][0]
        best_route = scored[0][1]

    return best_dist, best_route

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
    
    print("\nChoose algorithm:")
    print("1. Hill Climbing")
    print("2. Simulated Annealing")
    print("3. Genetic Algorithm")
    choice = input("Enter choice (1/2/3): ").strip()


    if choice == "1":
        num_restarts = int(input("Enter number of restarts: "))
        (result, runtime, cpu_time) = measure_with_repeat(hill_climbing, adj_matrix, num_restarts)
        route, distance = result

    elif choice == "2":
        alpha = float(input("Enter alpha: "))
        temp = float(input("Enter initial temperature: "))
        max_iter = int(input("Enter max iterations: "))
        (result, runtime, cpu_time) = measure_with_repeat(simulated_annealing, adj_matrix, alpha, temp, max_iter)
        route, distance = result

    elif choice == "3":
        mutation = float(input("Enter mutation chance (0-1): "))
        population = int(input("Enter population size: "))
        generations = int(input("Enter number of generations: "))
        (result, runtime, cpu_time) = measure_with_repeat(genetic_algorithm, adj_matrix, mutation, population, generations)
        distance, route = result

    else:
        print("Invalid choice.")
        sys.exit(1)

    print(f"\nRESULTS for {filename}:")
    print(f"Route: {route}")
    print(f"Total distance: {distance:.6f}")
    print(f"Runtime: {runtime:.6f} seconds")
    print(f"CPU Time: {cpu_time:.6f} seconds")
if __name__ == "__main__":
    main()