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
pygame.display.set_caption("Pygame UI")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Scrap Initialization
pygame.scrap.init()

# Collision Function
def collision(mousepos, rect):
    mousex, mousey = mousepos[0], mousepos[1]
    x, y, width, height = rect
    if (mousex > x and mousex < x+width):
        if (mousey > y and mousey < y+height):
            return True
    return False
    
# Main function to run the game loop
#----------------------------------------------------------------------------------------------
def main():
    # Running variables
    running = True

    # Starter variables
    mouse_pos = (0,0)

    # Initialize surfaces
    # Text Editor Surface
    text_editor_rect = (0, 0, (WIDTH - cfg.WINDOW_OFFSET_X) // 2, HEIGHT - cfg.WINDOW_OFFSET_Y)
    text_editor_surface = text_editor.Surface(text_editor_rect)
    text_editor_surface.set_active()
    text_editor_surface.set_border()

    te2_rect = ((WIDTH - cfg.WINDOW_OFFSET_X) // 2, 0, (WIDTH - cfg.WINDOW_OFFSET_X) // 2, HEIGHT - cfg.WINDOW_OFFSET_Y)
    te2_surface = text_editor.Surface(te2_rect)
    te2_surface.set_border()

    # Game loop
    while running:
        # Event handler
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if collision(mouse_pos, text_editor_rect):
                        text_editor_surface.set_active()
                        te2_surface.set_inactive()
                    elif collision(mouse_pos, te2_rect):
                        te2_surface.set_active()
                        text_editor_surface.set_inactive()
                    else:
                        te2_surface.set_inactive()
                        text_editor_surface.set_inactive()
                elif event.button == 3:
                    print("Right click pressed")
                elif event.button == 4:
                    print("Scroll up")
                elif event.button == 5:
                    print("Scroll down")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
        # Pass events to surfaces
        text_editor_surface.handle_event(events)
        te2_surface.handle_event(events)

        # Drawing to screen
        screen.fill(cfg.WHITE)
        text_editor_surface.draw(screen)
        te2_surface.draw(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(cfg.FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()