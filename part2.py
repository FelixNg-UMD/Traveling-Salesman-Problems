import numpy as np
import sys
import time
import os
import random
from scipy.sparse.csgraph import minimum_spanning_tree
from queue import PriorityQueue

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

 
def mst(adj_matrix, visited):
    n = len(adj_matrix)
    unvisited = [node for node in range(n) if node not in visited]

    if not unvisited:
        return 0
    
    unvisited = np.array(unvisited)
    subgraph = adj_matrix[unvisited[:, None], unvisited]

    mst = minimum_spanning_tree(subgraph).toarray()

    total = mst.sum()

    return total

def astart(adj_matrix):
    n = len(adj_matrix)
    start_node = 0

    route = [start_node]
    visited = {start_node}
    g = 0
    h = mst(adj_matrix, visited)
    f = g + h

    pq = PriorityQueue()
    pq.put((f, g, route, visited))

    best_route = None
    best_cost = float("inf")
    nodes_expanded = 0
    #step = 0  # Step for tracing 

    while not pq.empty():
        f, g, route, visited = pq.get()
        nodes_expanded += 1
        # For tracing
        #step += 1
        #print(f"\nStep {step}:")
        #print(f"  Popped from PQ -> f: {f}, g: {g}, route: {route}, visited: {visited}")

        if f >= best_cost:
           # print(f"  Skipped (f={f} >= best_cost={best_cost})")
            continue

        if len(visited) == n:
            final_route = route + [start_node]
            final_dist = calculate_total_distance(final_route, adj_matrix)
            
            if final_dist < best_cost:
                best_cost = final_dist
                best_route = final_route
            continue
        
        for each_node in range(n):
            if each_node not in visited:
                new_route = route + [each_node]
                new_visited = visited | {each_node}
                new_g = calculate_total_distance(new_route, adj_matrix)
                new_h = mst(adj_matrix, new_visited)
                new_f = new_g + new_h
                pq.put((new_f, new_g, new_route, new_visited))
                #For tracing
                #  print(f"    Added to PQ -> f: {new_f}, g: {new_g}, route: {new_route}, visited: {new_visited}")

    return best_route, best_cost, nodes_expanded

def list_matrix_files(folder_path):
    #List all matrix files in the folder
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return []
    
    matrix_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    return matrix_files

def main():
    # Check if matrix folder path is provided
    if len(sys.argv) != 2:
        print("Usage: python part1.py <matrix_folder_path>")
        print("Example: python part2.py mats_911")
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
    

    print("\nRunning A* algorithm...")
    start_time = time.time()
    cpu_start = time.process_time()

    route, distance, nodes_expanded = astart(adj_matrix)

    runtime = time.time() - start_time
    cpu_time = time.process_time() - cpu_start

    print(f"\nRESULTS for {filename}:")
    print(f"Route: {route}")
    print(f"Total distance: {distance:.6f}")
    print(f"Runtime: {runtime:.6f} seconds")
    print(f"CPU Time: {cpu_time:.6f} seconds")
    print(f"Nodes expanded: {nodes_expanded}")


if __name__ == "__main__":
    main()