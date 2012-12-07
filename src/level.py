#!/usr/bin/env python
'''
Created on Nov 27, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame
import entities

class Tile(object):
    def __init__(self, rect):
        self.rect = rect
        self.name = ""
        
    def get_rect(self):
        return self.rect

class Level(object):
    def __init__(self, path):
        self.tileset = pygame.image.load("../assets/img/tileset.png").convert_alpha()
        self.spawn_x = 0
        self.spawn_y = 0
        
        lines = [line.rstrip() for line in open(path)]
        
        startmapdata = 0
        mapsize_x = 0
        mapsize_y = 0
        
        self.entities = []
        self.colliders = []
        
        for i,line in enumerate(lines):
            lineinfo = line.split(' ')
            if lineinfo[0] == "spawn":
                self.spawn_x = int(lineinfo[1])
                self.spawn_y = int(lineinfo[2])
            elif lineinfo[0] == "button":
                btn = entities.Button(int(lineinfo[1]), int(lineinfo[2]), lineinfo[3])
                for name in lineinfo[4:]:
                    btn.connected.append(next(e for e in self.entities if e.name == name))
                self.entities.append(btn)
            elif lineinfo[0] == "slidingblock":
                self.entities.append(entities.SlidingBlock(int(lineinfo[1]), int(lineinfo[2]), lineinfo[3]))
            elif lineinfo[0] == "floorbutton":
                btn = entities.FloorButton(int(lineinfo[1]), int(lineinfo[2]), lineinfo[3])
                for name in lineinfo[4:]:
                    btn.connected.append(next(e for e in self.entities if e.name == name))
            elif lineinfo[0] == "spike":
                self.entities.append(entities.Spike(int(lineinfo[1]), int(lineinfo[2]), int(lineinfo[3]), int(lineinfo[4]), lineinfo[5]))
            elif lineinfo[0] == "levelend":
                self.entities.append(entities.LevelEnd(int(lineinfo[1]), int(lineinfo[2]), lineinfo[3]))
            elif lineinfo[0] == "mapinfo":
                mapsize_x = int(lineinfo[1])
                mapsize_y = int(lineinfo[2])
                startmapdata = i + 1
                break
            
        self.map_surface = pygame.Surface((mapsize_x * 32, mapsize_y * 32), pygame.SRCALPHA)
        
        for i,row in enumerate(lines[startmapdata:]):
            for j,col in enumerate(row):
                if col == 'n': #blank tiles
                    continue
                elif col.isdigit() or col in ('a', 'b', 'c', 'd', 'e', 'f'):
                    num=int(col, 16)
                    if 0 <= num <= 15:
                        tile_rect = pygame.rect.Rect(((num % 4) * 32, (num / 4) * 32), (32, 32))
                        self.map_surface.blit(self.tileset, (j * 32, i * 32), tile_rect)
                        self.colliders.append(Tile(pygame.rect.Rect((j * 32, i * 32), (32, 32))))
                elif col == 'o': #special 'o' character - visible but not collidable. Gives me more room for not having a physics broadphase.
                    self.map_surface.blit(self.tileset, (j * 32, i * 32), pygame.rect.Rect(0, 0, 32, 32))
        
        self.colliders = self.colliders + self.entities #include entities as colliders
    
    def draw(self, screen):
        screen.blit(self.map_surface, (0,0))
        
if __name__ == "__main__":
    import main