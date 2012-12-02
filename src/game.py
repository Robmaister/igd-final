#!/usr/bin/env python
'''
Created on Nov 27, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame, sys

import player, level, replay

class Game(object):
    def __init__(self):
        pygame.init()
        self.lastUpdateTime = pygame.time.get_ticks()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.prevlives = []
        self.currentlife = [replay.InputState(pygame.key.get_pressed())]
        self.prevlifeindex = 0
        self.prevlifeframe = 0
        self.level = level.Level("../assets/lvl/level0.lvl")
        self.player = player.Player(self.level.spawn_x, self.level.spawn_y)
        
    def update(self):
        pressedkeys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
                if e.key == pygame.K_k:
                    self.die()
        
        #store current life's state.
        if pressedkeys != self.currentlife[-1].keys:
            self.currentlife.append(replay.InputState(pressedkeys))
        else:
            self.currentlife[-1].frames += 1

        for life in self.prevlives:
            life.replay_step()
            
        self.player.update(pressedkeys, self.level.phys_rects)
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        for life in self.prevlives:
            life.player.draw(self.screen)
            
    def die(self):
        self.prevlives.append(replay.PreviousLife(self.currentlife))
        self.currentlife = [replay.InputState(pygame.key.get_pressed())]
        self.player.rect.left = 0
        self.player.rect.top = 0
        for life in self.prevlives:
            life.replay_reset()
            
if __name__ == "__main__":
    import main