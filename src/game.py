class Game:
    """Manages the autonomous snake game."""
    def __init__(self):
        """Initializes the Game object."""
        global GRID_SIZE, WIDTH, HEIGHT, SNAKE_COLORS, NUM_SNAKES
        GRID_SIZE = settings.grid_size
        WIDTH = GRID_SIZE * CELL_SIZE
        HEIGHT = GRID_SIZE * CELL_SIZE
        SNAKE_COLORS = settings.selected_snake_colors
        NUM_SNAKES = settings.num_snakes

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autonomous Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            self.grid[0][i] = 1
            self.grid[GRID_SIZE-1][i] = 1
            self.grid[i][0] = 1
            self.grid[i][GRID_SIZE-1] = 1

        self.snakes = []
        start_positions = [(5, 5), (GRID_SIZE - 6, GRID_SIZE - 6), (5, GRID_SIZE - 6), (GRID_SIZE - 6, 5)]
        selected_algorithms = settings.selected_algorithms
        for i in range(NUM_SNAKES):
            self.snakes.append(Snake(start_positions[i], SNAKE_COLORS[i], i, selected_algorithms[i]))

        self.food_pos = generate_food(self.grid, self.snakes)
        self.game_over = False
        self.paused = False
        self.game_state = "MENU"
        self.menu_option_index = 0

    def reset(self):
        """Resets the game to its initial state using current settings."""
        global GRID_SIZE, WIDTH, HEIGHT, SNAKE_COLORS, NUM_SNAKES
        GRID_SIZE = settings.grid_size
        WIDTH = GRID_SIZE * CELL_SIZE
        HEIGHT = GRID_SIZE * CELL_SIZE
        SNAKE_COLORS = settings.selected_snake_colors
        NUM_SNAKES = settings.num_snakes

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            self.grid[0][i] = 1
            self.grid[GRID_SIZE-1][i] = 1
            self.grid[i][0] = 1
            self.grid[i][GRID_SIZE-1] = 1

        self.game_over = False
        self.paused = False
        self.game_state = "PLAYING"
        self.snakes = []
        start_positions = [(5, 5), (GRID_SIZE - 6, GRID_SIZE - 6), (5, GRID_SIZE - 6), (GRID_SIZE - 6, 5)]
        selected_algorithms = settings.selected_algorithms
        for i in range(NUM_SNAKES):
            self.snakes.append(Snake(start_positions[i], SNAKE_COLORS[i], i, selected_algorithms[i]))
        self.food_pos = generate_food(self.grid, self.snakes)

    def run(self):
        """Runs the main game loop."""
        running = True
        while running:
            if self.game_state == "STARTING_GAME":
                self.reset()
                self.game_state = "PLAYING"
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_state == "MENU":
                        self._handle_menu_input(event.key)
                    elif self.game_state == "PLAYING":
                        if event.key == pygame.K_SPACE:
                            self.paused = not self.paused
                        if event.key == pygame.K_r:
                            self.reset()
                    elif self.game_state == "GAME_OVER":
                        if event.key == pygame.K_r:
                            self.reset()
                            self.game_state = "MENU"

            if self.game_state == "PLAYING" and not self.game_over and not self.paused:
                food_eaten_by_any_snake = False
                for snake in self.snakes:
                    if snake.is_alive:
                        food_eaten = snake.move(self.grid, self.food_pos, self.snakes)
                        if food_eaten:
                            food_eaten_by_any_snake = True

                if food_eaten_by_any_snake:
                    self.food_pos = generate_food(self.grid, self.snakes)

                alive_snakes = sum(1 for snake in self.snakes if snake.is_alive)
                if alive_snakes <= 1:
                    self.game_over = True
                    self.game_state = "GAME_OVER"

            self.screen.fill(BACKGROUND_COLOR)

            if self.game_state == "MENU":
                self._draw_start_menu()
            elif self.game_state in ("PLAYING", "GAME_OVER"):
                draw_grid(self.screen)
                draw_food(self.screen, self.food_pos)
                for snake in self.snakes:
                    if snake.is_alive:
                        draw_snake(self.screen, snake)

                for i, snake in enumerate(self.snakes):
                    score_text = self.font.render(f"Snake {snake.id+1}: {snake.score}", True, snake.color)
                    self.screen.blit(score_text, (10, 10 + i * 20))

                if self.game_state == "GAME_OVER":
                    self._draw_game_over_screen()
                elif self.paused:
                    pause_text = self.font.render("Paused (Space to Play, R to Reset)", True, (255, 255, 255))
                    text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
                    self.screen.blit(pause_text, text_rect)
                else:
                    instruction_text = self.font.render("Space to Pause, R to Reset", True, (200, 200, 200))
                    self.screen.blit(instruction_text, (10, HEIGHT - 30))

            pygame.display.flip()
            self.clock.tick(FPS)

    def _draw_start_menu(self):
        """Draws a simpler vertical start menu layout."""
        self.screen.fill(BACKGROUND_COLOR)

        title_font = pygame.font.Font(None, 50)
        menu_font = pygame.font.Font(None, 28)

        grid_size_names = list(settings.grid_sizes.keys())
        current_grid_size_name = settings.selected_grid_size_name
        algorithm_names = settings.pathfinding_algorithms
        current_algorithm_indices = settings.selected_algorithm_indices

        title_text = title_font.render("Autonomous Snake Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        self.screen.blit(title_text, title_rect)

        menu_y_start = HEIGHT // 3
        line_height = 30

        color = (255, 255, 255) if self.menu_option_index == 0 else (200, 200, 200)
        grid_text = f"Grid Size: [{current_grid_size_name}] < >"
        grid_text_surface = menu_font.render(grid_text, True, color)
        grid_text_rect = grid_text_surface.get_rect(center=(WIDTH // 2, menu_y_start))
        self.screen.blit(grid_text_surface, grid_text_rect)

        color = (255, 255, 255) if self.menu_option_index == 1 else (200, 200, 200)
        algorithms_text_surface = menu_font.render("Algorithms:", True, color)
        algorithms_text_rect = algorithms_text_surface.get_rect(
            center=(WIDTH // 2, menu_y_start + line_height)
        )
        self.screen.blit(algorithms_text_surface, algorithms_text_rect)

        for snake_index in range(NUM_SNAKES):
            snake_color = (255, 255, 255) if (
                self.menu_option_index == 1 and
                settings.menu_snake_algorithm_index == snake_index
            ) else (200, 200, 200)

            snake_text = f"Snake {snake_index + 1}: [{algorithm_names[current_algorithm_indices[snake_index]]}]"
            snake_text_surface = menu_font.render(snake_text, True, snake_color)

            snake_text_rect = snake_text_surface.get_rect(
                center=(WIDTH // 2, menu_y_start + line_height * (2 + snake_index))
            )
            self.screen.blit(snake_text_surface, snake_text_rect)

        color = (255, 255, 255) if self.menu_option_index == 2 else (200, 200, 200)
        start_text_surface = menu_font.render("Start Game", True, color)
        start_text_rect = start_text_surface.get_rect(
            center=(WIDTH // 2, menu_y_start + line_height * (2 + NUM_SNAKES))
        )
        self.screen.blit(start_text_surface, start_text_rect)

    def _draw_game_over_screen(self):
        """Draws the game over screen with scores."""
        game_over_font = pygame.font.Font(None, 80)
        prompt_font = pygame.font.Font(None, 30)

        game_over_text = game_over_font.render("Game Over!", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 30))
        self.screen.blit(game_over_text, game_over_rect)

        score_y_pos = HEIGHT // 2
        for i, snake in enumerate(self.snakes):
            score_text = self.font.render(f"Snake {snake.id+1} Score: {snake.score}", True, snake.color)
            score_rect = score_text.get_rect(center=(WIDTH // 2, score_y_pos + i * 30))
            self.screen.blit(score_text, score_rect)

        restart_prompt_text = prompt_font.render("Press R to Restart to Menu", True, (200, 200, 200))
        restart_prompt_rect = restart_prompt_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(restart_prompt_text, restart_prompt_rect)

    def _handle_menu_input(self, key):
        """Handles key presses in the start menu."""
        if key == pygame.K_DOWN:
            self.menu_option_index = (self.menu_option_index + 1) % 3
            if self.menu_option_index == 1:
                settings.menu_snake_algorithm_index = 0

        elif key == pygame.K_UP:
            self.menu_option_index = (self.menu_option_index - 1) % 3
            if self.menu_option_index == 1:
                settings.menu_snake_algorithm_index = 0

        elif self.menu_option_index == 1:
            if key == pygame.K_1:
                settings.menu_snake_algorithm_index = 0
            elif key == pygame.K_2:
                settings.menu_snake_algorithm_index = 1
            elif key == pygame.K_3:
                settings.menu_snake_algorithm_index = 2
            elif key == pygame.K_4:
                settings.menu_snake_algorithm_index = 3
            elif key in (pygame.K_LEFT, pygame.K_RIGHT):
                self._adjust_menu_option(key, settings.menu_snake_algorithm_index)

        elif key in (pygame.K_LEFT, pygame.K_RIGHT):
            self._adjust_menu_option(key, None)

        elif key == pygame.K_SPACE or key == pygame.K_RETURN:
            if self.menu_option_index == 2:
                self.game_state = "STARTING_GAME"

    def _adjust_menu_option(self, key, snake_index):
        """Adjusts the selected menu option's value."""
        if self.menu_option_index == 0:
            grid_size_names = list(settings.grid_sizes.keys())
            current_index = grid_size_names.index(settings.selected_grid_size_name)
            if key == pygame.K_RIGHT:
                settings.selected_grid_size_name = grid_size_names[(current_index + 1) % len(grid_size_names)]
            elif key == pygame.K_LEFT:
                settings.selected_grid_size_name = grid_size_names[(current_index - 1) % len(grid_size_names)]

        elif self.menu_option_index == 1:
            if snake_index is not None:
                algorithm_names = settings.pathfinding_algorithms
                if key == pygame.K_RIGHT:
                    settings.selected_algorithm_indices[snake_index] = (
                        settings.selected_algorithm_indices[snake_index] + 1
                    ) % len(algorithm_names)
                elif key == pygame.K_LEFT:
                    settings.selected_algorithm_indices[snake_index] = (
                        settings.selected_algorithm_indices[snake_index] - 1
                    ) % len(algorithm_names)

        elif self.menu_option_index == 2:
            pass
