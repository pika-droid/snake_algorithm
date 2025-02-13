# --- Snake Class ---
class Snake:
    """Represents a snake in the autonomous snake game."""

    def __init__(self, start_pos, color, snake_id, algorithm_name):
        """Initializes a snake object."""
        self.body = [start_pos] * INITIAL_SNAKE_LENGTH
        self.color = color
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.id = snake_id
        self.score = 0
        self.is_alive = True
        self.algorithm_name = algorithm_name

    def move(self, grid, food_pos, snakes):
        """Moves the snake based on pathfinding and game rules."""
        if not self.is_alive:
            return False

        snake_bodies_obstacles = self._get_obstacle_positions(snakes)
        path = self._find_path_to_food(grid, food_pos, snake_bodies_obstacles)
        next_pos = self._determine_next_position(grid, path, snake_bodies_obstacles)

        if not next_pos:
            self.is_alive = False
            return False

        self.body.insert(0, next_pos)

        food_eaten = self._check_collisions_and_food(grid, food_pos, snake_bodies_obstacles)
        if not food_eaten:
            self.body.pop()
        return food_eaten

    def _get_obstacle_positions(self, snakes):
        """Collects positions of other snakes' bodies as obstacles."""
        snake_bodies_obstacles = set()
        for other_snake in snakes:
            if other_snake != self:
                snake_bodies_obstacles.update(other_snake.body)
        snake_bodies_obstacles.update(tuple(segment) for segment in self.body[1:])
        return snake_bodies_obstacles

    def _find_path_to_food(self, grid, food_pos, obstacles):
        """Finds a path to food using the selected pathfinding algorithm."""
        algorithm_name = self.algorithm_name
        if algorithm_name == "Dijkstra":
            return dijkstra(grid, self.body[0], food_pos, obstacles)
        elif algorithm_name == "A*":
            return astar(grid, self.body[0], food_pos, obstacles)
        elif algorithm_name == "BFS":
            return bfs(grid, self.body[0], food_pos, obstacles)
        else:
            return dijkstra(grid, self.body[0], food_pos, obstacles)

    def _determine_next_position(self, grid, path, obstacles):
        """Determines the next position based on path or survival moves."""
        if path and len(path) > 1:
            next_pos = path[1]
            self.direction = (next_pos[0] - self.body[0][0], next_pos[1] - self.body[0][1])
            return next_pos
        else:
            return self._survival_move(grid, obstacles)

    def _survival_move(self, grid, obstacles):
        """Attempts to make a safe move when no path to food is found."""
        possible_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(possible_directions)
        for dir_option in possible_directions:
            test_pos = (self.body[0][0] + dir_option[0], self.body[0][1] + dir_option[1])
            if self._is_safe_position(grid, test_pos, obstacles):
                self.direction = dir_option
                return test_pos
        return None

    def _is_safe_position(self, grid, pos, obstacles):
        """Checks if a position is safe (within bounds, not wall/obstacle)."""
        return is_valid_pos(pos) and grid[pos[1]][pos[0]] == 0 and pos not in obstacles

    def _check_collisions_and_food(self, grid, food_pos, obstacles):
        """Checks for collisions and if food is eaten."""
        head_pos = self.body[0]
        if not self._is_safe_position(grid, head_pos, obstacles) or head_pos in self.body[1:]:
            self.is_alive = False
            return False

        if head_pos == food_pos:
            self.score += 1
            return True
        else:
            return False

