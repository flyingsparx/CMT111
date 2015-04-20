from blobs_backend_engine import Game

game = Game(winning_score = 5)
game.add_player("will")
game.add_player("sarah")

game.start()

game.move_player("will", "up")
