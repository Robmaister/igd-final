#!/usr/bin/env python
'''
Created on Nov 27, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame

class Tile(object):
    def __init__(self, rect):
        self.rect = rect
        
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
        
        for i,line in enumerate(lines):
            lineinfo = line.split(' ')
            if lineinfo[0] == "spawn":
                self.spawn_x = int(lineinfo[1])
                self.spawn_y = int(lineinfo[2])
            elif lineinfo[0] == "mapinfo":
                mapsize_x = int(lineinfo[1])
                mapsize_y = int(lineinfo[2])
                startmapdata = i + 1
                break
            
        self.map_surface = pygame.Surface((mapsize_x * 32, mapsize_y * 32))
        self.phys_tiles = []
        
        for i,row in enumerate(lines[startmapdata:]):
            for j,col in enumerate(row):
                if col == 'n': #blank tiles
                    continue
                elif col.isdigit() or col in ('a', 'b', 'c', 'd', 'e', 'f'):
                    num=int(col, 16)
                    if 0 <= num <= 15:
                        tile_rect = pygame.rect.Rect(((num % 4) * 32, (num / 4) * 32), (32, 32))
                        self.map_surface.blit(self.tileset, (j * 32, i * 32), tile_rect)
                        self.phys_tiles.append(Tile(pygame.rect.Rect((j * 32, i * 32), (32, 32))))
        
        
    
    def draw(self, screen):
        screen.blit(self.map_surface, (0,0))
        
if __name__ == "__main__":
    import main