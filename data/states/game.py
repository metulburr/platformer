import pygame as pg
from .. import tools, player, block, powerup, TMXLoader
import random
from xml import sax



class Game(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        #self.score_text, self.score_rect = self.make_text("",
        #    (255,255,255), (screen_rect.centerx,100), 30)
        self.pause_text, self.pause_rect = self.make_text("PAUSED",
            (255,255,255), screen_rect.center, 50)

        #game specific content
        self.bg_color = (0,0,0)
        self.pause = False

        
        self.player = player.Player(self.screen_rect)
        self.reset_level()
        
        self.parser = sax.make_parser()
        self.tmx = TMXLoader.TMXHandler(debug=True)
        self.parser.setContentHandler(self.tmx)
        self.parser.parse(tools.TMX.load('test2.tmx'))
        
    def reset_level(self):
        self.blocks = []
        step_top = ((self.screen_rect.bottom - 20) - 75) - 25#bottom screen - floor - player height - platform hieght
        self.blocks.append(block.Block((100,step_top-75,50,25)))
        self.blocks.append(block.Block((200,step_top,50,25)))
        self.blocks.append(block.Block((300,step_top-150,50,25)))
        self.blocks.append(block.Block((self.screen_rect.right-50,step_top+65,50,25)))
        self.blocks.append(block.Block((0,580,800,20)))
        
        self.powerups = []

        self.powerups.append(powerup.PowerUp((125,step_top-10, 15,15)))
        self.powerups.append(powerup.PowerUp((425,step_top+10, 15,15)))
        self.powerups.append(powerup.PowerUp((500,step_top+10, 15,15)))
        self.powerups.append(powerup.PowerUp((580,step_top+10, 15,15)))
        self.powerups.append(powerup.PowerUp((self.screen_rect.right-30,step_top-25, 15,15),5))
        self.powerups.append(powerup.PowerUp((325,step_top-225,15,15)))
        
        self.score_text, self.score_rect = self.make_text("",
            (255,255,255), (self.screen_rect.centerx,100), 30)
        self.player.reset()
        self.player.reset_position()


    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.button_click.sound.play()
                self.done = True
                self.next = 'MENU'
            elif event.key == pg.K_p:
                self.pause = not self.pause
        self.player.get_event(event, keys)

    def update(self, now, keys):
        if not self.pause:
            self.player.update(keys, self.blocks)
            for block in self.blocks:
                block.update()
            for up in self.powerups[:]:
                remove = up.update(self.player)
                if remove:
                    #print('jump power increased to {}'.format(self.player.jump_power))
                    self.powerups.remove(up)
        else:
            self.pause_text, self.pause_rect = self.make_text("PAUSED",
                (255,255,255), self.screen_rect.center, 50)

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.tmx.image, (0,0))
        screen.blit(self.score_text, self.score_rect)
        self.player.render(screen)
        for block in self.blocks:
            block.render(screen)
        for up in self.powerups:
            up.render(screen)
        if not self.powerups:
            self.score_text, self.score_rect = self.make_text("Complete",
                (255,255,255), (self.screen_rect.centerx,100), 30)
        if self.pause:
            screen.blit(self.pause_text, self.pause_rect)

    def make_text(self,message,color,center,size):
        font = tools.Font.load('impact.ttf', size)
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
        self.reset_level()

    def entry(self):
        pass#
