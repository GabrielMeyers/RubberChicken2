__author__ = 'Mr. Howe'
import pygame, random, math


class Clown:
    def __init__(self):
        """
        This is where we set up the variables for this particular object as soon as it is created.
        """
        self.x = random.randrange(0,600)
        self.y = random.randrange(0,200)
        angle = random.random()*2*math.pi
        self.vx = 300 * math.cos(angle)
        self.vy = 300 * math.cos(angle)
        self.i_am_alive = True
        self.image = pygame.image.load("images/invader.gif")
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

    def draw_self(self, screen_canvas):
        """
        It is this object's responsibility to draw itself on the surface. It will be told to do this often!
        :param screen_canvas:
        :return: None
        """
        #pygame.draw.ellipse(screen_canvas,pygame.Color("red"),(int(self.x),int(self.y),self.width,self.height),2);
        screen_canvas.blit(self.image, (int(self.x)-self.width/2 ,
                                        int(self.y)-self.height/2))

    def step(self, delta_T):
        """
        In order to change over time, this method gets called very often. The delta_T variable is the amount of time it
        has been since the last time we called "step()" usually about 1/20 -1/60 of a second.
        :param delta_T:
        :return: None
        """
        self.x = self.x + self.vx * delta_T
        self.y = self.y + self.vy * delta_T

        if self.y < 0+self.width/2:
            self.vy = abs(self.vy)

        if self.y > 200 - self.width/2:
            self.vy = -abs(self.vy)

        if self.x < 0+self.height / 2:
            self.vx  = abs(self.vx)

        if self.x > 600 - self.height / 2:
            self.vx = -abs(self.vx)


    def is_dead(self):
        """
        lets another object know whether this object is still live and on the board. Used by the main loop to clear objects
        in need of removal.
        :return: True or False - is this object dead?
        """
        if self.i_am_alive:
            return False
        else:
            return True
        # alternative (1-line) version of this function:
        #  "return not self.i_am_alive"


    def die(self):
        """
        change the status of this object so that it is dead.
        :return: None
        """
        self.i_am_alive = False