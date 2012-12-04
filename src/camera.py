'''
Created on Dec 3, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame

class Camera(object):
    '''
    classdocs
    '''

    def __init__(self, screen, bounds, view):
        '''
        Constructor
        '''
        self.bounds = bounds
        self.view = view
        self.screen = screen
        self.original_pos = (view.x, view.y)
        self.target_pos = (view.x, view.y)
        
    def move_to(self, pos):
        self.target_pos = (pos.x, pos.y)
        
    def move_by(self, x, y):
        self.target_pos = (self.target_pos[0] + x, self.target_pos[1] + y)
        
    def center_at(self, pos):
        self.target_pos = (pos.x - self.view.size[0] / 2, pos.y - self.view.size[1] / 2)
        
    def update(self):
        self.view.x += (self.target_pos[0] - self.view.x) * 0.1 #adding some juice
        self.view.y += (self.target_pos[1] - self.view.y) * 0.1
        self.view.clamp_ip(self.bounds)
        
    def blit(self, source, dest, area=None, special_flags=0):
        newdest = (dest[0] - self.view.x, dest[1] - self.view.y)
        ret_rect = self.screen.blit(source, newdest, area, special_flags)
        return ret_rect
    
if __name__ == "__main__":
    import main