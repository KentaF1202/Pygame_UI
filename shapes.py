# Module Imports
import pygame
import math

# File Imports
import configs as cfg

# Pygame Initialization
pygame.init()

#Base Shapes
def draw_text(surface, text: str, coordinates, font_size = 20, color = cfg.VS_OFF_WHITE, orientation="left"):
    font = pygame.font.SysFont("ubuntu", font_size) 
    text_surface = font.render(text, True, color)
    x, y = coordinates
    new_coordinates = (x, y)
    if orientation == "left":
        text_rectangle = surface.get_rect(topleft=(new_coordinates))
    else:
        text_rectangle = surface.get_rect(center=(new_coordinates))

    surface.blit(text_surface, text_rectangle)

def draw_rectangle(surface, coordinates, rectangle_width, rectangle_height, border=0, color= cfg.BLACK):
    rect_object = (coordinates[0], coordinates[1], rectangle_width, rectangle_width)
    pygame.draw.rect(surface, color, rect_object, border)


def draw_line(surface, start_pos, end_pos, color = cfg.BLACK):
    pygame.draw.line(surface, color, start_pos, end_pos, cfg.line_width)


# Advanced shapes
def draw_node(surface, value, coordinates, rectangle_width, rectangle_height, error = False, highlight = False):
    if(highlight):
        color = cfg.HIGHLIGHT_YELLOW
    elif(error):
        color = cfg.HIGHLIGHT_RED
    else:
        color = cfg.WHITE

    draw_rectangle(surface, coordinates, rectangle_width, rectangle_height, 0, color)
    draw_rectangle(surface, coordinates, rectangle_width, rectangle_height, 2, cfg.BLACK)
    draw_text(surface, f"{value}", (coordinates[0] + cfg.text_offset, coordinates[1] + cfg.text_offset))

def draw_arrow_bidirect(surface, start_pos, end_pos, color=cfg.BLACK):
    #Draw the line
    draw_line(surface, start_pos, end_pos, color)

    #Find arrow head points
    angle1 = math.atan2((end_pos[1]-start_pos[1]),(end_pos[0]-start_pos[0]))
    xa = start_pos[0]+(cfg.arrow_head_distance*math.cos(angle1+math.pi/4))
    ya = start_pos[1] + (cfg.arrow_head_distance*math.sin(angle1+math.pi/4))
    a_pos = (xa, ya)

    xb = start_pos[0]+(cfg.arrow_head_distance*math.cos(angle1-math.pi/4))
    yb = start_pos[1] + (cfg.arrow_head_distance*math.sin(angle1-math.pi/4))
    b_pos = (xb, yb)

    angle2 = math.atan2((start_pos[1]-end_pos[1]),(start_pos[0]-end_pos[0]))
    xc = end_pos[0]+(cfg.arrow_head_distance*math.cos(angle2+math.pi/4))
    yc = end_pos[1] + (cfg.arrow_head_distance*math.sin(angle2+math.pi/4))
    c_pos = (xc, yc)

    xd = end_pos[0]+(cfg.arrow_head_distance*math.cos(angle2-math.pi/4))
    yd = end_pos[1] + (cfg.arrow_head_distance*math.sin(angle2-math.pi/4))
    d_pos = (xd, yd)

    #Draw the arrow head
    draw_line(surface, start_pos, a_pos, color)
    draw_line(surface, start_pos, b_pos, color)

    draw_line(surface, end_pos, c_pos, color)
    draw_line(surface, end_pos, d_pos, color)


def draw_arrow(surface, start_pos, end_pos, color=cfg.BLACK):
    #Draw the line
    draw_line(surface, start_pos, end_pos, color)

    #Find arrow head points
    angle2 = math.atan2((start_pos[1]-end_pos[1]),(start_pos[0]-end_pos[0]))
    xc = end_pos[0]+(cfg.arrow_head_distance*math.cos(angle2+math.pi/4))
    yc = end_pos[1] + (cfg.arrow_head_distance*math.sin(angle2+math.pi/4))
    c_pos = (xc, yc)

    xd = end_pos[0]+(cfg.arrow_head_distance*math.cos(angle2-math.pi/4))
    yd = end_pos[1] + (cfg.arrow_head_distance*math.sin(angle2-math.pi/4))
    d_pos = (xd, yd)
    
    draw_line(surface, end_pos, c_pos, color)
    draw_line(surface, end_pos, d_pos, color)