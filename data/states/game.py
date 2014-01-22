
import pygame as pg
from .. import tools, player, block
import random

class Game(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.score_text, self.score_rect = self.make_text("Game State",
            (255,255,255), (screen_rect.centerx,100), 30)
        self.pause_text, self.pause_rect = self.make_text("PAUSED",
            (255,255,255), screen_rect.center, 50)
        
        #game specific content
        self.bg_color = (0,0,0)
        self.pause = False
        
        self.player = player.Player(self.screen_rect)
        self.blocks = []
        self.blocks.append(block.Block((100,550,50,25)))
        self.blocks.append(block.Block((200,550,50,25)))
    
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'
            elif event.key == pg.K_p:
                self.pause = not self.pause
        self.player.get_event(event, keys)
        #elif event.type == self.background_music.track_end:
        #    self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
        #    pg.mixer.music.load(self.background_music.tracks[self.background_music.track]) 
        #    pg.mixer.music.play()

    def update(self, now, keys):
        if not self.pause:
            self.player.update(keys, self.blocks)
            for block in self.blocks:
                block.update()
        else:
            self.pause_text, self.pause_rect = self.make_text("PAUSED",
                (255,255,255), self.screen_rect.center, 50)

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.score_text, self.score_rect)
        self.player.render(screen)
        for block in self.blocks:
            block.render(screen)
        if self.pause:
            screen.blit(self.pause_text, self.pause_rect)
        
    def make_text(self,message,color,center,size):
        font = tools.Font.load('arial.ttf', size)
        text = font.render(message,True,color)
        rect = text.get_rect(center=center)
        return text,rect
        
    def adjust_score(self, hit_side):
        if hit_side == -1:
            self.score[1] += 1
        elif hit_side == 1:
            self.score[0] += 1
            
    def const_event(self, keys):
        pass
            
    def cleanup(self):
        self.mouse_cursor.set_as_arrow()
        #pg.mixer.music.stop()
        #self.background_music.setup(self.background_music_volume)
        
    def entry(self):
        pass#self.mouse_cursor.set_as_lowrect()
        #pg.mixer.music.play()
