import pygame as pg
from . import shared

class PowerUp(shared.Shared):
    def __init__(self, rect, jump=1):
        shared.Shared.__init__(self)
        self.jump_inc = jump
        self.rect = pg.Rect(rect)
        self.image = pg.Surface([self.rect.width, self.rect.height])
        self.image.fill((255,255,0))

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.jump_power_add(self.jump_inc)
            return True

    def render(self, screen):
        screen.blit(self.image, self.rect)
