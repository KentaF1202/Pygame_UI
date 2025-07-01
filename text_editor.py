# File Imports
import pygame

# File Imports
import configs as cfg
import draw

# Initialize Pygame
pygame.init()  

# Class for the Text Editor Surface
class Surface:
    def __init__(self, rect, placeholder_text=""):
        self.surface = pygame.Surface((rect[2], rect[3]))
        self.x = rect[0]
        self.y = rect[1]
        self.margin_x = cfg.text_margin_x
        self.margin_y = cfg.text_margin_y
        self.line_spacing = cfg.text_line_spacing
        self.text = [""]
        self.placeholder_text = placeholder_text
        self.active = False
        self.cursor_visible = True
        self.cursor = [0, 0]
        self.font_type = cfg.text_font_type
        self.font_size = cfg.text_font_size
        self.font = cfg.text_font
        self.font_color = cfg.GREEN
        self.background_color = cfg.BLACK

    def set_background_color(self, color):
        self.background_color = color

    def set_border(self, border_type, border_color, border_thickness):
        pass

    def set_font(self, font_type="Ubuntu", font_size=24, font_color=cfg.GREEN):
        self.font_type = font_type
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.font_color = font_color

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def draw_border(self):
        pass

    def draw_text(self):
        for i, line in enumerate(self.text):
            draw.text(self.surface, line, (self.margin_x, self.margin_y + (i * (self.font.get_height() + self.line_spacing))), self.font_size, self.font_color)

    def draw_cursor(self):
        # If the surface is inactive or cursor is not visible, do not draw it
        if self.active == False or self.cursor_visible == False:
            return

        if (pygame.time.get_ticks() % 1000 < 500):
            cursor_x = self.margin_x + (self.font.size(self.text[self.cursor[0]][:self.cursor[1]])[0])
            cursor_y = self.margin_y + (self.cursor[0] * (self.font.get_height() + self.line_spacing))
            print(f"font: {self.font}")
            print(f"font height: {self.font.get_height()}")
            draw.rectangle(self.surface, (cursor_x, cursor_y), 2, self.font.get_height(), 0, self.font_color)

    def draw(self, screen):
        self.surface.fill(self.background_color)
        self.draw_border()
        self.draw_text()
        self.draw_cursor()
        screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, events, capslock):
        # If the surface is not active, just update and draw the text
        if self.active == False:
            self.draw(self.surface)
            return self.text
        
        # If the surface is active, handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    pass
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    self.cursor = [self.cursor[0], self.cursor[1] + 1]
                    self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + event.unicode + self.text[self.cursor[0]][self.cursor[1]:]

        # Draw the updated surface
        self.draw(self.surface)
        return self.text