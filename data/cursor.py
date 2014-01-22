
import pygame as pg

class Cursor:
    def __init__(self):
        pass
        
    def set_as_arrow(self):
        arrow = (
              "XX                      ",
              "XXX                     ",
              "XXXX                    ",
              "XX.XX                   ",
              "XX..XX                  ",
              "XX...XX                 ",
              "XX....XX                ",
              "XX.....XX               ",
              "XX......XX              ",
              "XX.......XX             ",
              "XX........XX            ",
              "XX........XXX           ",
              "XX......XXXXX           ",
              "XX.XXX..XX              ",
              "XXXX XX..XX             ",
              "XX   XX..XX             ",
              "     XX..XX             ",
              "      XX..XX            ",
              "      XX..XX            ",
              "       XXXX             ",
              "       XX               ",
              "                        ",
              "                        ",
              "                        ")
        datatuple, masktuple = pg.cursors.compile(arrow,
            black='.', white='X', xor='o' )
        pg.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )
        
    def set_as_box(self):
        box = (
              "XXXXXXXXXXXXXXXXXXXXXXXX",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "X                      X",
              "XXXXXXXXXXXXXXXXXXXXXXXX")
              
        datatuple, masktuple = pg.cursors.compile(box,
            black='.', white='X', xor='o' )
        pg.mouse.set_cursor( (24,24), (12,12), datatuple, masktuple )
        
        
    def set_as_lowrect(self):
        lowrect = (
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "XXXXXXXXXXXXXXXXXXXXXXXX",
            "X                      X",
            "X                      X",
            "X                      X",
            "X                      X",
            "X                      X",
            "X                      X",
            "X                      X",
            "XXXXXXXXXXXXXXXXXXXXXXXX")
              
        datatuple, masktuple = pg.cursors.compile(lowrect,
            black='.', white='X', xor='o' )
        pg.mouse.set_cursor( (24,24), (12,20), datatuple, masktuple )
