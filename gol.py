import pygame
import scipy.signal as signal
import numpy as np

R = 5  # Radius of kernel
b1, b2 = 34, 45  # Birth thresholds
s1, s2 = 20, 25  # Survival thresholds

# Initialize PyGame
pygame.init()

# Set up display
size = 128  # Reduced size for better visualization
cell_size = 5
cx, cy = 10, 10
game_width, game_height = size * cell_size, size * cell_size
info_width, info_height = 300, game_height
total_width = game_width + info_width
screen = pygame.display.set_mode((total_width, game_height))
pygame.display.set_caption("Conway's Game of Life and Kernel Info")

# Initialize grid
np.random.seed(0)
A = np.random.randint(2, size=(size, size))
K = np.asarray([[1,1,1], [1,0,1], [1,1,1]])
K_sum = np.sum(K)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def growth(U):
    return 0 + (U==3) - ((U<2)|(U>3))

def update(A):
    U = signal.convolve2d(A, K, mode='same', boundary='wrap')
    return np.clip(A + growth(U), 0, 1)

def draw_grid(surface, A):
    for y in range(size):
        for x in range(size):
            color = WHITE if A[y, x] == 1 else BLACK
            pygame.draw.rect(surface, color, (x * cell_size, y * cell_size, cell_size, cell_size))

def draw_kernel_info(surface):
    surface.fill(BLACK)
    
    # Draw kernel at the top-centered of info panel
    kernel_size = K.shape[0]
    cell_size = 50
    total_width = kernel_size * cell_size  # total width of all rectangles
    padding = 50  # padding between kernel and cross-section
    start_x = (info_width - total_width) // 2  # starting x-coordinate

    for y in range(kernel_size):
        for x in range(kernel_size):
            color = WHITE if K[y, x] == 1 else BLACK
            pygame.draw.rect(surface, color, (start_x + x * cell_size, y * cell_size + padding, cell_size, cell_size))
            pygame.draw.rect(surface, RED, (start_x + x * cell_size, y * cell_size + padding, cell_size, cell_size), 1)
    
    # Draw cross-section in center of info panel
    cross_section = K[kernel_size // 2, :]
    cross_section_width = len(cross_section) * 50  # total width of all rectangles in the cross-section

    start_x = (info_width - cross_section_width) // 2  # starting x-coordinate
    start_y = kernel_size * 50 + padding  # starting y-coordinate

    for i, value in enumerate(cross_section):
        color = WHITE if value == 1 else BLACK
        pygame.draw.rect(surface, color, (start_x + i * cell_size, start_y + padding, cell_size, cell_size))
        pygame.draw.rect(surface, RED, (start_x + i * cell_size, start_y + padding, cell_size, cell_size), 1)
    
    # Calculate growth function values
    x_vals = np.arange(9)
    y_vals = growth(x_vals)

    # Draw growth function plot
    plot_width = 100
    plot_height = 100
    start_x = (info_width - plot_width) // 2
    start_y = 400

    for i in range(9):
        x = start_x + i * (plot_width // 8)
        y = start_y + plot_height - y_vals[i] * plot_height
        pygame.draw.circle(surface, WHITE, (x, y), 5)

    for i in range(8):
        x1 = start_x + i * (plot_width // 8)
        y1 = start_y + plot_height - y_vals[i] * plot_height
        x2 = start_x + (i + 1) * (plot_width // 8)
        y2 = start_y + plot_height - y_vals[i + 1] * plot_height
        pygame.draw.line(surface, WHITE, (x1, y1), (x2, y2), 1)

    # Draw growth function info
    font = pygame.font.Font(None, 36)

    for i in range(1, -2, -1):
        text = font.render(str(i), True, WHITE)
        text_rect = text.get_rect(center=(start_x - 40, start_y + plot_height - i * plot_height))
        surface.blit(text, text_rect)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update grid
    A = update(A)

    # Draw grid
    game_surface = pygame.Surface((game_width, game_height))
    game_surface.fill(BLACK)
    draw_grid(game_surface, A)
    screen.blit(game_surface, (0, 0))

    # Draw kernel and growth function info
    info_surface = pygame.Surface((info_width, info_height))
    draw_kernel_info(info_surface)
    screen.blit(info_surface, (game_width, 0))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

pygame.quit()
