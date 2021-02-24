
from threading import Thread
from queue import Queue
from objects import Character
from objects import Obstacle
from player import Gene
from player import Handle
import pygame as pg
import sys

class ThreadHandler :
    def __init__(self) :
        self.is_stop = False

    def stop(self) :
        self.is_stop = True

    def getState(self) :
        return self.is_stop

class JumpGame :
    def __init__(self, size, fps, screen_color, character_color, obstacle_color) :
        self.SIZE = size
        self.FPS = fps
        self.SC = screen_color
        self.CC = character_color
        self.OC = obstacle_color

        # default setting
        self.FPS = 60
        self.C_WIDTH = 30
        self.C_HEIGHT = 80
        self.O_WIDTH = 28
        self.O_HEIGHT = 28
        self.O_SPEED = 4

        self.GENE_AMOUNT = 3
        self.GENE_BEST_AMOUNT = 1
        self.FIRST_RANGE = 0
        self.SECOND_RANGE = 100

        self.genes = []
        self.ths = []
        self.threads = []
        self.generation = 1
        self.pg = pg

    def __initCharacter(self) :
        char = Character(self.pg, self.screen)
        char.drawInit(self.CC, self.C_WIDTH, self.C_HEIGHT)

        return char

    def __initObstacle(self) :
        obs = Obstacle(self.pg, self.screen, self.O_SPEED)
        obs.drawInit(self.OC, self.O_WIDTH, self.O_HEIGHT)

        return obs

    def __drawCharacter(self, char) :
        char.draw()

    def __drawObstacle(self, obs) :
        return obs.draw()

    def __checkJumping(self, char) :
        char.jump()

    def __checkCrash(self, char, obs, th) :
        while True :
            for char_pos in char.getAllLocation() :
                for obs_pos in obs.getAllLocation() :
                    if char_pos == obs_pos :
                        # print("crash")
                        sys.exit(0)

            if th.getState() :
                # print("avoid")
                sys.exit(0)

    def __createNewGene(self) :
        for _ in range(self.GENE_AMOUNT) :
            self.ths.append(ThreadHandler())

        return [
            Gene(self.__initCharacter(), self.FIRST_RANGE, self.SECOND_RANGE) for _ in range(self.GENE_AMOUNT)
        ]

    def show(self) :
        self.pg.init()
        self.pg.display.set_caption("Jumping Game!")
        self.screen = self.pg.display.set_mode(self.SIZE)
        self.clock = self.pg.time.Clock()

        if len(self.genes) == 0 :
            self.genes = self.__createNewGene()

        else :
            handle = Handle(self.genes, self.__createNewGene())
            self.genes = handle.mutate(self.GENE_BEST_AMOUNT)
        
        obs1 = self.__initObstacle()

        for i in range(self.GENE_AMOUNT) :
            thread = Thread(target=self.__checkCrash, args=(
                self.genes[i].char, obs1, self.ths[i]
            ))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

        while True :
            self.screen.fill(self.SC) 
           
            for event in pg.event.get() :
                if event.type == pg.QUIT :
                    sys.exit(0)

            for i in range(self.GENE_AMOUNT) :
                if self.threads[i].is_alive() :
                    self.genes[i].addScore()
                    self.genes[i].jump(obs1)
                    self.__drawCharacter(self.genes[i].char)
                    self.__checkJumping(self.genes[i].char)

            if not self.__drawObstacle(obs1) :
                break

            self.pg.display.flip()
            self.clock.tick(self.FPS)
        
        gene_amount = 0

        for i in range(self.GENE_AMOUNT) :
            if self.threads[i].is_alive() :
                gene_amount += 1

            self.ths[i].stop()
            self.threads[i].join()

        print("Generation ", self.generation, " : ", gene_amount)

        self.ths = []
        self.threads = []
        self.generation += 1
        self.show()

game = JumpGame(
    (500, 250), # size
    30, # fps
    (255, 255, 255), # screen color 
    (0, 0, 0), # character color
    (255, 0, 0) # obstacle color
)
game.show()