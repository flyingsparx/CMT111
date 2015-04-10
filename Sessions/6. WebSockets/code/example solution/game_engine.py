import random


class Player:
    def __init__(self, name, colour):
        self.name = name
        self.x = random.randint(0,19)
        self.y = random.randint(0,19)
        self.score = 0
        self.colour = colour
        self.winner = False
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
    def __init__(self, winning_score = 10):
        self.players = []
        self.food = Food()
        self.player_colours = ["red","blue","yellow","brown","black","pink","cyan"]
        self.winning_score = winning_score
        self.is_alive = True
        self.is_started = False
       
    def add_player(self, name):
        if self.is_started:
            raise Exception("Game has already started")
        if len(self.players) >= len(self.player_colours):
            raise Exception("Too many players")
        p = Player(name.replace(" ",""),self.player_colours[len(self.players)])
        self.players.append(p)

    def start(self):
        self.is_started = True

    def move_player(self, name, direction):
        if not self.is_started:
            raise Exception("Game hasn't yet started")
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
                if p.score >= self.winning_score:
                    p.winner = True
                    p.is_alive = False
