from gol_utils import *

screen = pygame.display.set_mode((total_width, game_height))
pygame.display.set_caption("Conway's Game of Life and Kernel Info")

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
    clock.tick(5)

pygame.quit()
