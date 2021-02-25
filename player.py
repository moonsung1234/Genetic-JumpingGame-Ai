
import random
import math

class Gene :
    def __init__(self, char, range1, range2) :
        self.char = char
        self.distance = random.uniform(range1, range2)
        self.score = 0

    def __getDistance(self, obs) :
        char_x = self.char.x + self.char.width
        char_y = self.char.y + self.char.height

        return math.sqrt(math.pow(char_x - obs.x2, 2) + math.pow(char_y - obs.y2, 2))

    def getScore(self) :
        return self.score

    def getDistance(self) :
        return self.distance

    def addScore(self) :
        self.score += 1

    def setDistance(self, range1, range2) :
        self.distance = random.uniform(range1, range2)

    def jump(self, obs) :
        if abs(round(self.distance) - round(self.__getDistance(obs))) <= 2 :
            self.char.startJumping()

class Handle :
    def __init__(self, before_genes, new_genes) :
        self.before_genes = before_genes
        self.new_genes = new_genes

    def __getBestGene(self, amount) :
        return sorted(self.before_genes, key=lambda gene : gene.getScore())[len(self.before_genes) - amount:]

    def mutate(self, amount) :
        best_genes = self.__getBestGene(amount)
        mean = 0

        for gene in best_genes :
            mean += gene.getDistance()

        mean /= len(best_genes)

        for i in range(len(self.new_genes)) :
            if random.randint(0, 2) == 0 :
                self.new_genes[i].setDistance(mean - mean / 3, mean + mean / 3)

            else :
                self.new_genes[i].setDistance(mean, mean)

        return self.new_genes


