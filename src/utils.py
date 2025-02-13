import random
from src.settings import settings


def generate_food(grid, snakes):
    """Generates a random food position that is not on a snake."""
    global GRID_SIZE
    GRID_SIZE = settings.grid_size
    while True:
        food_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if grid[food_pos[1]][food_pos[0]] == 0:
            is_on_snake = False
            for snake in snakes:
                if food_pos in snake.body:
                    is_on_snake = True
                    break
            if not is_on_snake:
                return food_pos

def draw_grid(screen):
    """Draws the game grid on the screen."""
    global GRID_SIZE, WIDTH, HEIGHT
    GRID_SIZE = settings.grid_size
    WIDTH = GRID_SIZE * settings.cell_size
    HEIGHT = GRID_SIZE * settings.cell_size
    line_thickness = 1
    for x in range(0, WIDTH, settings.cell_size):
        x_coord = int(x)
        pygame.draw.line(screen, settings.grid_color, (x_coord, 0), (x_coord, HEIGHT), line_thickness)
    for y in range(0, HEIGHT, settings.cell_size):
        y_coord = int(y)
        pygame.draw.line(screen, settings.grid_color, (0, y_coord), (WIDTH, y_coord), line_thickness)

def draw_snake(screen, snake):
    """Draws a snake on the screen."""
    for segment in snake.body:
        rect = pygame.Rect(segment[0] * settings.cell_size, segment[1] * settings.cell_size, settings.cell_size, settings.cell_size)
        pygame.draw.rect(screen, snake.color, rect)

def draw_food(screen, food_pos):
    """Draws food on the screen."""
    rect = pygame.Rect(food_pos[0] * settings.cell_size, food_pos[1] * settings.cell_size, settings.cell_size, settings.cell_size)
    pygame.draw.rect(screen, settings.food_color, rect)

def is_valid_pos(pos):
    """Checks if a position is within the grid boundaries."""
    global GRID_SIZE
    GRID_SIZE = settings.grid_size
    return 0 <= pos[0] < GRID_SIZE and 0 <= pos[1] < GRID_SIZE
