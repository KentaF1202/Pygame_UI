import pygame

# 1. Initialize Pygame
pygame.init()

# 2. Set initial window dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Window")

# Game loop control
running = True
clock = pygame.time.Clock()

while running:
    # 3. Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for the VIDEORESIZE event
        if event.type == pygame.VIDEORESIZE:
            # Get the new dimensions
            screen_width, screen_height = event.w, event.h
            # Re-create the screen surface with the new size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # 4. Drawing
    # Fill the background with a color
    screen.fill((0, 0, 25)) # Dark blue

    # Draw a rectangle in the center of the screen
    # Its position will update automatically as the screen size changes
    rect_width, rect_height = 100, 100
    rect_x = (screen_width - rect_width) / 2
    rect_y = (screen_height - rect_height) / 2
    pygame.draw.rect(screen, (255, 0, 0), (rect_x, rect_y, rect_width, rect_height))

    # 5. Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()