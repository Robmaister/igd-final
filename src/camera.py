'''
Created on Dec 3, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame

class ParallaxBackground(object):
    
    def __init__(self, camera, p, img):
        self.cam = camera
        self.img = pygame.image.load(img).convert()
        self.p = p
        
    def draw(self, screen):
        imgrect = self.img.get_rect()
        newrect = pygame.rect.Rect((self.cam.view.x * -self.p, self.cam.view.y * -self.p), (imgrect.width, imgrect.height))
        if newrect.x > 0: newrect.x = 0
        if newrect.y > 0: newrect.y = 0
        if newrect.x < -imgrect.width + self.cam.view.width: newrect.x = -imgrect.width + self.cam.view.width
        if newrect.y < -imgrect.height + self.cam.view.height: newrect.y = -imgrect.height + self.cam.view.height
        screen.blit(self.img, (newrect.x, newrect.y))

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