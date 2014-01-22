
import pygame as pg

class Player:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.width = 50
        self.height = 75
        self.image = pg.Surface([self.width, self.height])
        self.image.fill((0,0,255))
        starting_loc = (0, screen_rect.height)
        self.rect = self.image.get_rect(bottomleft=starting_loc)
        self.speed = 5
        self.grav = .5
        self.in_air = False
        self.y_vel = 0
        self.jump_power = 10
        
    def get_event(self, event, keys):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.jump()
                
    def movementX(self, keys):
        if keys[pg.K_d]:
            self.rect.x += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        
    def update(self, keys, blocks):
        self.rect.clamp_ip(self.screen_rect)
        self.movementX(keys)
        self.handle_collision(blocks)
        
    def handle_collision(self, blocks):
        for block in blocks:
            if not self.rect.colliderect(block) and self.rect.bottom < self.screen_rect.bottom:
                self.in_air = True
                break
        if self.in_air:
            self.y_vel += self.grav
            self.rect.y += self.y_vel
            if self.rect.bottom >= self.screen_rect.bottom:
                self.in_air = False
            for block in blocks:
                if self.rect.colliderect(block):
                    if self.rect.bottom >= block.rect.top:
                        self.in_air = False
                        break
        else:
            self.y_vel = 0

        
    def render(self, screen):
        screen.blit(self.image, self.rect)
        
    def jump(self):
        if not self.in_air:
            self.y_vel = -self.jump_power
            self.in_air = True
