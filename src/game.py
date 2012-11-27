'''
Created on Nov 27, 2012

@author: robert
'''

import pygame, sys

class StoredInputState(object):
    def __init__(self, keys):
        self.keys = keys
        self.time = 0

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.previouslives = []
        self.currentlife = [StoredInputState([])] #temp item
        self.prevlifeindex = 0
        self.prevlifetime = 0
        
    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
                
        pressedkeys = pygame.key.get_pressed()
        
        #store current life's state.
        if pressedkeys != self.currentlife[-1].keys:
            self.currentlife.append(StoredInputState(pressedkeys))
        else:
            self.currentlife[-1].time += self.clock.get_time()

        if len(self.previouslives) > 0 and not self.prevlifeindex >= len(self.previouslives[0]):
            self.prevlifetime += self.clock.get_time()
            if self.prevlifetime >= self.previouslives[0][self.prevlifeindex].time:
                self.prevlifeindex += 1
                self.prevlifetime = 0
            print "Previous life 0, State", self.prevlifeindex, ", Time", self.prevlifetime
            
        #handle movement
        #if pressedkeys[pygame.K_w]:
        #if pressedkeys[pygame.K_a]:
        #if pressedkeys[pygame.K_s]:
        #if pressedkeys[pygame.K_d]:
        if pressedkeys[pygame.K_k]:
            self.previouslives.append(self.currentlife)
            self.currentlife = [StoredInputState([])]
        
    def draw(self):
        pass