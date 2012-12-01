'''
Created on Nov 16, 2012

@author: robert
'''

import pygame
import game

g = game.Game()
while True:
    g.clock.tick(61)
    g.update()
    g.draw()
    pygame.display.flip()
    #pygame.display.update()