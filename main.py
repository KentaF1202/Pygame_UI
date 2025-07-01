# Module Imports
import pygame
import os
import sys

# File Imports
import configs as cfg
#import shapes
#import text_editor

# Pygame Initialization
pygame.init()

# Screen Variables
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{cfg.WINDOW_OFFSET_X}, {cfg.WINDOW_OFFSET_Y}"

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Main function to run the game loop
#----------------------------------------------------------------------------------------------
def main():
    # Running variables
    running = True

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen with a color
        screen.fill(cfg.VS_GREY)

        # Update the display
        pygame.display.flip()
        clock.tick(cfg.FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()