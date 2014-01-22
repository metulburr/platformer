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

    def movementX(self, keys, blocks):
        frame_speed = 0
        if keys[pg.K_d]:
            frame_speed += self.speed
        if keys[pg.K_a]:
            frame_speed -= self.speed
        self.rect.x += frame_speed
        collide = pg.sprite.spritecollideany(self, blocks)
        if collide:
            if frame_speed > 0:
                self.rect.right = collide.rect.left
            else:
                self.rect.left = collide.rect.right

    def update(self, keys, blocks):
        self.movementX(keys, blocks)
        self.handle_collision(blocks)
        self.rect.clamp_ip(self.screen_rect)

    def check_ground(self, blocks):
        self.rect.move_ip(0,1)
        if not pg.sprite.spritecollideany(self, blocks):
            self.in_air = True
        self.rect.move_ip(0,-1)

    def handle_collision(self, blocks):
        self.check_ground(blocks)
        if self.in_air:
            self.y_vel += self.grav
            self.rect.y += self.y_vel
            collide = pg.sprite.spritecollideany(self, blocks)
            if collide:
                if self.y_vel > 0:
                    self.rect.bottom = collide.rect.top
                else:
                    self.rect.top = collide.rect.bottom
                self.in_air = False
                self.y_vel = 0

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def jump(self):
        if not self.in_air:
            self.y_vel = -self.jump_power
            self.in_air = True
