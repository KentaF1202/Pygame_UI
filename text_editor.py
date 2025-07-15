# TODO
# Finish mouse_to_cursor, delete_highlight, and draw_highlight

# File Imports
import pygame

# File Imports
import configs as cfg
import draw

# Initialize Pygame
pygame.init()  

# Set key repeat delay and interval
pygame.key.set_repeat(250,50)  

# Class for the Text Editor Surface
class Surface:
    def __init__(self, rect):
        # Dimensions
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        
        # Surface
        self.surface = pygame.Surface((self.width, self.height))
        self.background_color = cfg.BLACK
        self.active = False

        # Border
        self.border_type = "none"
        self.border_color = cfg.VS_LIGHT_GREY
        self.border_thickness = 1

        # Text 
        self.text = [""]
        self.placeholder_text = ""
        self.clipboard_text = ""

        # Font
        self.font_type = cfg.text_font_type
        self.font_size = cfg.text_font_size
        self.font = cfg.text_font
        self.font_color = cfg.GREEN

        # Text Spacing
        self.margin_x = cfg.text_margin_x
        self.margin_y = cfg.text_margin_y
        self.line_spacing = cfg.text_line_spacing
        self.line_height = self.font.get_height() + self.line_spacing

        # Cursor
        self.cursor_visible = True
        self.cursor = [0, 0]

        # Highlight
        self.highlight_mode = False
        self.highlight_start = [0,0]
        self.highlight_end = [0,0]

    def set_placeholder(self, placeholder):
        self.placeholder_text = placeholder

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
        self.line_height = self.font.get_height() + self.line_spacing

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def draw_border(self):
        if self.border_type == "solid":
            draw.rectangle(self.surface, (0, 0), self.width, self.height, self.border_thickness, self.border_color)
    
    def draw_text(self):
        for i, line in enumerate(self.text):
            draw.text(self.surface, line, (self.margin_x, self.margin_y + (i * self.line_height)), self.font_size, self.font_color)

    def draw_cursor(self):
        # If the surface is inactive or cursor is not visible, do not draw it
        if self.active == False or self.cursor_visible == False:
            return

        if (pygame.time.get_ticks() % 1000 < 500):
            cursor_x, cursor_y = self.cursor_to_coords(self.cursor[0], self.cursor[1])
            draw.rectangle(self.surface, (cursor_x, cursor_y), 2, self.font.get_height(), 0, self.font_color)

    def draw_highlight(self):
        # If on same row
        if (self.highlight_start[0] == self.highlight_end[0]):
            # If start comes first
            if (self.highlight_start[1] < self.highlight_end[1]):
                cursor_x1, cursor_y1 = self.cursor_to_coords(self.highlight_start[0], self.highlight_start[1])
                cursor_x2, _ = self.cursor_to_coords(self.highlight_end[0], self.highlight_end[1])
                draw.text(self.surface, f"SL: x, y, width, height: {cursor_x1}, {cursor_y1}, {cursor_x2-cursor_x1}, {self.line_height}", (400,0), 40, cfg.GREEN)
                draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)
            # If end comes first
            else:
                cursor_x1, cursor_y1 = self.cursor_to_coords(self.highlight_end[0], self.highlight_end[1])
                cursor_x2, _ = self.cursor_to_coords(self.highlight_start[0], self.highlight_start[1])
                draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)
        
        # Not on same row, if start comes first
        elif (self.highlight_start[0] < self.highlight_end[0]):
            cursor_x1, cursor_y1 = self.cursor_to_coords(self.highlight_start[0], self.highlight_start[1])
            cursor_x2, _ = self.cursor_to_coords(self.highlight_start[0], len(self.text[self.highlight_start[0]]))
            draw.text(self.surface, f"1Lb: x, y, width, height: {cursor_x1, cursor_y1, cursor_x2-cursor_x1, self.line_height}", (400,150), 40, cfg.GREEN)
            draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)

            for i in range(self.highlight_start[0]+1, self.highlight_end[0]):
                cursor_x1, cursor_y1 = self.cursor_to_coords(i, 0)
                cursor_x2, _ = self.cursor_to_coords(i, len(self.text[i]))
                draw.text(self.surface, f"{i}SL: x, y, width, height: {cursor_x1, cursor_y1, cursor_x2-cursor_x1, self.line_height}", (600,i*50), 40, cfg.GREEN)
                draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)

            cursor_x1, cursor_y1 = self.cursor_to_coords(self.highlight_end[0], 0)
            cursor_x2, _ = self.cursor_to_coords(self.highlight_end[0], self.highlight_end[1])
            draw.text(self.surface, f"LL: x, y, width, height: {cursor_x1, cursor_y1, cursor_x2-cursor_x1, self.line_height}", (400,200), 40, cfg.GREEN)
            draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)
       
        elif (self.highlight_end[0] < self.highlight_start[0]):
            cursor_x1, cursor_y1 = self.cursor_to_coords(self.highlight_end[0], self.highlight_end[1])
            cursor_x2, _ = self.cursor_to_coords(self.highlight_end[0], len(self.text[self.highlight_end[0]]))
            draw.text(self.surface, f"1Lb: x, y, width, height: {cursor_x1, cursor_y1, cursor_x2-cursor_x1, self.line_height}", (400,150), 40, cfg.GREEN)
            draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)

            for i in range(self.highlight_end[0]+1, self.highlight_start[0]):
                cursor_x1, cursor_y1 = self.cursor_to_coords(i, 0)
                cursor_x2, _ = self.cursor_to_coords(i, len(self.text[i]))
                draw.text(self.surface, f"{i}SL: x, y, width, height: {cursor_x1, cursor_y1, cursor_x2-cursor_x1, self.line_height}", (600,i*50), 40, cfg.GREEN)
                draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)

            cursor_x1, cursor_y1 = self.cursor_to_coords(self.highlight_start[0], 0)
            cursor_x2, _ = self.cursor_to_coords(self.highlight_start[0], self.highlight_start[1])
            draw.text(self.surface, f"LL: x, y, width, height: {cursor_x1, cursor_y1, cursor_x2-cursor_x1, self.line_height}", (400,200), 40, cfg.GREEN)
            draw.rectangle(self.surface, (cursor_x1, cursor_y1), cursor_x2 - cursor_x1, self.line_height, color=cfg.HIGHLIGHT_YELLOW)           
        
    def draw(self, screen):
        try:
            self.surface.fill(self.background_color)
            self.draw_border()
            self.draw_highlight()
            self.draw_text()
            self.draw_cursor()  # Does not draw if inactive

            # Debugging highlight
            draw.text(self.surface, f"Highlight mode: {"on" if self.highlight_mode else "off"}", (100, 400))
            draw.text(self.surface, f"Highlight start: {self.highlight_start[0]}, {self.highlight_start[1]}", (100, 500))
            draw.text(self.surface, f"Highlight end: {self.highlight_end[0]}, {self.highlight_end[1]}", (100, 600))
            draw.text(self.surface, f"Cursor: {self.cursor}", (100, 700))

            screen.blit(self.surface, (self.x, self.y))
        except Exception as e:
            print(f"An error occurred: {e} 😟")
            print(self.text)
            
    def cursor_to_coords(self, row, col):
        cursor_x = self.margin_x + self.font.size(self.text[row][:col])[0]
        cursor_y = self.margin_y + (row * self.line_height)
        return cursor_x, cursor_y
    
    def mouse_to_cursor(self, mouse_pos):
        mousex, mousey = mouse_pos[0], mouse_pos[1]
        cursorx, cursory = 0, 0

        for row, y in enumerate(range(self.margin_y, self.margin_y + (len(self.text) * self.line_height), self.line_height)):
            if mousey >  y:
                cursory = row
                cursorx = 0
                for col in range(0, len(self.text[row])+1, 1):
                    x = self.font.size(self.text[row][:col])[0]
                    if mousex > self.margin_x + x:
                        cursorx = col

        print(f"x and y: {cursorx, cursory}")
        return [cursory, cursorx]


    def delete_highlight(self):
        # Swapping positions to make start always have earlier position within text
        if (self.highlight_start[0] < self.highlight_end[0]):
            pass
        elif (self.highlight_start[0] == self.highlight_end[0]):
            if (self.highlight_start[1] < self.highlight_end[1]):
                pass
            else:
                temp = self.highlight_start.copy()
                self.highlight_start = self.highlight_end.copy()
                self.highlight_end = temp.copy()
        else:
            temp = self.highlight_start.copy()
            self.highlight_start = self.highlight_end.copy()
            self.highlight_end = temp.copy()

        # Splicing text for later
        beginning = self.text[self.highlight_start[0]][:self.highlight_start[1]]
        end = self.text[self.highlight_end[0]][self.highlight_end[1]:]

        # Deleting rows inside of text
        del self.text[self.highlight_start[0]:self.highlight_end[0]+1]
        
        # Splicing text back together
        self.text.insert(self.highlight_start[0], beginning + end)

        print(f"Begin: {beginning}, End: {end}")
        
        # Reseting variables
        self.cursor = self.highlight_start.copy()
        self.highlight_end = self.highlight_start.copy()
        self.highlight_mode = False

    def press_left(self):
        if self.cursor[1] == 0:
            if self.cursor[0] > 0:
                self.cursor[0] -= 1
                self.cursor[1] = len(self.text[self.cursor[0]])
        else:
            self.cursor[1] -= 1
        
        if self.highlight_mode == True:
            self.highlight_end = self.cursor.copy()

    def press_right(self):
        if self.cursor[1] == len(self.text[self.cursor[0]]):
            if self.cursor[0] < len(self.text)-1:
                self.cursor[0] += 1
                self.cursor[1] = 0
        else:
            self.cursor[1] += 1
        
        if self.highlight_mode:
            self.highlight_end = self.cursor.copy()

    def press_up(self):
        if self.cursor[0] > 0:
            if len(self.text[self.cursor[0]-1]) < self.cursor[1]:
                self.cursor[1] = len(self.text[self.cursor[0]-1])
            self.cursor[0] -= 1
        
        if self.highlight_mode:
            self.highlight_end = self.cursor.copy()

    def press_down(self):
        if self.cursor[0] < len(self.text)-1:
            if len(self.text[self.cursor[0]+1]) < self.cursor[1]:
                self.cursor[1] = len(self.text[self.cursor[0]+1])
            self.cursor[0] += 1
        
        if self.highlight_mode:
            self.highlight_end = self.cursor.copy()

    def press_enter(self):
        if self.highlight_start != self.highlight_end:
            self.delete_highlight()

        if self.cursor[1] == len(self.text[self.cursor[0]]):
            self.text.insert(self.cursor[0]+1, "")
        else:
            self.text.insert(self.cursor[0]+1, self.text[self.cursor[0]][self.cursor[1]:])
            self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]]
        self.cursor[0] += 1
        self.cursor[1] = 0

    def press_backspace(self):
        if self.highlight_start != self.highlight_end:
            self.delete_highlight()
        else:
            if self.cursor[1] > 0:
                self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1] - 1] + self.text[self.cursor[0]][self.cursor[1]:]
                self.cursor[1] -= 1
            elif self.cursor[0] > 0:
                # Merge with the previous line
                self.cursor[1] = len(self.text[self.cursor[0] - 1])
                self.text[self.cursor[0] - 1] += self.text[self.cursor[0]]
                del self.text[self.cursor[0]]
                self.cursor[0] -= 1

    def press_tab(self):
        if self.highlight_start != self.highlight_end:
            self.delete_highlight()
        
        self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + "    " + self.text[self.cursor[0]][self.cursor[1]:]
        self.cursor = [self.cursor[0], self.cursor[1] + 4]

    def press_character(self, event):
        if self.highlight_start != self.highlight_end:
            self.delete_highlight()

        self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + event.unicode + self.text[self.cursor[0]][self.cursor[1]:]
        self.cursor = [self.cursor[0], self.cursor[1] + 1]

    def paste(self):
        if self.highlight_start != self.highlight_end:
            self.delete_highlight()

        try:
            self.clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)

            if self.clipboard_text:
                # Splicing the string to insert the text in between
                end_of_text = self.text[self.cursor[0]][self.cursor[1]:]
                self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]]

                # Processing the clipboard text
                for t in pygame.scrap.get_types():
                    #print(f"DEBUG: Clipboard type: {t}\n")
                    pasted_text = self.clipboard_text.decode('utf-8')
                    pasted_text = pasted_text.replace('\x0d', '')
                    pasted_text = pasted_text.replace('\x00', '')

                # Parsing the clipboard text
                for c in pasted_text:
                    if ord(c) == 10:  # New line character or LF (Line Feed)
                        self.text.insert(self.cursor[0]+1, "")
                        self.cursor[0] += 1
                        self.cursor[1] = 0
                    else:
                        self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + c
                        self.cursor[1] += 1

                # Reattaching the remenants of the string
                self.text[self.cursor[0]] = self.text[self.cursor[0]][:self.cursor[1]] + end_of_text

            print(f"this be the text in clip: {self.clipboard_text}")
        except UnicodeDecodeError:
            print("Could not decode clipboard data as UTF-8")
        except Exception as e:
            print(f"An unexpected error occured during paste: {e}")

    def handle_event(self, events):
        # If the surface is not active, just return text
        if self.active == False:
            return self.text
        
        # If the surface is active, handle events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mousex, mousey = mouse_pos[0] - self.x, mouse_pos[1] - self.y
                mouse_pos = [mousex, mousey]
                self.cursor = self.mouse_to_cursor(mouse_pos)
                self.highlight_mode = True
                self.highlight_start = self.cursor.copy()
                self.highlight_end = self.cursor.copy()

            elif event.type == pygame.MOUSEBUTTONUP:
                self.highlight_mode = False

            elif event.type == pygame.MOUSEMOTION:
                if self.highlight_mode:
                    mouse_pos = pygame.mouse.get_pos()
                    mousex, mousey = mouse_pos[0] - self.x, mouse_pos[1] - self.y
                    mouse_pos = [mousex, mousey]
                    self.cursor = self.mouse_to_cursor(mouse_pos)
                    self.highlight_end = self.cursor

            elif event.type == pygame.KEYDOWN:
                if event.mod & pygame.KMOD_CTRL: # Check if Control key is held down
                    if event.key == pygame.K_UP:
                        pass
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_c:
                        pass
                    if event.key == pygame.K_v:
                        print("pasting that ho")
                        self.paste()
                    if event.key == pygame.K_x:
                        pass
                elif event.key == pygame.K_ESCAPE:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.press_backspace()
                elif event.key == pygame.K_RETURN:
                    self.press_enter()
                elif event.key == pygame.K_TAB:
                    self.press_tab()
                elif event.key == pygame.K_UP:
                    self.press_up()
                elif event.key == pygame.K_DOWN:
                    self.press_down()
                elif event.key == pygame.K_LEFT:
                    self.press_left()
                elif event.key == pygame.K_RIGHT:
                    self.press_right()
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.highlight_mode = True
                    self.highlight_start = self.cursor.copy()
                    self.highlight_end = self.cursor.copy()
                else:
                    self.press_character(event)
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.highlight_mode = False

        # Return text
        return self.text