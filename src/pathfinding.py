import heapq
from src.utils import is_valid_pos


def dijkstra(grid, start, end, snake_bodies_obstacles):
    """Finds the shortest path using Dijkstra's algorithm."""
    distances = {(r, c): float('inf') for r in range(len(grid)) for c in range(len(grid[0]))}
    previous_nodes = {(r, c): None for r in range(len(grid)) for c in range(len(grid[0]))}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_pos = heapq.heappop(priority_queue)

        if current_distance > distances[current_pos]:
            continue

        if current_pos == end:
            path = []
            while current_pos is not None:
                path.append(current_pos)
                current_pos = previous_nodes[current_pos]
            return path[::-1]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (current_pos[0] + dc, current_pos[1] + dr)

            if is_valid_pos(neighbor_pos) and grid[neighbor_pos[1]][neighbor_pos[0]] == 0 and neighbor_pos not in snake_bodies_obstacles:
                distance = current_distance + 1
                if distance < distances[neighbor_pos]:
                    distances[neighbor_pos] = distance
                    previous_nodes[neighbor_pos] = current_pos
                    heapq.heappush(priority_queue, (distance, neighbor_pos))

    return None


def astar(grid, start, end, snake_bodies_obstacles):
    """Finds the shortest path using A* algorithm."""
    distances = {(r, c): float('inf') for r in range(len(grid)) for c in range(len(grid[0]))}
    previous_nodes = {(r, c): None for r in range(len(grid)) for c in range(len(grid[0]))}
    distances[start] = 0
    priority_queue = [(0, start)]

    def heuristic(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

    while priority_queue:
        current_f_score, current_pos = heapq.heappop(priority_queue)

        if current_pos == end:
            path = []
            while current_pos is not None:
                path.append(current_pos)
                current_pos = previous_nodes[current_pos]
            return path[::-1]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (current_pos[0] + dc, current_pos[1] + dr)

            if is_valid_pos(neighbor_pos) and grid[neighbor_pos[1]][neighbor_pos[0]] == 0 and neighbor_pos not in snake_bodies_obstacles:
                distance = distances[current_pos] + 1
                if distance < distances[neighbor_pos]:
                    distances[neighbor_pos] = distance
                    previous_nodes[neighbor_pos] = current_pos
                    f_score = distance + heuristic(neighbor_pos)
                    heapq.heappush(priority_queue, (f_score, neighbor_pos))

    return None


def bfs(grid, start, end, snake_bodies_obstacles):
    """Finds the shortest path using BFS algorithm."""
    queue = [(start, [start])]
    visited = {start}

    while queue:
        current_pos, path = queue.pop(0)

        if current_pos == end:
            return path

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (current_pos[0] + dc, current_pos[1] + dr)

            if is_valid_pos(neighbor_pos) and grid[neighbor_pos[1]][neighbor_pos[0]] == 0 and neighbor_pos not in snake_bodies_obstacles and neighbor_pos not in visited:
                visited.add(neighbor_pos)
                new_path = list(path)
                new_path.append(neighbor_pos)
                queue.append((neighbor_pos, new_path))

    return None
