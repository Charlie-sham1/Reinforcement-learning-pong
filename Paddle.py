import pygame

class Paddle:
    WIDTH = 20
    HEIGHT = 100
    VEL = 4

    def __init__(self,x,y):
        self.x = self.og_x = x
        self.y = self.og_y = y

    def draw(self, window):
        pygame.draw.rect(window, (255,255,255), pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self,up = True):
        if up:
            self.y -= self.VEL

        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.og_x
        self.y = self.og_y
