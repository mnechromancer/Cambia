import pygame
import scipy.signal as signal
import numpy as np

# Initialize PyGame
pygame.init()

# Set up display
size = 256
cell_size = 2
width, height = size * cell_size, size * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Conway\'s Game of Life')

# Initialize grid
np.random.seed(0)
A = np.random.randint(2, size=(size, size))
K = np.asarray([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
K_sum = np.sum(K)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def growth(U):
    return 0 + (U==3) - ((U<2) | (U>3))

def update(A):
    # Neighbor sum (for discrete neighbors)
    # U = sum(np.roll(A, (i, j), axis=(0, 1)) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i != 0 or j != 0))
    # Convolution (for continuous neighbors)
    U = signal.convolve2d(A, K, mode='same', boundary='wrap')
    # Conditional Update
    # return (A & (U==2) | (U==3))
    # Incremental Update and Clipping
    return np.clip(A + growth(U), 0, 1)

def draw_grid(screen, A):
    for y in range(size):
        for x in range(size):
            color = BLACK if A[y, x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

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
    screen.fill(BLACK)
    draw_grid(screen, A)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(20)

pygame.quit()
