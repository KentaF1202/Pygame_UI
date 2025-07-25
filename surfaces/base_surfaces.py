# Module Imports
import pygame

# File Imports
import configs as cfg
from tools import shapes
from tools.collision import collision

# Pygame Initialization
pygame.init()

class UIElement:
    def __init__(self, rect: tuple, parent: "UIElement" =None) -> None:
        # Rectangle parameters
        if not isinstance(rect, (tuple, list)) or len(rect) != 4:
            raise ValueError("Rect must be a tuple or list with four elements (x, y, width, height).")
        self._x, self._y, self._width, self._height = rect

        # Parent parameter
        if parent is not None and not isinstance(parent, UIElement):
            raise ValueError("Parent must be an instance of UIElement or None.")
        self._parent = parent

        # Child parameters
        self._children = []

        # States
        self._interactable = False
        self._visible = True
        self._hovered = False

    @property
    def parent(self):
        return self._parent
    
    
    def draw(self, surface: pygame.Surface) -> None:
        if not isinstance(surface, pygame.Surface):
            raise ValueError("Surface must be an instance of pygame.Surface.")
        if self._visible:
            pygame.draw.rect(surface, (255, 255, 255), (self._x, self._y, self._width, self._height))

