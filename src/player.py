#!/usr/bin/env python
'''
Created on Nov 27, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame

import level, entities

class Player(object):
    '''A Player is a game entity that the user can control.'''
    
    def __init__(self, x, y):
        '''Initializes a new Player instance at a specified point in the world.
        
        @type x: number
        @param x: The player's X coordinate
        @type y: number
        @param y: The player's Y coordinate
        '''
        self.img_idle0 = pygame.image.load("../assets/img/player_idle0.png").convert_alpha()
        self.img_idle1 = pygame.image.load("../assets/img/player_idle1.png").convert_alpha()
        self.img_walk0 = pygame.image.load("../assets/img/player_walk0.png").convert_alpha()
        self.img_walk1 = pygame.image.load("../assets/img/player_walk1.png").convert_alpha()
        self.img_jump0 = pygame.image.load("../assets/img/player_jump0.png").convert_alpha()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.spawn_x = x
        self.spawn_y = y
        self.velx = 0
        self.vely = 0
        self.jumping = True
        self.readytojump = False
        self.prev_update_e = False
        self.dead = False
        self.anim_counter = 0
    
    def update(self, keys, colliders):
        '''Updates the player.
        
        @type keys: bools
        @param keys: The current keyboard state.
        @type colliders: Rects
        @param colliders: The rectangles to collide against.
        '''
        if self.dead:
            return
        #Figure out when we first press E and not when we hold it
        e_pressed = False
        if not self.prev_update_e and keys[pygame.K_e]:
            e_pressed = True
            self.prev_update_e = True
        if not keys[pygame.K_e]:
            self.prev_update_e = False
        
        if keys[pygame.K_w]:
            if (not self.jumping) and self.readytojump:
                self.vely -= 950
                #self.readytojump = False
        else:
            if not self.jumping:
                self.readytojump = True
        if keys[pygame.K_s] and self.jumping:
            self.vely += 20
        if keys[pygame.K_a]:
            self.velx = -400
        elif keys[pygame.K_d]:
            self.velx = 400
        else:
            if self.velx > 0:
                self.velx = max(0, self.velx - 50)
            elif self.velx < 0:
                self.velx = min(0, self.velx + 50)
        
        if self.jumping:
            self.vely += 55
            
        self.vely = min(2000, self.vely) #terminal velocity
            
        #separate collision detection/resolution by axis.
        self.rect.left += self.velx * 0.016
        for c in colliders:
            r = c.get_rect()
            if self.rect.colliderect(r):
                if isinstance(c, level.Tile) or isinstance(c, entities.SlidingBlock):
                    if self.velx > 0: self.rect.right = r.left
                    elif self.velx < 0: self.rect.left = r.right
                elif isinstance(c, entities.Button) and e_pressed:
                    c.press()
                elif isinstance(c, entities.LevelEnd):
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 2))
                elif isinstance(c, entities.Spike):
                    self.dead = True
                    return
                
        self.jumping = True
        self.rect.top += self.vely * 0.016
        for c in colliders:
            r = c.get_rect()
            if self.rect.colliderect(r):
                if isinstance(c, level.Tile) or isinstance(c, entities.SlidingBlock):
                    if self.vely > 0:
                        self.rect.bottom = r.top
                        self.vely = 0
                        self.jumping = False
                    elif self.vely < 0:
                        self.rect.top = r.bottom
                        self.vely = 0 #start falling
                elif isinstance(c, entities.FloorButton):
                    c.pressed = True
                elif isinstance(c, entities.Spike):
                    self.dead = True
                    return
            elif isinstance(c, entities.FloorButton):
                c.pressed = False
        

    def draw(self, surface):
        '''Draws the player to the screen.
        
        @type surface: Surface
        @param surface: The surface to blit the player onto. 
        '''
        self.anim_counter += 1
        self.anim_counter %= 20 #wrap back to 0 after 90 frames.
        
        if not self.dead:
            if self.vely > 55 or self.vely < 0: #prevents animation spazzing
                surface.blit(self.img_jump0, self.rect)
            elif self.velx != 0:
                if self.anim_counter < 5:
                    surface.blit(self.img_walk0, self.rect)
                elif 5 <= self.anim_counter < 10:
                    surface.blit(self.img_idle0, self.rect)
                elif 10 <= self.anim_counter < 15:
                    surface.blit(self.img_walk1, self.rect)
                elif 15 <= self.anim_counter:
                    surface.blit(self.img_idle0, self.rect)
            elif self.anim_counter <= 10:
                surface.blit(self.img_idle0, self.rect)
            else:
                surface.blit(self.img_idle1, self.rect)
        
    def respawn(self):
        self.velx = 0
        self.vely = 0
        self.jumping = True
        self.dead = False
        self.rect.topleft = (self.spawn_x, self.spawn_y)
        
    def get_rect(self):
        return self.rect