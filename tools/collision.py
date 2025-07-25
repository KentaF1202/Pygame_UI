# Collision Function
def collision(mousepos, rect):
    mousex, mousey = mousepos[0], mousepos[1]
    x, y, width, height = rect
    if (mousex > x and mousex < x+width):
        if (mousey > y and mousey < y+height):
            return True
    return False