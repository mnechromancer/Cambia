import pygame
import scipy.signal as signal
import numpy as np

# Initialize PyGame
pygame.init()

# Set up display
size = 128  # Reduced size for better visualization
cell_size = 5
game_width, game_height = size * cell_size, size * cell_size
info_width, info_height = 300, game_height
total_width = game_width + info_width
screen = pygame.display.set_mode((total_width, game_height))
pygame.display.set_caption("Conway's Game of Life and Kernel Info")

# Initialize grid
np.random.seed(0)
A = np.random.randint(2, size=(size, size))
K = np.asarray([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
K_sum = np.sum(K)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def growth(U):
    return 0 + (U == 3) - ((U < 2) | (U > 3))

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
    
    # Draw kernel
    kernel_size = K.shape[0]
    for y in range(kernel_size):
        for x in range(kernel_size):
            color = WHITE if K[y, x] == 1 else BLACK
            pygame.draw.rect(surface, color, (x * 50, y * 50, 50, 50))
            pygame.draw.rect(surface, RED, (x * 50, y * 50, 50, 50), 1)
    
    # Draw cross-section
    cross_section = K[kernel_size // 2, :]
    for i, value in enumerate(cross_section):
        color = WHITE if value == 1 else BLACK
        pygame.draw.rect(surface, color, (i * 50, 150, 50, 50))
        pygame.draw.rect(surface, RED, (i * 50, 150, 50, 50), 1)
    
    # Draw growth function
    x_vals = np.linspace(0, K_sum, 100)
    y_vals = growth(x_vals)
    points = [(int(x * 50), int(250 - y * 50)) for x, y in zip(x_vals, y_vals)]
    if len(points) > 1:
        pygame.draw.lines(surface, WHITE, False, points)

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
