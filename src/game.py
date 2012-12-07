#!/usr/bin/env python
'''
Created on Nov 27, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame, sys

import player, level, camera, replay

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.prevlives = []
        self.currentlife = [replay.InputState(pygame.key.get_pressed())]
        self.prevlifeindex = 0
        self.prevlifeframe = 0
        self.level = level.Level("../assets/lvl/level0.lvl")
        self.player = player.Player(self.level.spawn_x, self.level.spawn_y)
        self.camera = camera.Camera(self.screen, self.level.map_surface.get_rect(), pygame.rect.Rect((0, 0), (800, 600)))
        self.background = camera.ParallaxBackground(self.camera, 0.4, "../assets/img/background.png")
        self.level_count = 0
        
    def update(self):
        pressedkeys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
                if e.key == pygame.K_k:
                    self.die()
                if e.key == pygame.K_r:
                    self.prevlifeframe = 0
                    self.prevlifeindex = 0
                    self.prevlives = []
                    self.currentlife = [replay.InputState(pygame.key.get_pressed())]
                    self.player.respawn()
                    for ent in self.level.entities:
                        ent.reset()
            elif e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.USEREVENT + 2: #level win
                #TODO cleaner level changing, at the very least an array of levels...
                if self.level_count > 0:
                    sys.exit()
                else:
                    self.level = level.Level("../assets/lvl/level1.lvl")
                    self.prevlifeframe = 0
                    self.prevlifeindex = 0
                    self.prevlives = []
                    self.currentlife = [replay.InputState(pygame.key.get_pressed())]
                    self.camera.bounds = self.level.map_surface.get_rect()
                    self.player.spawn_x = self.level.spawn_x
                    self.player.spawn_y = self.level.spawn_y
                    self.player.respawn()
                    self.level_count += 1
        
        #store current life's state.
        if pressedkeys != self.currentlife[-1].keys:
            self.currentlife.append(replay.InputState(pressedkeys))
        else:
            self.currentlife[-1].frames += 1

        for life in self.prevlives:
            life.replay_step(self.level.colliders)
            
        for ent in self.level.entities:
            ent.update()
            
        self.player.update(pressedkeys, self.level.colliders)
        self.camera.center_at(self.player.rect)
        self.camera.update()
        
        #call death code only if current player dies. Replays will simply stop working and disappear.
        if self.player.dead:
            self.die()
        
    def draw(self):
        self.screen.fill((17, 25, 27))
        
        self.background.draw(self.screen)
        self.level.draw(self.camera)
        
        for ent in self.level.entities:
            ent.draw(self.camera)
            
        self.player.draw(self.camera)
        for life in self.prevlives:
            life.player.draw(self.camera)
            
    def die(self):
        self.prevlives.append(replay.PreviousLife(self.currentlife, player.Player(self.level.spawn_x, self.level.spawn_y)))
        self.currentlife = [replay.InputState(pygame.key.get_pressed())]
        self.player.respawn()
        for life in self.prevlives:
            life.replay_reset()
        for ent in self.level.entities:
            ent.reset()
            
if __name__ == "__main__":
    import main