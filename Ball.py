import pygame
import random 

class Ball:
    RADIUS = 7
    VEL = 5

    def __init__(self,x,y):
        self.x = self.og_x = x
        self.y = self.og_y = y

        x_dir = random.uniform(0,1)
        x_dir = 1 if x_dir > 0.5 else -1
        y_ang = random.uniform(-3,3)

        self.x_vel = self.VEL * x_dir
        self.y_vel = y_ang

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self,window):
        pygame.draw.circle(window, (255,0,0), (self.x, self.y),self.RADIUS)

    def reset(self):
        self.x = self.og_x 
        self.y = self.og_y 

        x_dir = random.uniform(0,1)
        x_dir = 1 if x_dir > 0.5 else -1
        y_ang = random.uniform(-3,3)

        self.x_vel = self.VEL * x_dir
        self.y_vel = y_ang

