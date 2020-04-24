from time import sleep
import pygame
from pygame.locals import *
import autopy
from pynput.mouse import Controller,Button
import keyboard


m = Controller()


class MouseClass:

    def getMouseValues(self,done):
        (ch, LB, RB) = ('None',0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    done = True
                else:
                    print (pygame.key.name(event.key))
                    ch = pygame.key.name(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print ("in mousebuttondown")
                print ("mouse  : %d" % event.button)
                if event.button == 1:
                    LB = 1
                elif event.button == 3:
                    RB = 1
        (X,Y) = pygame.mouse.get_pos()
        print ("%d %d %d %d" %(X ,Y ,LB ,RB))
        return [ch, X, Y, LB, RB]

    def setMouseValues(self, ch, X, Y, LB, RB):

        autopy.mouse.move(int(X),int(Y))

        if int(LB) ==1:
            m.click(Button.left, 1)
        if int(RB) ==1:
            m.click(Button.right, 1)

        if ch != 'None':
            keyboard.press_and_release(ch)


if __name__ == '__main__' :
	pygame.init()
	screen = pygame.display.set_mode((1440,900))
	done = False
	mi = MouseClass()
	while not done:
		(ch, X, Y, LB, RB) = mi.getMouseValues(done)
		print ("%c %d %d %d %d" %(ch, X, Y, LB, RB))
