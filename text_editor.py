# File Imports
import pygame

# File Imports
import configs as cfg
import draw

# Initialize Pygame And Its Modules
pygame.init()  
pygame.scrap.init()
pygame.key.set_repeat(500, 100)  # Set key repeat delay and interval

# Class for the Text Editor Surface
class Surface:
    def __init__(self, rect, placeholder_text=""):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.surface = pygame.Surface((self.width, self.height))
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
        self.border_type = "none"
        self.border_color = cfg.VS_LIGHT_GREY
        self.border_thickness = 1

    def set_background_color(self, color):
        self.background_color = color

    def set_border(self, border_type="solid", border_color=cfg.VS_LIGHT_GREY, border_thickness=1):
        if border_type == "solid":
            self.border_type = border_type
        else:
            self.border_type = "none"
        self.border_color = border_color
        self.border_thickness = border_thickness

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
        if self.border_type == "solid":
            draw.rectangle(self.surface, (self.x, self.y), self.width, self.height, self.border_thickness, self.border_color)
    
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

    def handle_event(self, events):
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
                    if self.cursor[1] > 0:
                        self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1] - 1] + self.text[self.cursor[0]][self.cursor[1]:]
                        self.cursor[1] -= 1
                    elif self.cursor[0] > 0:
                        # Merge with the previous line
                        self.cursor[1] = len(self.text[self.cursor[0] - 1])
                        self.text[self.cursor[0] - 1] += self.text[self.cursor[0]]
                        del self.text[self.cursor[0]]
                        self.cursor[0] -= 1
                elif event.key == pygame.K_RETURN:
                    if self.cursor[1] == len(self.text[self.cursor[0]]):
                        self.text.insert(self.cursor[0]+1, "")
                    else:
                        self.text.insert(self.cursor[0]+1, self.text[self.cursor[0]][self.cursor[1]:])
                        self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]]
                    self.cursor[0] += 1
                    self.cursor[1] = 0
                elif event.key == pygame.K_UP:
                    if self.cursor[0] > 0:
                        if len(self.text[self.cursor[0]-1]) < self.cursor[1]:
                            self.cursor[1] = len(self.text[self.cursor[0]])
                        self.cursor[0] -= 1
                elif event.key == pygame.K_DOWN:
                    if self.cursor[0] < len(self.text)-1:
                        if len(self.text[self.cursor[0]+1]) < self.cursor[1]:
                            self.cursor[1] = len(self.text[self.cursor[0]])
                        self.cursor[0] += 1
                elif event.key == pygame.K_LEFT:
                    if self.cursor[1] == 0:
                        if self.cursor[0] > 0:
                            self.cursor[0] -= 1
                            self.cursor[1] = len(self.text[self.cursor[0]])
                    else:
                        self.cursor[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.cursor[1] == len(self.text[self.cursor[0]]):
                        if self.cursor[0] < len(self.text)-1:
                            self.cursor[0] += 1
                            self.cursor[1] = 0
                    else:
                        self.cursor[1] += 1
                else:
                    self.cursor = [self.cursor[0], self.cursor[1] + 1]
                    self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + event.unicode + self.text[self.cursor[0]][self.cursor[1]:]

        # Draw the updated surface
        self.draw(self.surface)
        return self.text