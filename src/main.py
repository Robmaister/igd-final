'''
Created on Nov 16, 2012

@author: robert
'''

import pygame, sys
import game

g = game.Game()
while True:
    g.clock.tick()
    g.update()
    g.draw()
    pygame.display.flip()
    pygame.display.update()