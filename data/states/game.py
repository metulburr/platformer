

import pygame as pg
from .. import tools
import os
import random
from .. import tmx

class Enemy(pg.sprite.Sprite):
    #image = pg.image.load('enemy.png')
    image = tools.Image.load('enemy.png')
    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        self.rect = pg.rect.Rect(location, self.image.get_size())
        self.direction = 1

    def update(self, dt, game):
        self.rect.x += self.direction * 100 * dt
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            self.direction *= -1
            break
        if self.rect.colliderect(game.player.rect):
            game.player.is_dead = True

class Bullet(pg.sprite.Sprite):
    #image = pg.image.load('bullet.png')
    image = tools.Image.load('bullet.png')
    def __init__(self, location, direction, *groups):
        super(Bullet, self).__init__(*groups)
        self.rect = pg.rect.Rect(location, self.image.get_size())
        self.direction = direction
        self.lifespan = 1

    def update(self, dt, game):
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return
        self.rect.x += self.direction * 400 * dt

        if pg.sprite.spritecollide(self, game.enemies, True):
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        #self.image = pg.image.load('player-right.png')
        self.image = tools.Image.load('player-right.png')
        self.right_image = self.image
        #self.left_image = pg.image.load('player-left.png')
        self.left_image = tools.Image.load('player-left.png')
        self.rect = pg.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0
        self.is_dead = False
        self.direction = 1
        self.gun_cooldown = 0

    def update(self, dt, game):
        last = self.rect.copy()

        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rect.x -= 300 * dt
            self.image = self.left_image
            self.direction = -1
        if key[pg.K_RIGHT]:
            self.rect.x += 300 * dt
            self.image = self.right_image
            self.direction = 1

        if key[pg.K_LSHIFT] and not self.gun_cooldown:
            if self.direction > 0:
                Bullet(self.rect.midright, 1, game.sprites)
            else:
                Bullet(self.rect.midleft, -1, game.sprites)
            self.gun_cooldown = 1

        self.gun_cooldown = max(0, self.gun_cooldown - dt)

        if self.resting and key[pg.K_SPACE]:
            self.dy = -500
        self.dy = min(400, self.dy + 40)

        self.rect.y += self.dy * dt

        new = self.rect
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            blockers = cell['blockers']
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

        game.tilemap.set_focus(new.x, new.y)

class Game(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.overlay_bg = pg.Surface((screen_rect.width, screen_rect.height))
        self.overlay_bg.fill(0)
        self.overlay_bg.set_alpha(200)
        self.bg_color = (255,255,255)

        self.timer = 0

        self.overlay = pg.Surface((screen_rect.width, screen_rect.height))
        self.overlay.fill(0)
        self.overlay.set_alpha(200)
        
        self.sprites = tmx.SpriteLayer()
        self.tilemap = tools.TMX.load('test.tmx', self.screen_rect.size)
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        
        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)
        
        
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == self.keybinding['back']:
                self.button_click.sound.play()
                self.done = True
                self.next = 'MENU'
                
        #elif event.type == self.bg_music.track_end:
        #    self.bg_music.track = (self.bg_music.track+1) % len(self.bg_music.tracks)
        #    pg.mixer.music.load(self.bg_music.tracks[self.bg_music.track]) 
        #    pg.mixer.music.play()
                    
    def update(self, now, keys, dt):
        if pg.time.get_ticks()-self.timer > 1000:
            self.timer = pg.time.get_ticks()
        self.tilemap.update(dt / 1000., self)
        if self.player.is_dead:
            print('YOU DIED')
            self.quit = True
        
    def render(self, screen):
        screen.fill((self.bg_color))
        self.tilemap.draw(screen)


    def cleanup(self):
        pass
        
    def entry(self):
        pass
