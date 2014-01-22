
import pygame as pg

class Player:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.width = 50
        self.height = 75
        self.image = pg.Surface([self.width, self.height])
        self.image.fill((255,255,255))
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
        
    def update(self, keys):
        self.rect.clamp_ip(self.screen_rect)
        self.jump_update()
        print(self.screen_rect)
            
        if keys[pg.K_d]:
            self.rect.x += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        
    def render(self, screen):
        screen.blit(self.image, self.rect)
                
    def jump_update(self):
        mouse = pg.mouse.get_pos()
        if self.in_air:
            self.y_vel += self.grav
            self.rect.y += self.y_vel
            if self.collisionY(mouse):
                self.in_air = False
        else:
            self.y_vel = 0
        
        #allow fall if mouse moves from under rect
        if not self.rect.collidepoint(mouse) and self.rect.y < self.screen_rect.height - self.height:
            self.in_air = True
                
    def collisionY(self, mouse):
        if self.rect.y >= self.screen_rect.height - self.height:
            return True
        if self.rect.collidepoint(mouse):
            if self.rect.y >= mouse[0]:
                return True
            else:
                return False
        
    def jump(self):
        if not self.in_air:
            self.y_vel = -self.jump_power
            self.in_air = True
