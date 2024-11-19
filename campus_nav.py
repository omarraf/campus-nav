
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import queue
import heapq

class CampusMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Map Navigation")

        # Set canvas size to 800x600
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Load and resize campus map image
        self.image = Image.open("csuf_map.jpg")
        self.image = self.image.resize((800, 600))
        self.map_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)

        # Define nodes and edges
        self.nodes = {
            "MH": (334, 415), "DBH": (296, 440), "PL": (344, 334),
            "TG": (306, 269), "KHS": (295, 290), "B": (256, 320),
            "CPAC": (258, 379), "TSU": (149, 322), "VA": (124, 373),
            "SRC": (200, 268), "RG": (464, 250), "GAS": (537, 264),
            "UP": (108, 271), "NPS": (153, 434), "ENPS": (553, 372),
            "TS": (247, 117), "ECSL": (412, 309), "QUAD": (344, 385),
            "RH": (530, 226), "GF": (340, 101), "AF": (365, 142),
            "TSF": (387, 173), "CP": (452, 524), "TTC": (243, 227),
            "TL": (245, 283), "ECS": (484, 305), "SHCC": (412, 274),
            "EC": (394, 336), "H": (404, 382), "GH": (413, 415),
            "LH": (397, 444), "SGMH": (440, 458), "CJ": (430, 430)
        }

        self.edges = {
    "AF": {"GF": (400, 6), "TS": (378, 5), "TSF": (50, 1)},
    "B": {"CPAC": (110, 1), "KHS": (174, 2), "PL": (152, 2), "TSU": (112, 2), "VA": (227, 3)},
    "CJ": {"GH": (40, 1), "LH": (40, 1), "SGMH": (12, 1)},
    "CP": {"ENPS": (597, 8), "NPS": (747, 10), "SGMH": (385, 5)},
    "CPAC": {"KHS": (224, 3), "MH": (63, 1), "NPS": (681, 9), "QUAD": (63, 1), "VA": (242, 3), "B": (110, 1)},
    "DBH": {"LH": (148, 2), "MH": (22, 0), "NPS": (547, 7), "QUAD": (209, 3), "SGMH": (296, 4)},
    "EC": {"ECSL": (55, 1), "H": (126, 2), "PL": (68, 1), "SHCC": (140, 2)},
    "ECS": {"ECSL": (69, 1), "ENPS": (180, 2), "GAS": (90, 1), "RG": (113, 2), "RH": (219, 3), "SHCC": (88, 1)},
    "ECSL": {"PL": (129, 2), "RG": (164, 2), "SHCC": (28, 0), "TG": (170, 2), "EC": (55, 1), "ECS": (69, 1)},
    "ENPS": {"GAS": (504, 7), "CP": (597, 8), "ECS": (180, 2)},
    "GAS": {"RG": (65, 1), "RH": (29, 0), "ECS": (90, 1), "ENPS": (504, 7)},
    "GF": {"TS": (115, 2), "AF": (400, 6)},
    "GH": {"H": (77, 1), "MH": (201, 3), "QUAD": (150, 2), "SGMH": (99, 1), "CJ": (40, 1), "LH": (40, 1)},
    "H": {"MH": (169, 2), "PL": (130, 2), "QUAD": (52, 1), "EC": (126, 2), "GH": (77, 1)},
    "KHS": {"PL": (140, 2), "TG": (8, 0), "TL": (88, 1), "B": (174, 2), "CPAC": (224, 3)},
    "LH": {"SGMH": (33, 0), "GH": (40, 1), "DBH": (50, 1), "CJ": (40, 1)},
    "MH": {"QUAD": (48, 1), "CPAC": (63, 1), "DBH": (22, 0), "GH": (201, 3), "H": (169, 2)},
    "NPS": {"VA": (350, 5), "CP": (747, 10), "CPAC": (681, 9), "DBH": (547, 7)},
    "PL": {"QUAD": (10, 0), "TG": (73, 1), "B": (152, 2), "EC": (68, 1), "ECSL": (129, 2), "H": (130, 2), "KHS": (140, 2)},
    "RG": {"RH": (100, 1), "SHCC": (147, 2), "ECS": (113, 2), "ECSL": (164, 2), "GAS": (65, 1)},
    "SHCC": {"TG": (120, 2), "EC": (140, 2), "ECS": (88, 1), "ECSL": (28, 0), "RG": (147, 2)},
    "SRC": {"TG": (122, 2), "TL": (10, 0), "TSU": (118, 2), "TTC": (132, 2), "UP": (236, 3)},
    "TG": {"TL": (3, 0), "ECSL": (170, 2), "KHS": (8, 0), "PL": (73, 1), "SHCC": (120, 2), "SRC": (122, 2)},
    "TL": {"TTC": (80, 1), "KHS": (88, 1), "SRC": (10, 0), "TG": (3, 0)},
    "TSF": {"TTC": (7, 1), "AF": (50, 1)},
    "TSU": {"UP": (230, 3), "VA": (111, 1), "B": (112, 2), "SRC": (118, 2)},
    "TS": {"AF": (378, 5), "GF": (115, 2)},
    "VA": {"B": (227, 3), "CPAC": (242, 3), "NPS": (350, 5), "TSU": (111, 1)},
    "SGMH": {"CJ": (12, 1), "CP": (385, 5), "DBH": (296, 4), "GH": (99, 1), "LH": (33, 0)},
    "QUAD": {"CPAC": (63, 1), "DBH": (209, 3), "GH": (150, 2), "H": (52, 1), "MH": (48, 1), "PL": (10, 0)},
    "RH": {"ECS": (219, 3), "GAS": (29, 0), "RG": (100, 1)},
    "TTC": {"SRC": (132, 2), "TL": (80, 1), "TSF": (7, 1)},
    "UP": {"SRC": (236, 3), "TSU": (230, 3)}
}

        for node, neighbors in list(self.edges.items()):
            for neighbor, (distance, time) in neighbors.items():
                if neighbor not in self.edges:
                    self.edges[neighbor] = {}
                if node not in self.edges[neighbor]:
                    self.edges[neighbor][node] = (distance, time)

        


        # Draw nodes and edges on the map
        self.draw_connectivity()

        # User input fields for start, end, and algorithm selection
        self.start_label = tk.Label(root, text="Start Node:")
        self.start_label.pack()
        self.start_dropdown = ttk.Combobox(root, values=list(self.nodes.keys()))
        self.start_dropdown.pack()

        self.end_label = tk.Label(root, text="End Node:")
        self.end_label.pack()
        self.end_dropdown = ttk.Combobox(root, values=list(self.nodes.keys()))
        self.end_dropdown.pack()

        self.algorithm_label = tk.Label(root, text="Algorithm:")
        self.algorithm_label.pack()
        self.algorithm_dropdown = ttk.Combobox(root, values=["BFS", "DFS", "Dijkstra"])
        self.algorithm_dropdown.pack()

        # Create a frame for buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        # Button to execute the selected algorithm
        self.find_path_button = tk.Button(self.button_frame, text="Find Path", command=self.execute_algorithm)
        self.find_path_button.pack(side=tk.LEFT, padx=5)

        # Add Reset button
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_all)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def reset_all(self):
        # Clear all entry fields
        self.start_dropdown.set('')
        self.end_dropdown.set('')
        self.algorithm_dropdown.set('')
        
        # Clear the canvas and redraw the original map
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)
        self.draw_connectivity()

    def draw_connectivity(self):
        # Draw edges to show connectivity before finding paths
        for node, neighbors in self.edges.items():
            x1, y1 = self.nodes[node]
            for neighbor in neighbors:
                x2, y2 = self.nodes[neighbor]
                self.canvas.create_line(x1, y1, x2, y2, fill="grey", dash=(2, 4))  # Grey dashed lines for general connectivity

        # Draw nodes
        for node, (x, y) in self.nodes.items():
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")
            self.canvas.create_text(x, y - 10, text=node, fill="black")

    def execute_algorithm(self):
        start_node = self.start_dropdown.get().upper()
        end_node = self.end_dropdown.get().upper()
        algorithm = self.algorithm_dropdown.get().upper()

        if start_node not in self.nodes or end_node not in self.nodes:
            print("Invalid start or end node")
            return

        if algorithm == "BFS":
            path = self.bfs(start_node, end_node)
            self.highlight_path(path, "green")
        elif algorithm == "DFS":
            path = self.dfs(start_node, end_node)
            self.highlight_path(path, "orange")
        elif algorithm == "DIJKSTRA":
            path, total_distance = self.dijkstra(start_node, end_node)
            if path:
                self.highlight_path(path, "purple")

                # Calculate total time based on the final path
                total_time = sum(self.edges[path[i]][path[i + 1]][1] for i in range(len(path) - 1))

                # Display a popup with accumulated distance and time
                messagebox.showinfo("Dijkstra's Shortest Path",
                                    f"Shortest path: {' -> '.join(path)}\n"
                                    f"Total Distance: {total_distance} meters\n"
                                    f"Estimated Time: {total_time} minutes")
            else:
                print("No path found")
        else:
            print("Invalid algorithm selection")

    def bfs(self, start, end):
        visited = set()
        queue = [(start, [start])]
        while queue:
            current, path = queue.pop(0)
            if current == end:
                return path
            for neighbor in self.edges.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def dfs(self, start, end):
        # if start == end:
        #     return [start]

        # # Stack to keep track of the current node and path
        # stack = [(start, [start])]
        # best_path = []

        # while stack:
        #     current, path = stack.pop()

        #     # If we reached the end, check if this path is the longest so far
        #     if current == end and len(path) > len(best_path):
        #         best_path = path[:]
        #         continue

        #     # Explore all neighbors, allowing revisits if they don’t create loops
        #     neighbors = self.edges.get(current, [])
        #     for neighbor in neighbors:
        #         if neighbor not in path:  # Prevents cycles by not revisiting nodes in the current path
        #             new_path = path + [neighbor]
        #             stack.append((neighbor, new_path))

        # return best_path if best_path else []
        """Modified DFS to find a reasonably long path without exhaustive search"""
        if start == end:
            return [start]
            
        # Keep track of visited nodes and their visit counts
        visit_counts = {node: 0 for node in self.nodes}
        visit_counts[start] = 1
        
        # Stack will store tuples of (current_node, current_path)
        stack = [(start, [start])]
        best_path = []
        
        while stack:
            current, path = stack.pop()
            
            # If we found end node, update best path if this one is longer
            if current == end and len(path) > len(best_path):
                best_path = path[:]
                continue
                
            # Add unvisited or less visited neighbors to stack
            neighbors = self.edges.get(current, [])
            for neighbor in neighbors:
                if visit_counts.get(neighbor, 0) < 1:  # Allow each node to be visited once
                    visit_counts[neighbor] = 1
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))
        
        return best_path if best_path else []

    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        
        # Priority queue to hold nodes to explore: (cumulative distance, current node, path)
        queue = [(0, start, [start])]
        # Keep track of visited nodes and their optimal paths
        best_paths = {start: [start]}

        while queue:
            current_distance, current_node, current_path = heapq.heappop(queue)

            # If we've found a longer path to this node, skip it
            if current_distance > distances[current_node]:
                continue

            # If we've reached the end node, return the path and total distance
            if current_node == end:
                return current_path, distances[end]

            # Explore neighbors
            for neighbor, (edge_distance, _) in self.edges[current_node].items():
                distance = current_distance + edge_distance

                # If we've found a shorter path to the neighbor
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    new_path = current_path + [neighbor]
                    best_paths[neighbor] = new_path
                    heapq.heappush(queue, (distance, neighbor, new_path))

        # If we get here, no path was found
        return None, None


    def highlight_path(self, path, color):
        for i in range(len(path) - 1):
            x1, y1 = self.nodes[path[i]]
            x2, y2 = self.nodes[path[i + 1]]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

root = tk.Tk()
app = CampusMapApp(root)
root.mainloop()



'''
'AF', 'GF') 400m :06
('AF', 'TS') 378m :05
('AF', 'TSF') 50m :01
('B', 'CPAC') 110m :01
('B', 'KHS') 174m :02
('B', 'PL') 152m :02
('B', 'TSU') 112m :02
('B', 'VA') 227m :03
('CJ', 'GH') 40m :01
('CJ', 'H') 
('CJ', 'LH') 40m :01
('CJ', 'SGMH') 12m :01
('CP', 'ENPS') 597m :08
('CP', 'NPS') 747m :10
('CP', 'SGMH') 385m :05
('CPAC', 'KHS') 224m :03
('CPAC', 'MH') 63m :01
('CPAC', 'NPS') 681m :09
('CPAC', 'QUAD') 63m :01
('CPAC', 'VA') 242m :03
('DBH', 'LH') 148m :02
('DBH', 'MH') 22m :00
('DBH', 'NPS') 547m :07
('DBH', 'QUAD') 209m :03
('DBH', 'SGMH') 296m :04
('EC', 'ECSL') 55m :01
('EC', 'H') 126m :02
('EC', 'PL') 68m :01
('EC', 'SHCC') 140m :02
('ECS', 'ECSL') 69m :01
('ECS', 'ENPS') 180m :02
('ECS', 'GAS') 90m :01
('ECS', 'RG') 113m :02
('ECS', 'RH') 219m :03
('ECS', 'SHCC') 88m :01
('ECSL', 'PL') 129m :02
('ECSL', 'RG') 164m :02
('ECSL', 'SHCC') 28m :00
('ECSL', 'TG') 170m :02
('ENPS', 'GAS') 504m :07
('ENPS', 'NPS') X
('GAS', 'RG') 65m :01
('GAS', 'RH') 29m :00
('GF', 'TS') 115m :02
('GF', 'TSF') X
('GH', 'H') 77m :01
('GH', 'MH') 201m :03
('GH', 'QUAD') 150m :02
('GH', 'SGMH') 99m :01
('H', 'MH') 169m :02
('H', 'PL') 130m :02
('H', 'QUAD') 52m :01
('KHS', 'PL') 140m :02
('KHS', 'TG') 8m :00
('KHS', 'TL') 88m :01
('LH', 'SGMH') 33m :00
('LH', 'GH') 40m :01
('LH', 'DBH') 50m :01
('MH', 'QUAD') 48m :01
('NPS', 'VA') 350m :05
('PL', 'QUAD') 10m :00
('PL', 'TG') 73m :01
('RG', 'RH') 100m :01
('RG', 'SHCC') 147m :02
('SHCC', 'TG') 120m :02
('SRC', 'TG') 122m :02
('SRC', 'TL') 10m :00
('SRC', 'TSU') 118m :02
('SRC', 'TTC') 132m :02
('SRC', 'UP') 236m :03
('TG', 'TL') 3m :00
('TL', 'TS') X
('TL', 'TTC') 80m :01
('TS', 'TSF') X
('TS', 'TTC') X
('TSF', 'TTC') 7m :01
('TSU', 'UP') 230m :03
('TSU', 'VA') 111m :01
('TTC', 'UP') X
'''