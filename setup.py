import pygame
import scipy.signal as signal
import numpy as np

R = 2  # Radius of kernel
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

# Initialize grid
np.random.seed(0)
A = np.random.randint(2, size=(size, size))
K = np.asarray([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
# Make a circular kernel with radius R
# y, x = np.ogrid[-R:R + 1, -R:R + 1]
# K = x ** 2 + y ** 2 <= R ** 2
# K = K.astype(int)
# K[R, R] = 0

# Normalize kernel
K_sum = np.sum(K)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)