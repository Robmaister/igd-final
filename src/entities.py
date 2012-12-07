'''
Created on Dec 3, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

import pygame
import tweening

class Button(object):
    
    def __init__(self, x, y, name):
        self.img = pygame.image.load("../assets/img/button_unpressed.png").convert_alpha()
        self.img_disabled = pygame.image.load("../assets/img/button_disabled.png").convert_alpha()
        self.img_pressed = pygame.image.load("../assets/img/button_pressed.png").convert_alpha()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.name = name
        self.start_pos = (x, y)
        self.pressed = False
        self.enabled = True
        self.connected = []
        
    def get_rect(self):
        return self.rect
    
    def press(self):
        if not self.enabled:
            return
        
        self.pressed = not self.pressed
        if self.pressed:
            for c in self.connected:
                c.on_pressed()
        else:
            for c in self.connected:
                c.on_unpressed()
                
    def update(self):
        pass
    
    def draw(self, screen):
        if self.enabled:
            if self.pressed:
                screen.blit(self.img_pressed, self.rect)
            else:
                screen.blit(self.img, self.rect)
        else:
            screen.blit(self.img_disabled, self.rect)
        
    def reset(self):
        self.rect.x = self.start_pos[0]
        self.rect.y = self.start_pos[1]
        self.pressed = False
                
class SlidingBlock(object):
    
    def __init__(self, x, y, name):
        self.img = pygame.image.load("../assets/img/door.png").convert()
        self.img_pressed = pygame.image.load("../assets/img/door_opened.png").convert()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.start_pos = (x, y)
        self.name = name
        self.pressed = False
        self.step = 0.0
        
    def get_rect(self):
        return self.rect
        
    def on_pressed(self):
        self.pressed = True
    
    def on_unpressed(self):
        self.pressed = False
    
    def update(self):
        if self.pressed:
            smoothpos = tweening.smoothstep(0, 1, self.step)
            self.rect.y = self.start_pos[1] - (smoothpos * 32)
            self.step += 0.05
        elif self.step > 0.0:
            smoothpos = tweening.smoothstep(0, 1, self.step)
            self.rect.y = self.start_pos[1] - (smoothpos * 32)
            self.step -= 0.05
            self.step = max(0, self.step)
    
    def draw(self, screen):
        if self.pressed:
            screen.blit(self.img_pressed, self.rect)
        else:
            screen.blit(self.img_pressed, self.rect)
        
    def reset(self):
        self.rect.x = self.start_pos[0]
        self.rect.y = self.start_pos[1]
        self.step = 0.0
        self.pressed = False
    
class FloorButton(object):
    
    def __init__(self, x, y, name):
        self.img = pygame.image.load("../assets/img/player.png").convert()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.name = name
        self.start_pos = (x, y)
        self.connected = []
        self.already_pressed = False
        self.pressed = False #TODO call connected when this becomes true.
        
    def get_rect(self):
        return self.rect
    
    def press(self):
        pass
    
    def unpress(self):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        
    def reset(self):
        self.rect.x = self.start_pos[0]
        self.rect.y = self.start_pos[1]
        self.already_pressed = False
        self.pressed = False
        
class Spike(object):
    def __init__(self, x, y, xvel, yvel, name):
        self.img = pygame.image.load("../assets/img/spikes.png").convert_alpha()
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.vel = (xvel, yvel)
        self.start_pos = (x, y)
        self.name = name
        self.enabled = False
        
    def get_rect(self):
        return self.rect
    
    def on_pressed(self):
        self.enabled = True
    
    def on_unpressed(self):
        self.enabled = False
    
    def update(self):
        if self.enabled:
            self.rect.x += self.vel[0]
            self.rect.y += self.vel[1]
        
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        
    def reset(self):
        self.rect.x = self.start_pos[0]
        self.rect.y = self.start_pos[1]
        self.enabled = False
        
class LevelEnd(object):
    def __init__(self, x, y, name):
        self.rect = pygame.rect.Rect(x, y, 32, 32)
        self.name = name
        
    def get_rect(self):
        return self.rect
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass
    
    def reset(self):
        pass
    
if __name__ == "__main__":
    import main