'''
Created on Nov 27, 2012

@author: robert
'''

import pygame

class Player(object):
    def __init__(self, x, y):
        self.img = pygame.image.load("../assets/img/player.png").convert()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.velx = 0
        self.vely = 0
        self.accelx = 0
        self.accely = 0
    
    def update(self):
        self.rect.move_ip(self.velx * (16.0 / 1000.0), self.vely * (16.0 / 1000.0))

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        
if __name__ == "__main__":
    import main