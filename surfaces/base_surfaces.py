# Module Imports
import pygame

# File Imports
import configs as cfg
from tools import shapes
from tools.collision import collision

# Pygame Initialization
pygame.init()

class UIElement:
    def __init__(self, rect: tuple, color: tuple = cfg.BLACK, parent: "UIElement" =None) -> None:
        # Rectangle parameters
        if not isinstance(rect, (tuple, list)) or len(rect) != 4:
            raise ValueError("Rect must be a tuple or list with four elements (x, y, width, height).")
        self._x, self._y, self._width, self._height = rect
        self.color = color
        self.surface = pygame.Surface((self._width, self._height))
        self.surface.fill(self.color)

        # Parent parameters
        self._parent = None
        if parent is not None:
            self._parent = parent
            self._parent.add_children(self)

        # Child parameters
        self._children = []

        # States
        self._interactable = False
        self._visible = True
        self._hovered = False

    @property
    def parent(self) -> "UIElement":
        return self._parent
    
    @parent.setter
    def parent(self, parent: "UIElement") -> None:
        if not isinstance(parent, UIElement):
            raise ValueError("Parent must be an instance of UIElement.")
        self._parent = parent
        self._parent.add_children(self)
    
    @property
    def children(self) -> list:
        return list(self._children)
    
    def add_children(self, child: "UIElement") -> None:
        if not isinstance(child, UIElement):
            raise ValueError("Child must be an instance of UIElement.")
        self._children.append(child)

    def remove_child(self, child_to_remove: "UIElement") -> None:
        if not isinstance(child_to_remove, UIElement):
            raise ValueError("Child to remove must be an instance of UIElement.")
        if child_to_remove not in self._children:
            raise ValueError("Child is not within the list of children.")
        self._children.remove(child_to_remove)

    def draw(self, surface: pygame.Surface = None) -> None:
        if surface is None:
            surface = self._parent.surface
        if not isinstance(surface, pygame.Surface):
            raise ValueError("Surface must be an instance of pygame.Surface.")
        if self._visible:
            surface.blit(self.surface,(self._x, self._y))
