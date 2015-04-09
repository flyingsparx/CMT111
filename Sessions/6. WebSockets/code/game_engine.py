import random


class Player:
    def __init__(self, name, colour):
        self.name = name
        self.x = random.randint(0,19)
        self.y = random.randint(0,19)
        self.score = 0
        self.colour = colour
    def to_dict(self):
        ret = {}
        ret['name'] = self.name
        ret['x'] = self.x
        ret['y'] = self.y
        ret['colour'] = self.colour
        ret['score'] = self.score
        return ret

class Food:
    def __init__(self):
        self.generate_new_position()
    def generate_new_position(self):
        self.x = random.randint(0,19)
        self.y = random.randint(0,19)
    def to_dict(self):
        ret = {}
        ret['x'] = self.x
        ret['y'] = self.y
        return ret

class Game:
    def __init__(self):
        self.players = []
        self.food = Food()
       
    def add_player(self, name):
        colours = ["red","blue","yellow","brown"]
        p = Player(name.replace(" ",""),colours[len(self.players)])
        self.players.append(p)

    def move_player(self, name, direction):
        for p in self.players:
            if p.name == name:
                if direction == 'up' and p.y > 0:
                    p.y -= 1
                if direction == 'down' and p.y < 19:
                    p.y += 1
                if direction == 'left' and p.x > 0:
                    p.x -= 1
                if direction == 'right' and p.x < 19:
                    p.x += 1
                if p.x == self.food.x and p.y == self.food.y:
                    p.score += 1
                    self.food = Food()
