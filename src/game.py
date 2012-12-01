'''
Created on Nov 27, 2012

@author: robert
'''

import pygame, sys

import player

class StoredInputState(object):
    def __init__(self, keys):
        self.keys = keys
        self.frames = 0
        
class PreviousLife(object):
    def __init__(self, state):
        self.state = state
        self.index = 0
        self.frameoffset = 0
        self.player = player.Player(0, 0)
    
    def update(self):
        self.frameoffset += 1
        if self.state[self.index].frames < self.frameoffset:
            self.frameoffset = 0
            if self.index < len(self.state) - 1:
                self.index += 1
            else:
                self.player.velx = 0
                self.player.vely = 0
                self.player.accelx = 0
                self.player.accely = 0
        self.player.update()
            
    def get_current_state(self):
        return self.state[self.index]
    
    def replay_complete(self):
        return self.index == len(self.state) - 1
    
    def reset(self):
        self.frameoffset = 0
        self.index = 0
        self.player.rect.x = 0
        self.player.rect.y = 0
        self.player.velx = 0
        self.player.vely = 0
        #TODO reset player position

class Game(object):
    def __init__(self):
        pygame.init()
        self.lastUpdateTime = pygame.time.get_ticks()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.previouslives = []
        self.currentlife = [StoredInputState(pygame.key.get_pressed())] #temp item
        self.prevlifeindex = 0
        self.prevlifeframe = 0
        self.player = player.Player(0, 0)
        
    def update(self):
        pressedkeys = pygame.key.get_pressed()
        
        #Clock wasn't precise enough for accurate playback
        #rawtime = pygame.time.get_ticks()
        #time = rawtime - self.lastUpdateTime #self.clock.get_time()
        #print time
        #self.lastUpdateTime = rawtime
        
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
                if e.key == pygame.K_k:
                    self.previouslives.append(PreviousLife(self.currentlife))
                    self.currentlife = [StoredInputState(pressedkeys)]
                    self.player.rect.left = 0
                    self.player.rect.top = 0
                    for life in self.previouslives:
                        life.reset()
        
        #store current life's state.
        if pressedkeys != self.currentlife[-1].keys:
            self.currentlife.append(StoredInputState(pressedkeys))
        else:
            self.currentlife[-1].frames += 1

        for life in self.previouslives:
            life.update()
            if not life.replay_complete():
                keys = life.get_current_state().keys
                if keys[pygame.K_w]:
                    life.player.vely = -200
                elif keys[pygame.K_s]:
                    life.player.vely = 200
                else:
                    life.player.vely = 0
                if keys[pygame.K_a]:
                    life.player.velx = -200
                elif keys[pygame.K_d]:
                    life.player.velx = 200
                else:
                    life.player.velx = 0
                
            
        #handle movement
        if pressedkeys[pygame.K_w]:
            self.player.vely = -200
        elif pressedkeys[pygame.K_s]:
            self.player.vely = 200
        else:
            self.player.vely = 0
        if pressedkeys[pygame.K_a]:
            self.player.velx = -200
        elif pressedkeys[pygame.K_d]:
            self.player.velx = 200
        else:
            self.player.velx = 0
            
        #print self.clock.get_time()
        
        self.player.update()
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for life in self.previouslives:
            life.player.draw(self.screen)
            
if __name__ == "__main__":
    import main