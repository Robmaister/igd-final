'''
Created on Nov 16, 2012

@author: robert
'''

import pygame, sys

pygame.init()
screen = pygame.display.set_mode((800, 600))

while True:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                sys.exit()
                
    pygame.display.flip()
    pygame.display.update()