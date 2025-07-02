# File Imports
import pygame

# File Imports
import configs as cfg
import draw

# Initialize Pygame And Its Modules
pygame.init()  
pygame.key.set_repeat(250,50)  # Set key repeat delay and interval

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
        self.clipboard_text = ""
        self.active = False
        self.highlight_mode = False
        self.shift_start = [0,0]
        self.shift_end = [0,0]
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

    def update_highlight(self):
        pass

    def draw_border(self):
        if self.border_type == "solid":
            draw.rectangle(self.surface, (0, 0), self.width, self.height, self.border_thickness, self.border_color)
    
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
            draw.rectangle(self.surface, (cursor_x, cursor_y), 2, self.font.get_height(), 0, self.font_color)

    def draw_highlight(self):
        pass

    def draw(self, screen):
        self.surface.fill(self.background_color)
        self.draw_border()
        self.update_highlight()
        self.draw_highlight()
        self.draw_text()
        self.draw_cursor()
        draw.text(self.surface, f"Highlight mode: {"on" if self.highlight_mode else "off"}", (100, 400))
        screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, events):
        # If the surface is not active, just update and draw the text
        if self.active == False:
            self.draw(self.surface)
            return self.text
        
        # If the surface is active, handle events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.highlight_mode = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.highlight_mode = False

            elif event.type == pygame.MOUSEMOTION:
                pass

            elif event.type == pygame.KEYDOWN:
                if event.mod & pygame.KMOD_CTRL: # Check if Control key is held down
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_c:
                        pass
                    if event.key == pygame.K_v:
                        self.clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                        if self.clipboard_text:
                            try:
                                for t in pygame.scrap.get_types():
                                    #print(f"DEBUG: Clipboard type: {t}\n")
                                    pasted_text = self.clipboard_text.decode('utf-8')
                                    pasted_text = pasted_text.replace('\x0d', '')
                                    pasted_text = pasted_text.replace('\x00', '')
                                # Splicing the string to insert the text in between
                                end_of_text = self.text[self.cursor[0]][self.cursor[1]:]
                                self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]]
                                for c in pasted_text:
                                    if ord(c) == 10:  # New line character or LF (Line Feed)
                                        self.text.insert(self.cursor[0]+1, "")
                                        self.cursor[0] += 1
                                        self.cursor[1] = 0
                                    else:
                                        self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + c
                                        self.cursor[1] += 1
                                # Attaching the remenants of the string
                                self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + end_of_text
                            except UnicodeDecodeError:
                                print("Could not decode clipboard data as UTF-8")
                            except Exception as e:
                                print(f"An unexpected error occured during paste: {e}")
                    if event.key == pygame.K_x:
                        pass
                elif event.key == pygame.K_ESCAPE:
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
                            self.cursor[1] = len(self.text[self.cursor[0]-1])
                        self.cursor[0] -= 1
                elif event.key == pygame.K_DOWN:
                    if self.cursor[0] < len(self.text)-1:
                        if len(self.text[self.cursor[0]+1]) < self.cursor[1]:
                            self.cursor[1] = len(self.text[self.cursor[0]+1])
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
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.highlight_mode = True
                else:
                    self.cursor = [self.cursor[0], self.cursor[1] + 1]
                    self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + event.unicode + self.text[self.cursor[0]][self.cursor[1]:]
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.highlight_mode = False

        # Draw the updated surface
        self.draw(self.surface)
        return self.text