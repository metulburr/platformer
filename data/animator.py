
import pygame as pg

class Animator:
    def __init__(self, sheet, frames, rect, fps=5):
        self.rect = pg.Rect(rect)
        self.image = None
        self.spritesheet = pg.image.load(sheet).convert_alpha()
        self.frames = []
        self.frame = 0
        self.timer = 0.0
        self.fps = fps
        self.done = False
        self.get_images_equal_size(*frames)

    def get_images_equal_size(self, num_img_row, num_img_col, empty_frames=0):
        '''all images on spritesheet are of equal width and height'''
        for col in range(num_img_col):
            for row in range(num_img_row):
                loc = ((self.rect.width * row, self.rect.height * col), self.rect.size)
                self.frames.append(self.spritesheet.subsurface(loc))
        if empty_frames:
            for empty_frame in range(empty_frames):
                self.frames.pop()
        self.make_image()
        
    def make_image(self):
        if pg.time.get_ticks()-self.timer > 1000/self.fps:
            try:
                self.frame += 1
                self.image = self.frames[self.frame]
                self.timer = pg.time.get_ticks()
            except IndexError:
                self.done = True
        if not self.image:
            self.image = self.frames[self.frame]

    def update(self, surf):
        self.make_image()
        surf.blit(self.image, self.rect)

if __name__ == "__main__":
    class Control:
        def __init__(self):
            self.screen = pg.display.set_mode((256,256))
            pg.display.set_caption('Press Space Bar')
            pg.init()
            self.Clock = pg.time.Clock()
            self.done = False
            self.animations = []
            
        def event_loop(self):
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    self.done = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.animations.append(
                            Animator('../resources/graphics/darthvader.png', (4,4), (0,0,32,48))
                        )
                        
        def run(self):
            while not self.done:
                self.event_loop()
                self.screen.fill(0)
                for ani in self.animations[:]:
                    ani.update(self.screen)
                    if ani.done:
                        self.animations.remove(ani)
                pg.display.update()
                self.Clock.tick(60)


    app = Control()
    app.run()
    pg.quit()
