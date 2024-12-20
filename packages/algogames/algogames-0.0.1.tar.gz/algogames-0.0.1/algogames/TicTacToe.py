from algogames.base import EngineInterface
import numpy as np



class TicTacToeGameState:

    def __init__(self, engine_json): 
        self.board = np.array(engine_json['board'])
        self.gameover = engine_json['gameover']



class TicTacToeInterface(EngineInterface):

    EMPTY = 0
    SELF = 1
    ENEMY = 2

    def _get_gs(self):
        received = self._receive()
        gs = TicTacToeGameState(received)
        return gs


    def check_move(self, move):
        data = {'command': 'checkmove', 'data': move}
        self._send(data)
        resp = self._receive()
        return resp['data']['isvalid']


    def _make_moves(self, moves):
        self._send({'command': 'makemove', 'data': {'move':moves}})


    def _run(self, algo_class):
        self._ready()
        algo = algo_class(self._receive()['is_first'])

        gs = self._get_gs()
        while not gs.gameover:
            self._make_moves(algo.take_turn(gs, self))
            gs = self._get_gs()
