
import pygame as pg

class Block:
    def __init__(self, rect, color=(155,155,155)):
        self.rect = pg.Rect(rect)
        self.image = pg.Surface([self.rect.width, self.rect.height]).convert()
        self.image.fill(color)
        
    def render(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self):
        pass
