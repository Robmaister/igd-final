#!/usr/bin/env python
'''
Created on Nov 16, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame
import game

g = game.Game()
while True:
    g.clock.tick(61)
    g.update()
    g.draw()
    pygame.display.flip()
    #pygame.display.replay_step()