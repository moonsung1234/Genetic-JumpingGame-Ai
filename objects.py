
import time

class Character :
    def __init__(self, pg, screen) :
        self.pg = pg
        self.screen = screen

        self.jump_max = 80
        self.is_jumping = False
        self.jump_state = False 

    def drawInit(self, color, width, height) :
        self.color = color
        self.width = width
        self.height = height

        self.pg.draw.rect(
            self.screen,
            self.color,
            (100, self.screen.get_height() - height, self.width, self.height)
        )

        self.x, self.y = 100, self.screen.get_height() - height

    def draw(self) :
        self.pg.draw.rect(
            self.screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

    def startJumping(self) :
        self.is_jumping = True

    def getIsJumping(self) :
        return self.is_jumping

    def jump(self) :
        begin_y = self.screen.get_height() - self.height

        if self.is_jumping :
            if not self.jump_state :
                self.y -= 7

                if self.y <= self.jump_max :
                    self.jump_state = True
                
            elif self.y >= begin_y :
                self.jump_state = False
                self.is_jumping = False

            else :
                self.y += 7

            self.draw()

    def getAllLocation(self) :
        location_all = []

        for i in range(self.width) :
            location_all.append((self.x + i, self.y))
            location_all.append((self.x + i, self.y + self.height))

        for i in range(self.height) :
            location_all.append((self.x, self.y + i))
            location_all.append((self.x + self.width, self.y + i))

        return location_all

class Obstacle :
    def __init__(self, pg, screen, speed) :
        self.pg = pg
        self.screen = screen
        self.speed = speed

    def drawInit(self, color, width, height) :
        self.color = color
        self.width = width
        self.height = height

        self.pg.draw.polygon(
            self.screen,
            self.color,
            (
                (self.screen.get_width() + self.width / 2, self.screen.get_height() - height),
                (self.screen.get_width(), self.screen.get_height()),
                (self.screen.get_width() + self.width, self.screen.get_height())
            )
        )

        self.x1, self.y1 = self.screen.get_width() + self.width / 2, self.screen.get_height() - height
        self.x2, self.y2 = self.screen.get_width(), self.screen.get_height()
        self.x3, self.y3 = self.screen.get_width() + self.width, self.screen.get_height()

    def draw(self) :
        if not self.x3 <= 0 :
            self.x1 -= self.speed
            self.x2 -= self.speed
            self.x3 -= self.speed

        else :
            return False

        self.pg.draw.polygon(
            self.screen,
            self.color,
            (
                (self.x1, self.y1),
                (self.x2, self.y2),
                (self.x3, self.y3)
            )
        )

        return True

    def getAllLocation(self) :
        location_all = []

        for i in range(self.width) :
            location_all.append((self.x2 + i, self.y2))

        temp = self.width / self.height

        for i in range(1, self.height) :
            location_all.append((self.x1 - temp * i, self.y1 + i))
            location_all.append((self.x1 + temp * i, self.y1 + i))

        return location_all