#!/usr/bin/env python
'''
Created on Nov 27, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame

class Player(object):
    """A Player is a game entity that the user can control."""
    
    def __init__(self, x, y):
        """Initializes a new Player instance at a specified point in the world.
        
        @type x: number
        @param x: The player's X coordinate
        @type y: number
        @param y: The player's Y coordinate
        
        """
        self.img = pygame.image.load("../assets/img/player.png").convert()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.spawn_x = x
        self.spawn_y = y
        self.velx = 0
        self.vely = 0
        self.jumping = True
    
    def update(self, keys, colliders):
        """Updates the player.
        
        @type keys: bools
        @param keys: The current keyboard state.
        @type colliders: Rects
        @param colliders: The rectangles to collide against.
        
        """
        if keys[pygame.K_w]:
            if not self.jumping:
                self.vely -= 70
        #if keys[pygame.K_s]:
            #pass
        if keys[pygame.K_a]:
            self.velx = -10
        if keys[pygame.K_d]:
            self.velx = 10
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            self.velx = 0
        
        if self.jumping:
            self.vely += 5
            
        #separate collision detection/resolution by axis.
        self.rect.left += self.velx * 0.016
        for c in colliders:
            if self.rect.colliderect(c):
                if self.velx > 0: self.rect.right = c.left
                elif self.velx < 0: self.rect.left = c.right
                
        self.jumping = True
        self.rect.top += self.vely * 0.016
        for c in colliders:
            if self.rect.colliderect(c):
                if self.vely > 0:
                    self.rect.bottom = c.top
                    self.vely = 0
                    self.jumping = False
                elif self.vely < 0:
                    self.rect.top = c.bottom
        

    def draw(self, surface):
        """Draws the player to the screen.
        
        @type surface: Surface
        @param surface: The surface to blit the player onto. 
        
        """
        surface.blit(self.img, self.rect)
        
    def respawn(self):
        self.velx = 0
        self.vely = 0
        self.rect.topleft = (self.spawn_x, self.spawn_y)
        
if __name__ == "__main__":
    import main