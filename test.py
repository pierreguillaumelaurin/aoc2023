import heapq

def shortest_path(matrix, start, end):
    # Directions for moving up, down, left, and right
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    rows, cols = len(matrix), len(matrix[0])
    # Priority queue to hold nodes to explore next, formatted as (cost, (x, y))
    pq = [(1, start)]
    # Dictionary to track the minimum cost to reach a node
    costs = {start: 0}
    
    while pq:
        # Get the current node with the lowest cost
        cost, (x, y) = heapq.heappop(pq)
        
        # If we've reached the end, return the cost
        if (x, y) == end:
            return cost
        
        # Explore all adjacent nodes
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Ensure the new node is within the bounds of the matrix
            if 0 <= nx < rows and 0 <= ny < cols:
                # Calculate new cost to reach adjacent node
                new_cost = cost + matrix[nx][ny]
                # If this path to neighbor is cheaper than any previous one, record it
                if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                    costs[(nx, ny)] = new_cost
                    heapq.heappush(pq, (new_cost, (nx, ny)))
    # If the destination is not reachable, return None or an indication of failure
    return None

# Example matrix (each cell's value represents the weight to move to that cell)
matrix = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1]
]

# Start and end positions
start = (0, 0) # Top-left corner
end = (2, 2) # Bottom-right corner

# Find the shortest path
print(shortest_path(matrix, start, end))

