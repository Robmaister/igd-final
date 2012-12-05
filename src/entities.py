'''
Created on Dec 3, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame

class Button(object):
    
    def __init__(self, x, y):
        self.img = pygame.image.load("../assets/img/player.png").convert()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.pressed = False
        self.connected = []
        
    def get_rect(self):
        return self.rect
    
    def press(self):
        self.pressed = not self.pressed
        if self.pressed:
            for c in self.connected:
                c.on_pressed()
        else:
            for c in self.connected:
                c.on_unpressed()
                
                
class SlidingBlock(object):
    
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        
    def get_rect(self):
        return self.rect
        
    def on_pressed(self):
        pass
    
    def on_unpressed(self):
        pass
    
class FloorButton(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connected = []
        
    def get_rect(self):
        return self.rect
    
if __name__ == "__main__":
    import main