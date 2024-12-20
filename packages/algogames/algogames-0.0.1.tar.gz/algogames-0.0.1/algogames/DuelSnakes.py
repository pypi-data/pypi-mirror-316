from algogames.base import EngineInterface
import numpy as np



class DuelSnakesGameState:

    def __init__(self, engine_json):
        self.snakes = [np.array(engine_json['snakes'][0]), np.array(engine_json['snakes'][1])]
        self.hungers = np.array(engine_json['hungers'])
        self.apples = np.array(engine_json['apples'])
        self.directions = np.array(engine_json['directions'])
        self.gameover = engine_json['gameover']



class DuelSnakesInterface(EngineInterface):

    N = 0
    E = 1
    S = 2
    W = 3

    WIDTH = 26
    HEIGHT = 25

    def __init__(self):
        super().__init__(DuelSnakesGameState)


    def _parse_config(self, config: dict) -> dict:
        return {'start_pos': np.array(config['start_pos'])}


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
