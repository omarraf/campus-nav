# Campus Navigation System

An interactive campus navigation system built with Python, Tkinter, and Pillow. This tool allows users to visualize a campus map and find paths between buildings using popular graph traversal algorithms like BFS, DFS, and Dijkstra's.

## Features
- **Interactive Visual Map**: Navigate the campus by selecting start and end buildings from a user-friendly interface.
- **Pathfinding Algorithms**:
  - **BFS**: Finds the shortest path by the number of stops.
  - **DFS**: Explores paths between buildings.
  - **Dijkstra’s Algorithm**: Computes the shortest path based on weighted distances.
- **Dynamic Visualization**: Real-time path traversal display for DFS, showing progress on the map.

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - `Tkinter` for GUI design and canvas-based visualization
  - `Pillow` (PIL) for image handling
  - `queue` and `heapq` for efficient graph traversal algorithms

## How It Works
1. The campus is modeled as a **graph** using an adjacency list where:
   - **Nodes** represent buildings.
   - **Edges** represent pathways with weights for distance and time.
2. Users interact with a visual map, selecting:
   - A start building
   - An end building
   - A pathfinding algorithm (BFS, DFS, or Dijkstra’s).
3. The chosen algorithm calculates the path, which is highlighted on the map:
   - BFS and Dijkstra’s display the shortest path.
   - DFS shows exploratory traversal and optionally visualizes progress in real-time.

