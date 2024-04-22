import numpy as np 
from mss import mss
import pydirectinput
import cv2
import pytesseract
from matplotlib import pyplot as plt 
import time
from gym import Env
from gym.spaces import Box, Discrete

class game(Env):
    #setup the environment and observation
    def __init__(self):
        super().__init__()
        self.observation_space = Box(low=0, high=255, shape=(1,83,100), dtype=np.uint8)
        self.action_space = Discrete(4)
        env = game
        plt.imshow(env.observation_space.sample()[0])
    #do something in the game
    def step(self,action):
        #action key - 0 = accelerate, 1 = brake, 2 = turn left, 3 = turn right
        pass
    def render(self):
        pass
    def reset(self):
        pass
    def getObservation(self):
        pass
