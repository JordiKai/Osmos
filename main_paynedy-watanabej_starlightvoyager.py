#-----------STARLIGHT VOYAGER by JordiKai Watanabe-Inouye and Dylan Payne-----------


# ----SOUNDTRACK CREDITS------
# Orange Ocean (Loscil Remix) by Kodomo
# Calcium Needles by Brian Eno
# Horse by Brian Eno

import pygame
import random
import math
from pygame.locals import *
import sys

def main():
    # initialize Pygame
    pygame.init()
    # initialize sound module
    pygame.mixer.init(channels = 16, size = 8)
    # start game from the start screen
    SpaceGame(0)

class SpaceGame(pygame.sprite.Sprite):
    """MODEL: This class holds on to sprite groups and remembers important information such as velocity
    and position for each sprite.  The sprite groups contained in SpaceGame are modified by the
    control class and fed to the graphic interface class."""

    def __init__(self, ilevel):
        """ Launches a level (window size, music, etc.) """
        #---Creating a Window---
        # inititates the Graphic Interface
        self.width = 1440
        self.height = 900
        self.interface = GraphicInterface(self.width, self.height)
        self.level = ilevel
        #---Launch start screen---
        if self.level == 0:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load('Orange Ocean.wav')
                pygame.mixer.music.set_volume(.6)
                pygame.mixer.music.play(-1)
            self.start_screen()

        #---MAKE SPRITE GROUPS---
        # this group contains all the spheres including the user sphere
        # for colliding and absorbing purposes
        self.all_spherelist = pygame.sprite.Group()
        # a singleton group of just the usersphere, for later manipulation
        self.userspherelist = pygame.sprite.GroupSingle()
        # this group contains all star objects
        self.starlist = pygame.sprite.Group()
        self.missilelist = pygame.sprite.Group()
        # a list of all objects spheres and star(s), which will be used for
        # collision, absorbtion, clone 'n grow, and kill purposes
        self.absorb_list = []
        # the same as absorb_list, but specific to interactions with "magic missiles"
        self.missile_absorb_list = []
        # Inititates the Controller class
        self.controller = Controller()

        #---MAKE SPRITES---
        self.controller.generate_level(self.width, self.height, self.absorb_list, self.missile_absorb_list, self.all_spherelist, self.userspherelist, self.starlist, self.missilelist, self.level)

        self.play()

    def play(self):
        """ This method keeps the window open and pygame running until the user either
        inputs/clicks an exit operator, such as clicking the red 'x' or ESC.  Users can
        jump to any level by pressing the corresponding number on the keyboard and they can
        restart the current level by hitting the spacebar or clicking the mouse.
        """
        pygame.time.Clock()

        # Loop until the user clicks the close button or hits "escape"
        done = False
        while not done:
            #pygame.time.delay(15)
            pygame.time.delay(10) #Jordi Do-able

            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            SpaceGame(self.level)

                        if event.key == K_1:
                            pygame.mixer.music.stop()
                            SpaceGame(1)
                        if event.key == K_2:
                            pygame.mixer.music.stop()
                            SpaceGame(2)
                        if event.key == K_3:
                            pygame.mixer.music.stop()
                            SpaceGame(3)
                        if event.key == K_4:
                            pygame.mixer.music.stop()
                            SpaceGame(4)
                        if event.key == K_5:
                            pygame.mixer.music.stop()
                            SpaceGame(5)
                        if event.key == K_6:
                            pygame.mixer.music.stop()
                            SpaceGame(6)
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        SpaceGame(self.level)


            # This draws the spheres, stars and missiles on the window
            self.interface._clear()
            self.interface._draw(self.all_spherelist, self.starlist, self.missilelist)

            # This looks at the user input and updates all of the sprites
            self.controller.user_input()
            self.controller.update_and_move(self.userspherelist, self.all_spherelist, self.starlist, self.missilelist, self.width, self.height)
            self.controller.absorb(self.absorb_list,self.missile_absorb_list,self.all_spherelist, self.starlist, self.userspherelist, self.missilelist)
            self.controller.missile_absorb(self.absorb_list, self.missile_absorb_list, self.all_spherelist, self.starlist, self.userspherelist, self.missilelist)
            if len(self.starlist) == 0:
                self.nextlevel()
                if self.level > 4:
                    pygame.mixer.music.stop()
                if self.level < 7:
                    SpaceGame(self.level)
                else:
                    SpaceGame(0)

    def start_screen(self):
    	""" This method creates a start screen and waits for user input"""
    	texton = True
    	while texton:
    		self.interface.startscreen(self.width, self.height)
    		for event in pygame.event.get():
    			if event.type == MOUSEBUTTONDOWN:
    				texton = False
    			if event.type == KEYDOWN:
    				if event.key == K_RETURN:
    					texton = False
    				if event.key == K_SPACE:
    					texton = False
    				if event.key == K_ESCAPE:
    					pygame.quit()
    					sys.exit()
    	self.nextlevel()

    def nextlevel(self):
        """ Increases level by one"""
        self.level += 1

class GraphicInterface(pygame.sprite.Sprite):
    """This class is the VIEW portion of our game. It is in charge of creating a window
    and drawing the sprites.
    Arguments:
    -   width and height of the window
    """
    def __init__(self, width, height):
        """ Makes window"""
        #----Creating Window-----
        self.window = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
        # make mouse disappear
        pygame.mouse.set_visible(False)

    def startscreen(self, W, H):
        """ This method creates start screen with an image"""
        self.window.fill((0,0,0))
        start = pygame.image.load("StartBud.gif")
        startrect = list(start.get_rect())
        imageH = startrect[3]
        imageW = startrect[2]
        # centers the image on the screen
        self.window.blit(start, (W//2-imageW//2,H//2-imageH//2))
        pygame.display.flip()

    def _clear(self):
        """ Clears window"""
        self.window.fill((0,0,0))

    def _draw(self, sprite_group,starlist,missilelist):
        """ This method draws all the sprites on the window"""
        sprite_group.draw(self.window)
        starlist.draw(self.window)
        missilelist.draw(self.window)
        pygame.display.flip()

class Controller(pygame.sprite.Sprite):
    """This class is the CONTROL portion of our game. It is in charge of getting input from
    the user and updating the status of the sprites, which includes modifying the velocity of the
    user sprite, having the other sprites gravitate around the _Star object, and having all the sprites
    collide and absorb one another based off of their sizes(comparatively & case-by-case)"""
    def __init__(self):
        """ Sets variables that will be used later to detect user input and loads sound effects."""
        self.pressed_left = None
        self.pressed_right = None
        self.pressed_up = None
        self.pressed_down = None

        sound1 = pygame.mixer.Sound('1.wav')
        sound2 = pygame.mixer.Sound('2.wav')
        sound3 = pygame.mixer.Sound('3.wav')
        sound4 = pygame.mixer.Sound('4.wav')
        sound5 = pygame.mixer.Sound('5.wav')
        sound6 = pygame.mixer.Sound('6.wav')
        sound7 = pygame.mixer.Sound('7.wav')

        self.soundlist = [sound1,sound2,sound3,sound4,sound5,sound6,sound7]

    def gravitate(self, sphere, starlist):
        """ This method was taken mostly from Miller and Ranum.  It makes the other
        spheres gravitate towards the _Star object."""
        G = .1
        dt = .0001
        for star in starlist:
            M = star.getMass()
            rx = star.getXpos() - sphere.getXpos()
            ry = star.getYpos() - sphere.getYpos()
            r = math.sqrt(rx**2 + ry**2)
            # to prevent a divide by zero error when a sphere is on top of a star
            if r > 0:
            	# technically r should be raised to the third power, but we changed it
            	# to the 1.4th power so that the star would continue to have a stong pull
            	# at a great distance
            	accx = G * M*rx/r**1.4
            	accy = G * M*ry/r**1.4
            	sphere.change_Xvel(dt * accx)
            	sphere.change_Yvel(dt * accy)

    def magic_gravitate(self, missile, userspherelist):
    	"""This method makes the missile gravitate towards the usersphere"""
    	G = .13
    	dt = .1
    	for sphere in userspherelist:
            M = sphere.getRadius()*1.5
            rx = sphere.getXpos() - missile.getXpos()
            ry = sphere.getYpos() - missile.getYpos()
            r = math.sqrt(rx**2 + ry**2)
            if r > 0:
        	    accx = G * M*rx/r**1.1
        	    accy = G * M*ry/r**1.1
        	    missile.change_Xvel(dt * accx)
        	    missile.change_Yvel(dt * accy)

    def add_user_sphere(self, userobject, absorb_list, missile_absorb_list, all_spherelist, userspherelist):
        """ This method is in charge of adding the user sphere to lists"""
        # add this sprite to the absorb list
        absorb_list.append(userobject)
        missile_absorb_list.append(userobject)
        userspherelist.add(userobject)

        all_spherelist.add(userobject)

    def add_sphere(self, asphere, absorb_list, all_spherelist):
        """ This method is in charge of adding a sphere to lists"""
        absorb_list.append(asphere)
        all_spherelist.add(asphere)

    def add_star(self, newStar, absorb_list, missile_absorb_list, starlist):
        """ This method is in charge of adding a new star to lists"""
        # Add this sprite to the absorb list
        absorb_list.append(newStar)
        missile_absorb_list.append(newStar)
        # To allow for multiple stars if we want to use them
        starlist.add(newStar)

    def add_missile(self, newmissile, missile_absorb_list, missilelist):
        """ This method is in charge of adding a missile to lists"""
        missilelist.add(newmissile)
        missile_absorb_list.append(newmissile)

    def generate_spheres(self,width, height, number, lo, hi, absorb_list, all_spherelist):
        """ This method helps with the level creation process by reducing the creation of spheres
        to a few variables (number of spheres, size of "galaxy").  Each sphere's position is
        randomly generated and its initial velocity is determined by its position"""
        Xmid = width//2
        Ymid = height//2
        for i in range(1,number):
            # the "galaxy" of orbiting objects remains the same size regardless of window size
            galaxy_randX = random.randrange(Xmid-910,Xmid+910)
            galaxy_randY = random.randrange(Ymid-490, Ymid+490)

            randRadius = random.randrange(lo,hi)

            # This block helps to give the inner spheres some extra x velocity so the
            #orbits don't collapse:
                     # if the new sphere is above the center point:
            if galaxy_randY >= Ymid:
                # x velocity = distance above midpoint times -.007 minus 5
                scaledXvel = (galaxy_randY-Ymid) * -.007 - 2
            # if the new sphere it is below the center point
            if galaxy_randY < Ymid:
                scaledXvel = (galaxy_randY-Ymid) * -.007 + 2

            scaledYvel = (galaxy_randX-Xmid) * .007

            # create a sphere
            sphere = _Sphere(i,randRadius, galaxy_randX, galaxy_randY,scaledXvel,scaledYvel)
            # Add each sphere to its own group and put all of these "personal groups" into a
            # list to be iterated through in the absorb step
            self.add_sphere(sphere, absorb_list, all_spherelist)

    def generate_level(self, width, height, absorb_list, missile_absorb_list, all_spherelist, userspherelist, starlist, missilelist, level):
        """ This method creates and adds all the sprites (the user sphere, other spheres, the
        blackhole) for the game. This method frequently references the _Sphere and _Star classes."""

        #---Center of the Window---
        Xmid = width//2
        Ymid = height//2

        #-----------6 levels, one little sphere and the adventure of a lifetime----------------

        if level == 1:
                   #---PLAY SOUNDTRACK---
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load('Orange Ocean.wav')
                pygame.mixer.music.set_volume(.6)
                pygame.mixer.music.play(-1)

                    #---USER PLANET---
            randX = random.randrange(20,width-20)
            randY = random.randrange(20,height-20)
            new_user_sphere = _Sphere(0,7, randX, randY, 0, 0)
            self.add_user_sphere(new_user_sphere, absorb_list, missile_absorb_list, all_spherelist, userspherelist)

                    #---OTHER PLANETS---
            self.generate_spheres(width, height, 150, 3, 12, absorb_list, all_spherelist)

                    #---BLACK HOLES---
            black_hole = _Star(500,35, Xmid, Ymid)
            self.add_star(black_hole, absorb_list, missile_absorb_list, starlist)

        if level == 2:
                   #---PLAY SOUNDTRACK---
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load('Orange Ocean.wav')
                pygame.mixer.music.set_volume(.6)
                pygame.mixer.music.play(-1)

                    #---USER PLANET---
            randX = random.randrange(20,width-20)
            randY = random.randrange(20,height-20)
            new_user_sphere = _Sphere(0,7, randX, randY, 0, 0)
            self.add_user_sphere(new_user_sphere, absorb_list, missile_absorb_list, all_spherelist, userspherelist)

                    #---OTHER PLANETS---
            self.generate_spheres(width, height, 150, 3, 12, absorb_list, all_spherelist)

                    #---BLACK HOLES---
            black_hole2 = _Star(501,21, Xmid-250, Ymid+200)
            self.add_star(black_hole2, absorb_list, missile_absorb_list, starlist)
            black_hole3 = _Star(502,21, Xmid+250, Ymid+200)
            self.add_star(black_hole3, absorb_list, missile_absorb_list, starlist)
            black_hole4 = _Star(503,21, Xmid, Ymid-200)
            self.add_star(black_hole4, absorb_list, missile_absorb_list, starlist)

        if level == 3:
                   #---PLAY SOUNDTRACK---
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load('Orange Ocean.wav')
                pygame.mixer.music.set_volume(.6)
                pygame.mixer.music.play(-1)

                     #---USER PLANET---
            randX = random.randrange(20,width-20)
            randY = random.randrange(20,height-20)
            new_user_sphere = _Sphere(0,7, randX, randY, 0, 0)
            self.add_user_sphere(new_user_sphere, absorb_list, missile_absorb_list, all_spherelist, userspherelist)

                    #---OTHER PLANETS---
            self.generate_spheres(width, height, 150, 3, 12, absorb_list, all_spherelist)

                    #---BLACK HOLES---
            black_hole2 = _Star(502,23, Xmid-150, Ymid)
            self.add_star(black_hole2, absorb_list, missile_absorb_list, starlist)
            black_hole3 = _Star(503,23, Xmid+150, Ymid)
            self.add_star(black_hole3, absorb_list, missile_absorb_list, starlist)
            black_hole4 = _Star(504,22, Xmid+75, Ymid+150)
            self.add_star(black_hole4, absorb_list, missile_absorb_list, starlist)
            black_hole5 = _Star(505,22, Xmid-75, Ymid+150)
            self.add_star(black_hole5, absorb_list, missile_absorb_list, starlist)
            black_hole6 = _Star(506,22, Xmid+75, Ymid-150)
            self.add_star(black_hole6, absorb_list, missile_absorb_list, starlist)
            black_hole7 = _Star(507,22, Xmid-75, Ymid-150)
            self.add_star(black_hole7, absorb_list, missile_absorb_list, starlist)

        if level == 4:
                   #---PLAY SOUNDTRACK---
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load('Orange Ocean.wav')
                pygame.mixer.music.set_volume(.6)
                pygame.mixer.music.play(-1)

    	            #---USER PLANET---
            randX = random.randrange(20,width-20)
            randY = random.randrange(20,height-20)
            new_user_sphere = _Sphere(0,7, randX, randY, 0, 0)
            self.add_user_sphere(new_user_sphere, absorb_list, missile_absorb_list, all_spherelist, userspherelist)

                    #---OTHER PLANETS---
            self.generate_spheres(width, height, 150, 3, 9, absorb_list, all_spherelist)

                    #---BLACK HOLES---
            black_hole = _Star(500,40, Xmid, Ymid)
            self.add_star(black_hole, absorb_list, missile_absorb_list, starlist)

                    #---MAGIC MISSILES----
            for i in range (6):
                randX = random.randrange(20,width-20)
                randY = random.randrange(20,height-20)
                magic_missile = _Sphere(600+i,5, randX, randY, 0, 0)
                self.add_missile(magic_missile, missile_absorb_list, missilelist)

        if level == 5:
                   #---PLAY SOUNDTRACK---
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load('Calcium Needles.wav')
                pygame.mixer.music.set_volume(.13)
                pygame.mixer.music.play(-1)

    	            #---USER PLANET---
            randX = random.randrange(20,width-20)
            randY = random.randrange(20,height-20)
            new_user_sphere = _Sphere(0,11, randX, randY, 0, 0)
            self.add_user_sphere(new_user_sphere, absorb_list, missile_absorb_list, all_spherelist, userspherelist)

                    #---BLACK HOLES---
            black_hole = _Star(500,18, Xmid, Ymid)
            self.add_star(black_hole, absorb_list, missile_absorb_list, starlist)
            black_hole2 = _Star(501,8, Xmid-350, Ymid+200)
            self.add_star(black_hole2, absorb_list, missile_absorb_list, starlist)
            black_hole3 = _Star(502,8, Xmid+350, Ymid+200)
            self.add_star(black_hole3, absorb_list, missile_absorb_list, starlist)
            black_hole4 = _Star(503,8, Xmid-350, Ymid-200)
            self.add_star(black_hole4, absorb_list, missile_absorb_list, starlist)
            black_hole5 = _Star(504,8, Xmid+350, Ymid-200)
            self.add_star(black_hole5, absorb_list, missile_absorb_list, starlist)

                    #---MAGIC MISSILES----
            for i in range (50):
                randX = random.randrange(10,width-10)
                randY = random.randrange(10,height-10)
                magic_missile = _Sphere(600+i,5, randX, randY, 0, 0)
                self.add_missile(magic_missile, missile_absorb_list, missilelist)

            magic_missile = _Sphere(600,5, Xmid, Ymid+100, 0, 0)
            self.add_missile(magic_missile, missile_absorb_list, missilelist)
            magic_missile = _Sphere(601,5, Xmid, Ymid-100, 0, 0)
            self.add_missile(magic_missile, missile_absorb_list, missilelist)
            magic_missile = _Sphere(602,5, Xmid+75, Ymid+75, 0, 0)
            self.add_missile(magic_missile, missile_absorb_list, missilelist)
            magic_missile = _Sphere(603,5, Xmid-75, Ymid+75, 0, 0)
            self.add_missile(magic_missile, missile_absorb_list, missilelist)
            magic_missile = _Sphere(604,5, Xmid+75, Ymid-75, 0, 0)
            self.add_missile(magic_missile, missile_absorb_list, missilelist)
            magic_missile = _Sphere(605,5, Xmid-75, Ymid-75, 0, 0)
            self.add_missile(magic_missile, missile_absorb_list, missilelist)

        if level == 6:
                   #---PLAY SOUNDTRACK---
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load('Horse.wav')
                pygame.mixer.music.set_volume(.16)
                pygame.mixer.music.play(-1)

    	            #---USER PLANET---
            randX = random.randrange(30,width-30)
            randY = random.randrange(30,height-30)
            new_user_sphere = _Sphere(0,18, randX, randY, 0, 0)
            self.add_user_sphere(new_user_sphere, absorb_list, missile_absorb_list, all_spherelist, userspherelist)

                    #---OTHER PLANETS---
            self.generate_spheres(width, height, 170, 3, 15, absorb_list, all_spherelist)

                    #---BLACK HOLES---
            black_hole2 = _Star(501,20, Xmid-500, Ymid+300)
            self.add_star(black_hole2, absorb_list, missile_absorb_list, starlist)
            black_hole5 = _Star(504,20, Xmid+500, Ymid-300)
            self.add_star(black_hole5, absorb_list, missile_absorb_list, starlist)

                    #---MAGIC MISSILES----
            magic_missile = _Sphere(600,100, Xmid, Ymid, 0, 0)
            self.add_missile(magic_missile, missile_absorb_list, missilelist)

    def user_input(self):
        """ This method is in charge of figuring out what key the user has pressed.
        The response then changes the triggers initialized outside. Based on this response """
        # These act as triggers- recognizing when the user releases the key
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_up = False
        self.pressed_down = False

        # This gets the key that was pressed and changes the value of the key
        # to 'True' if it was pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pressed_left = True
        if keys[K_RIGHT]:
            self.pressed_right = True
        if keys[K_UP]:
            self.pressed_up = True
        if keys[K_DOWN]:
            self.pressed_down = True

    def drag(self, asphere, amount):
        """ Reduces a sphere's velocity over time"""
        Xvel = asphere.getXvel()
        Yvel = asphere.getYvel()
        if Xvel < 0:
            asphere.change_Xvel(amount)
        if Xvel > 0:
            asphere.change_Xvel(-amount)
        if Yvel < 0:
            asphere.change_Yvel(amount)
        if Yvel > 0:
            asphere.change_Yvel(-amount)

    def update_and_move(self,userspherelist, all_spherelist, starlist, missilelist, width, height):
        """ High-level method in control of changing postion and velocity of objects and adding and removing them."""
        # makes usersphere bounce off of walls
        for usersphere in userspherelist:
            if usersphere.rect.left < 0 or usersphere.rect.right > width:
                usersphere.vel[0] = -usersphere.vel[0]
            if usersphere.rect.top < 0 or usersphere.rect.bottom > height:
                usersphere.vel[1] = -usersphere.vel[1]

            thrust = .25

            if self.pressed_left == True:
                usersphere.change_Xvel(-thrust)
            if self.pressed_right == True:
                usersphere.change_Xvel(thrust)
            if self.pressed_up == True:
                usersphere.change_Yvel(-thrust)
            if self.pressed_down == True:
                usersphere.change_Yvel(thrust)

            # Give the user sphere some drag better more control
            self.drag(usersphere, .065)

		# MOVE PLANETS
        for asphere in all_spherelist:
            self.gravitate(asphere, starlist)
            # This command moves the Sprites at a given velocity!
            asphere.rect = asphere.rect.move(asphere.vel)

        # MOVE MISSILES
        for amissile in missilelist:
        	self.drag(amissile,.15)
        	self.magic_gravitate(amissile, userspherelist)
        	amissile.rect = amissile.rect.move(amissile.vel)

    def absorb(self, absorb_list, missile_absorb_list, all_spherelist, starlist, userspherelist, missilelist):
        """ This function looks for collision between sprites and makes the larger sprite eat the smaller"""
        for asprite in absorb_list:
            A = asprite
            # for all sprites in the absorb list not including the sprite called 'A'
            for asprite in self.listExceptIndex(absorb_list,absorb_list.index(A)):
                B = asprite
                if pygame.sprite.collide_rect(A,B) == True:
                    if A.getRadius() > B.getRadius():
                        # Plays a note signifying the gobbling of a star
                    	if B in starlist:
                    	    note = random.choice(self.soundlist)
                    	    note.play()
                    	# Kill B and replace A
                    	self.kill(B, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)
                    	new_sphere = self.clone_and_grow(A,B,absorb_list, missile_absorb_list, all_spherelist, starlist, userspherelist)
                    	self.kill(A, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)

                    elif A.getRadius() == B.getRadius():
                        if B in starlist:
                    	    note = random.choice(self.soundlist)
                    	    note.play()
                        # Kill B and replace A
                        self.kill(B, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)
                        new_sphere = self.clone_and_grow(A,B, absorb_list, missile_absorb_list, all_spherelist, starlist, userspherelist)
                        self.kill(A, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)

                    elif A.getRadius() < B.getRadius():
                        if A in starlist:
                    	    note = random.choice(self.soundlist)
                    	    note.play()
                        # Kill A and replace B
                        self.kill(A, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)
                        new_sphere = self.clone_and_grow(B,A, absorb_list, missile_absorb_list, all_spherelist, starlist, userspherelist)
                        self.kill(B, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)

    def missile_absorb(self, absorb_list, missile_absorb_list, all_spherelist, starlist, userspherelist, missilelist):
        """ This function does the same as the absorb function however it is specific to missile objects"""
        for asprite in missile_absorb_list:
            A = asprite
            # for all sprites in the absorb list not including the sprite called 'A'
            for asprite in self.listExceptIndex(missile_absorb_list,missile_absorb_list.index(A)):
                B = asprite
                if pygame.sprite.collide_circle(A,B) == True:
                	if A in missilelist and B in userspherelist:
                	    self.kill(B, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)

                	elif B in missilelist and A in userspherelist:
                	    self.kill(A, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)

                	elif A in missilelist and B in starlist:
                	    self.kill(A, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)

                	elif B in missilelist and A in starlist:
                	    self.kill(B, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist)

    def clone_and_grow(self,A_sprite, B_sprite, absorb_list, missile_absorb_list, all_spherelist, starlist, userspherelist):
        """ Returns a new sphere with some of the properties of the old one."""

        if A_sprite in starlist:
            # we wanted to make the growth visually noticable, so after some testing
            # we found that multiplying B's area by 1.57 was a good number
            new_area = A_sprite.getArea() + B_sprite.getArea()*1.57
            new_radius = round(math.sqrt(new_area//(math.pi)))
            replacement = _Star(A_sprite.getName(), new_radius, A_sprite.getXpos(),A_sprite.getYpos())
            self.add_star(replacement, absorb_list, missile_absorb_list, starlist)
        else:
            new_area = A_sprite.getArea() + B_sprite.getArea()
            new_radius = round(math.sqrt(new_area//(math.pi)))
            if A_sprite.getName() == 0:
                replacement = _Sphere(0, new_radius, A_sprite.getXpos(),A_sprite.getYpos(),A_sprite.getXvel(),A_sprite.getYvel())
                self.add_user_sphere(replacement, absorb_list, missile_absorb_list, all_spherelist, userspherelist)
            else:
                replacement = _Sphere(A_sprite.getName(), new_radius, A_sprite.getXpos(),A_sprite.getYpos(),A_sprite.getXvel(),A_sprite.getYvel())
                self.add_sphere(replacement, absorb_list, all_spherelist)

        return replacement

    def kill(self, object, absorb_list, missile_absorb_list, all_spherelist, starlist, missilelist, userspherelist):
        """ This function is in charge of removing an object from its designated lists"""
        if object in absorb_list:
            absorb_list.remove(object)
        if object in missile_absorb_list:
            missile_absorb_list.remove(object)

        if object in all_spherelist:
            all_spherelist.remove(object)
        if object in userspherelist:
            userspherelist.remove(object)
        if object in missilelist:
        	missilelist.remove(object)
        if object in starlist:
            starlist.remove(object)


    # a little trick I learned back in CS 111
    def listExceptIndex(self, L, i):
        """Given a list L and an index i, returns a copy of L without the item at
        index i."""
        return L[:i] + L[i+1:]

class _Sphere(pygame.sprite.Sprite):
    """This class is in charge of creating a sphere object.
    A sphere is created as a sprite (based off of a circle image)! """
    def __init__(self, iname, irad, ix, iy, ivx, ivy):
        """ Makes a sprite based off of radius"""
        pygame.sprite.Sprite.__init__(self)

        self.name = iname
        self.radius = irad
        self.vel = [ivx,ivy]
        self.xPos = ix
        self.yPos = iy

        #This block determines the color of the sphere based off of its radius (compared to the usersphere):
        self.color = (100-255//(self.radius),0,100+255//(self.radius))
        if self.name == 0:
            self.color = (255,255,255)
        if self.name >= 600:
        	self.color = (100,0,0)

        self.image = self.make_circle(self.radius, self.color)

        self.rect = self.image.get_rect()

        #sets the initial position
        self.setposition(ix, iy)


    def make_circle(self, radius, color):
        """ Returns a circle image that will be saved as a sphere """
        image = pygame.Surface((2*radius,2*radius))
        image.fill((0,0,0))

        #set_colorkey makes the square surface behind the circle transparent
        #as long as it is the same color as the background
        image.set_colorkey((0,0,0))

        pygame.draw.circle(image,(color),(radius,radius),radius,0)
        return image

    def getArea(self):
        """ Returns the area of a sphere (not rounded; float int)"""
        r = self.getRadius()
        Area = (math.pi)*(r**2)
        return Area

    def getRect(self):
        return self.rect
    def getName(self):
        return(self.name)
    def getRadius(self):
        return self.radius

    def getXvel(self):
        return self.vel[0]
    def getYvel(self):
        return self.vel[1]
    def change_Xvel(self, amount):
        self.vel[0] += amount
    def change_Yvel(self, amount):
        self.vel[1] += amount

    def getXpos(self):
        return self.rect.x
    def getYpos(self):
        return self.rect.y
    def setposition(self, x, y):
        self.rect.x = x
        self.rect.y = y

class _Star(pygame.sprite.Sprite):
    """This class is in charge of creating a star object.
    A star is also created as a sprite (based off of a circle image)!"""
    def __init__(self, iname, irad, ix, iy):
            pygame.sprite.Sprite.__init__(self)

            self.name = iname
            self.color = (50,20,20)
            self.radius = irad
            self.volume = 4.0/3 * math.pi * self.radius**3

            # This block of code is different from portions in the Sphere class
            self.mass = self.volume/5
            self.xPos = ix
            self.yPos = iy
            self.image = self.make_circle(self.radius, self.color)
            self.rect = self.image.get_rect()

            #sets the initial position
            self.rect.center = (ix, iy)


    def make_circle(self, radius, color):
        """ Returns a circle image on a rectangular surface """
        image = pygame.Surface((2*radius,2*radius))
        image.fill((0,0,0))

        #set_colorkey makes the square surface behind the circle transparent
        #as long as it is the same color as the background
        image.set_colorkey((0,0,0))

        pygame.draw.circle(image,(color),(radius,radius),radius,5)
        return image

    def getArea(self):
        """ Returns the area of a star """
        r = self.getRadius()
        Area = (math.pi)*(r**2)
        return Area

    def getRect(self):
        return self.rect
    def getName(self):
        return(self.name)
    def getRadius(self):
        return self.radius
    def getMass (self):
        return self.mass

    def getXvel(self):
        return 0
    def getYvel(self):
        return 0

    def getXpos(self):
        return self.xPos
    def getYpos(self):
        return self.yPos
    def setposition(self, x, y):
        self.rect.x = x
        self.rect.y = y

if __name__ == "__main__":
  main()
