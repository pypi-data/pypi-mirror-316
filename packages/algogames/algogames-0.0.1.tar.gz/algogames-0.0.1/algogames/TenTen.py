from algogames.base import EngineInterface
import numpy as np



class TenTenInterface(EngineInterface):

    def __init__(self):
        self.state = None


    def check_move(self, move):
        data = {'command': 'checkmove', 'data': move}
        self._send(data)
        resp = self._receive()
        return resp['data']['isvalid']
    

    def _make_moves(self, moves):
        self._send({'command': 'makemove', 'data': moves})


    def _get_gs(self):
        received = self._receive()
        self.gameover = received['gameover']
        self.board = np.array(received['board'])
        self.hand = [np.array(piece) for piece in received['hand']]


    def _run(self, algo):
        self._get_gs()
        while not self.gameover:
            moves = algo.take_turn(self)
            self._make_moves(moves)
            self._get_gs()
