# Module Imports
import pygame
import os
import sys

# File Imports
import configs as cfg
import draw
import text_editor

# Pygame Initialization
pygame.init()

# Screen Variables
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((WIDTH - cfg.WINDOW_OFFSET_X, HEIGHT - cfg.WINDOW_OFFSET_Y), pygame.RESIZABLE)
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{cfg.WINDOW_OFFSET_X}, {cfg.WINDOW_OFFSET_Y}"

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Main function to run the game loop
#----------------------------------------------------------------------------------------------
def main():
    # Running variables
    running = True
    capslock = False

    # Initialize surfaces
    # Text Editor Surface
    text_editor_rect = (0, 0, WIDTH - cfg.WINDOW_OFFSET_X, HEIGHT - cfg.WINDOW_OFFSET_Y)
    text_editor_surface = text_editor.Surface(text_editor_rect)
    text_editor_surface.set_active()
    text_editor_surface.set_border()

    # Game loop
    while running:
        # Event handler
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Pass events to surfaces
        text_editor_surface.handle_event(events)

        # Drawing to screen
        screen.fill(cfg.WHITE)
        text_editor_surface.draw(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(cfg.FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()