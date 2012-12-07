#!/usr/bin/env python
'''
Created on Nov 30, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

class InputState(object):
    '''Stores a keyboard state and the number of frames it was held for.'''

    def __init__(self, keys):
        '''Initializes a new InputState instance with a keyboard state.
        
        @type keys: bools
        @param keys: A keyboard state.
        '''
        self.keys = keys
        self.frames = 0
        
        
class PreviousLife(object):
    '''Defines the actions of a previous player life. Allows for replay through
    the replay_step method.
    '''
    
    def __init__(self, state, player):
        '''Initializes a new PreviousLife instance with a list of InputStates.
        
        @type state: InputStates
        @param state: A list of InputStates of the player's previous life.
        @type player: Player
        @param player: The player object to act on.
        '''
        self.state = state
        self.index = 0
        self.frameoffset = 0
        self.player = player
    
    def replay_step(self, colliders):
        '''Steps the replay forward by one frame.'''
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
        self.player.update(self.state[self.index].keys, colliders)

    def replay_complete(self):
        '''Gets a value indicating whether the replay of the life has finished.
        
        @rtype: bool
        @return: True if the replay is finished, False otherwise.
        '''
        return self.index == len(self.state) - 1
    
    def replay_reset(self):
        '''Resets the replay back to the first frame of the first state.'''
        self.frameoffset = 0
        self.index = 0
        self.player.respawn()