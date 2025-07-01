# Module Imports
import pygame

# Pygame Initialization
pygame.init()

# Screen Variables
WINDOW_OFFSET_X = 0
WINDOW_OFFSET_Y = 0

# Refresh Rate
FPS = 60  # Set FPS to maximum possible value

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Visual Studio Colors
VS_GREY = (31, 31, 31)
VS_LIGHT_GREY = (67, 67, 67)
VS_BLACK = (24, 24, 24)
VS_OFF_WHITE = (172, 172, 172)
VS_LIGHTBLUE = (61, 144, 228)

# Highlight Colors
HIGHLIGHT_YELLOW = (255, 255, 0, 100)
HIGHLIGHT_RED = (255, 0, 0, 100)

# Fonts
font_size = 100
font_type = "Ubuntu"
font = pygame.font.SysFont(font_type, font_size)
text_font_size = 24
text_font_type = "Ubuntu"
text_font = pygame.font.SysFont(text_font_type, text_font_size)

# Text Editor Sizings
text_margin_x = 10
text_margin_y = 10
text_line_spacing = 5

# Button sizing
button_width = 50
button_height = 50 
button_spacing = 60 
button_margin = 15

# Shape Dimensions
line_width = 3
arrow_head_distance = 15