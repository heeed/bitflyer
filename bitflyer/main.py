from microbit import i2c, sleep, button_a as A, button_b as B, running_time

C = 123
def rand(limit):
    global C
    C = ((1664525 * C) + 1013904223) % 4294967296
    return C % limit

class Star:

    DATA = b'\x1c"\x13"!\x12\x0c'
    DATA2= b'\x18>?\x1f>\x1f\x0e\x04'
    SHIP_WIDTH = b'\x01\x02\x02\x03\x04\x04\x02\x03'

    def __init__(self):
        self.data = self.DATA if rand(2) else self.DATA2

    def init(self):
        self.moved = True
        self.x = rand(112) + 7
        self.y = 0
        self.speed = rand(27) + 10

    def draw(self, remove=False):
        D.blit(self.data, self.x, 63-(self.y//10), int(remove))
        if not remove:
            self.moved = False

    def next(self, ship_x):
        next_y = self.y + self.speed
        # ship is between 48 - 56, so 480-640 is the collision zone
        if next_y > 480 and next_y < 640:
            y_overlap = (next_y // 10) - 48
            if y_overlap > 7:
                y_overlap = 7
            if abs(self.x - ship_x) < self.SHIP_WIDTH[y_overlap]:
                self.draw(remove=True)
                self.y = next_y
                self.draw(remove=False)
                return True
        self.draw(remove=True)
        self.y = next_y
        self.moved = True
        if self.y > 640:
            self.init()


class Game:

    SHIP = b'\x0C\x15\x7e\x81\x7e\x15\x0C'

    def __init__(self):
        self.ship_x = 63
        self.ship_y = 8
        self.stars = [Star(),Star(),Star(),Star(),Star()]
        for star in self.stars:
            star.init()

    def collided(self):
        for star in self.stars:
            if star.y >= 48 and star.y < 56:
                pass

    def next(self):
        # remove ship
        D.blit(self.SHIP, self.ship_x -3, self.ship_y, 1)
        # update star positions
        cont = True
        for star in self.stars:
            if star.next(self.ship_x):
                cont = False
        for star in self.stars:
            if star.moved:
                star.draw()

        if A.is_pressed():
            self.ship_x -= 2
        elif B.is_pressed():
            self.ship_x += 2

        if self.ship_x < 6:
            self.ship_x = 6
        if self.ship_x > 124:
            self.ship_x = 124
        D.blit(self.SHIP, self.ship_x - 3, self.ship_y, 0)
        D.repaint(60)
        return cont


def run_game():
    g = Game()
    while g.next():
        pass


def game_over():
    pulse(200)
    pulse(200)
    for i in range(64, 30, -1):
        D.blit(None, 2, i, False, 1)
        D.blit(None, 2, i-8, False, 2)
        D.repaint(60)
        sleep(10)
        D.blit(None, 2, i, True, 1)
        D.blit(None, 2, i-8, True, 2)

    D.blit(None, 2, i, False, 1)
    D.blit(None, 2, i-8, False, 2)
    D.repaint(60)



from display import display as D
def main():
    global C
    display_init()
    D.repaint(60)
    D.clear()
    press_count = A.get_presses() + B.get_presses()
    while press_count == A.get_presses() + B.get_presses():
        pulse(150)
    C = running_time()
    D.repaint(60)
    run_game()
    game_over()

main()
