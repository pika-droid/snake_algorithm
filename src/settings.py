class GameSettings:
    """Encapsulates game settings and constants."""
    def __init__(self):
        self.grid_sizes = {"Small": 20, "Medium": 30, "Large": 40}
        self.selected_grid_size_name = "Medium" 

        self.cell_size = 15
        self.snake_colors_options = [(255, 0, 0), (255, 255, 0), (255, 255, 255), (255, 105, 180)]
        self.selected_snake_colors_indices = [0, 1, 2, 3]
        self.food_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.grid_color = (100, 100, 100)
        self.fps = 15
        self.initial_snake_length = 3
        self.num_snakes_options = [4]
        self.selected_num_snakes_index = 0
        self.pathfinding_algorithms = ["Dijkstra", "A*", "BFS"]
        self.selected_algorithm_indices = [0, 1, 0, 1]
        self.menu_snake_algorithm_index = 0

    @property
    def grid_size(self):
        return self.grid_sizes[self.selected_grid_size_name]

    @property
    def num_snakes(self):
        return self.num_snakes_options[self.selected_num_snakes_index]

    @property
    def selected_snake_colors(self):
        return [self.snake_colors_options[i] for i in self.selected_snake_colors_indices]

    @property
    def selected_algorithms(self):
        return [self.pathfinding_algorithms[i] for i in self.selected_algorithm_indices]


settings = GameSettings()

# --- Game Constants ---
CELL_SIZE = settings.cell_size
FOOD_COLOR = settings.food_color
BACKGROUND_COLOR = settings.background_color
GRID_COLOR = settings.grid_color
FPS = settings.fps
INITIAL_SNAKE_LENGTH = settings.initial_snake_length
NUM_SNAKES = 4
SNAKE_COLORS = settings.selected_snake_colors
