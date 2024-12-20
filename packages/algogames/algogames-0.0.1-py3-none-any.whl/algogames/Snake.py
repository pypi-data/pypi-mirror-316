from algogames.base import EngineInterface
import numpy as np



class SnakeGameState:

    def __init__(self, engine_json):
        self.snake = np.array(engine_json['snake'])
        self.apple = np.array(engine_json['apple'])
        self.hunger = engine_json['hunger']
        self.direction = engine_json['direction']
        self.gameover = engine_json['gameover']



class SnakeInterface(EngineInterface):

    N = 0
    E = 1
    S = 2
    W = 3

    WIDTH = 26
    HEIGHT = 25

    def __init__(self):
        super().__init__(SnakeGameState)


    def _make_move(self, direction: int):
        if isinstance(direction, (int, np.integer)):
            direction = int(direction) # fixes int64 issue
            self._send('make-move', {'direction': direction})
            return

        raise TypeError("`take_turn` must return an integer representing the direction your snake wants to move")      


    def _game_loop(self, algo):
        gs = self._get_gs()
        while not gs.gameover:
            self._make_move(algo.take_turn(gs))
            gs = self._get_gs()
