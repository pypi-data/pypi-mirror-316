import itertools
import numpy as np
from algogames.base import EngineInterface



class ChessPiece:

    def __init__(self, pos, ptype, color, valid_moves):
        self.pos = pos
        self.type = ptype #capital letter
        self._piece = ptype if color == 'w' else ptype.lower()
        self.color = color
        self.valid_moves = valid_moves

    def __repr__(self):
        return f"ChessPiece('{self._piece}', '{self.pos}')"
    
    def __eq__(self, x):
        if isinstance(x, ChessPiece):
            return x._piece == self._piece
        elif isinstance(x, str):
            return x._piece == x
        else:
            return False



class ChessPieces:

    def __init__(self, pieces):
        self._p = np.array(pieces)


    def __iter__(self):
        return iter(self._p)
    

    def __str__(self):
        return str(self._p.tolist())


    def get_color(self, color):
        return ChessPieces([p for p in self._p if p.color == color])
    

    def get_piece_type(self, piece_type):
        return ChessPieces([p for p in self._p if p.type == piece_type])


    def __getitem__(self, key):
        if key == 'w' or key == 'b':
            return self.get_color(key)
        elif key in ['R','N','B','P','Q','K']:
            return self.get_piece_type(key)
        
        return self._p[key]


    def __add__(self, x):
        if isinstance(x, ChessPieces):
            return ChessPieces(self._p.tolist()+x._p.tolist())
        else:
            raise TypeError('ChessPieces only supports addition with other ChessPieces')


    def __len__(self):
        return len(self._p)


    def get_valid_moves(self):
        return sum([p.valid_moves for p in self._p], [])


    def get_numpy_bitboard(self):
        bb = np.zeros((8,8))
        for p in self._p:
            i,j = ChessBoard.SAN_TO_IJ[p.pos]
            bb[i,j] = 1
        return bb.flatten()



class ChessBoard:

    SAN_TO_IJ = {''.join(k):tuple(reversed(divmod(i,8))) for i,k in enumerate(itertools.product('abcdefgh','87654321'))}
    IJ_TO_SAN = {v:k for k,v in SAN_TO_IJ.items()}

    def __init__(self, board, row_slice=None, col_slice=None):
        self.rows = list(range(8))
        self.cols = list(range(8))
        if row_slice is not None:
            self.rows = self.rows[row_slice]
        if col_slice is not None:
            self.cols = self.cols[col_slice]

        self.ranks = list({san[1] for san,(i,j) in self.SAN_TO_IJ.items() if i <= self.rows[-1] and i >= self.rows[0]})
        self.files = list({san[0] for san,(i,j) in self.SAN_TO_IJ.items() if j <= self.cols[-1] and j >= self.cols[0]})
        self.ranks.sort(reverse=True)
        self.files.sort()
        self._i = self.rows[0]
        self._j = self.cols[0]
        self._board = board

        msg = 'Board data does not align with sliced {}: {} vs. {}.'
        nrows = len(self._board)
        assert nrows == len(self.rows), msg.format('rows', nrows, len(self.rows))
        ncols = len(self._board[0])
        assert sum([ncols == len(row) for row in self._board]) == nrows, 'Invalid chess board structure'
        assert ncols == len(self.cols), msg.format('columns', ncols, len(self.cols))

        self.nrows = nrows
        self.ncols = ncols


    def __getitem__(self, key):
        # Single algebraic notation position
        if isinstance(key, str):
            _i,_j = self._validate_san_pos(key)
            return self._board[_i][_j]

        # Single row
        if isinstance(key, int):
            _i = self._validate_ij_pos((key, self._j))[0]
            return ChessBoard([self._board[_i]], slice(_i, _i+1))

        # Slice of either algebraic notation or rows
        elif isinstance(key, slice):
            
            # Algebraic notation
            if isinstance(key.start, str) and isinstance(key.stop, str):
                rslice,cslice = self._validate_san_slice(key)
                return ChessBoard([row[cslice] for row in self._board[rslice]], rslice, cslice)
            
            # Rows
            if isinstance(key.start, int) and isinstance(key.stop, int):
                rslice,cslice = self._validate_ij_slices(key, slice(None))
                return ChessBoard([row[cslice] for row in self._board[rslice]], rslice, cslice)

        # Row,col notation or 2-D slicing in row,col notation
        elif isinstance(key, tuple):
            if len(key) != 2:
                raise IndexError(f'Indices for {len(key)} dimensions provided')

            # ALGEBRAIC SLICES NOT ALLOWED WHEN 2 SLICES PRESENT
            k0,k1 = key
            # Row and column slice
            if isinstance(k0, slice) and isinstance(k1, slice):
                rslice,cslice = self._validate_ij_slices(k0, k1)
                return ChessBoard([row[cslice] for row in self._board[rslice]], rslice, cslice)
            
            # Row slice with specific column
            elif isinstance(k0, slice) and isinstance(k1, int):
                rslice,cslice = self._validate_ij_slices(k0, slice(k1,k1+1))
                return ChessBoard([row[cslice] for row in self._board[rslice]], rslice, cslice)
            
            # Column slice with specific row
            elif isinstance(k1, slice) and isinstance(k0, int):
                rslice,cslice = self._validate_ij_slices(slice(k0,k0+1), k1)
                return ChessBoard([row[cslice] for row in self._board[rslice]], rslice, cslice)
            
            # Specific row and column
            elif isinstance(k0, int) and isinstance(k1, int):
                _i,_j = self._validate_ij_pos(key)
                return self._board[_i][_j]

        raise IndexError(f'Invalid index type: {key}. Index should use either algebraic notation or zero-indexed (row,column) notation.')
    

    def __repr__(self):
        s = '   ' + ('-' * (3 * len(self.files))) + '\n'
        _s = '{} \u2502' + ' {} ' * len(self.files) + '\u2502\n'
        for i,rank in enumerate(self.ranks):
            pieces = ['\u00b7' if p is None else p._piece for p in self._board[i]]
            s += _s.format(rank, *pieces)
        s += '   ' + ('-' * (3 * len(self.files))) + '\n'
        s += '    ' + '  '.join(self.files)
        return s


    def __iter__(self):
        i_idxs, j_idxs = np.indices((self.nrows, self.ncols))
        i_idxs = i_idxs.flatten() + self._i
        j_idxs = j_idxs.flatten() + self._j
        return ((i,j,p) for i,j,p in zip(i_idxs, j_idxs, self.array.flatten()))


    @property
    def array(self):
        return np.array(self._board)


    @property
    def pieces(self):
        pieces = self.array.flatten()
        return ChessPieces(np.array([p for p in pieces if p is not None]))
    

    def _validate_san_pos(self, pos):
        pos = pos.lower()
        if pos[0] not in self.files:
            raise IndexError(f"File '{pos[0]}' is not valid. Allowed files are {self.files}.")
        if pos[1] not in self.ranks:
            raise IndexError(f"Rank '{pos[1]}' is not valid. Allowed ranks are {self.ranks}.")
        i,j = self.SAN_TO_IJ[pos]
        return (i - self._i, j - self._j)
    

    def _validate_san_slice(self, san_slice):
        start = self._validate_san_pos(san_slice.start)
        stop = self._validate_san_pos(san_slice.stop)
        rslice = slice(min(start[0],stop[0]), max(start[0],stop[0])+1)
        cslice = slice(min(start[1],stop[1]), max(start[1],stop[1])+1)
        return (rslice, cslice)
    

    def _validate_ij_pos(self, pos):
        if pos[0] not in self.rows:
            raise IndexError(f"Row index '{pos[0]}' is not valid. Allowed row indices are {self.rows}.")
        if pos[1] not in self.cols:
            raise IndexError(f"Column index '{pos[1]}' is not valid. Allowed column indices are {self.cols}.")
        return (pos[0] - self._i, pos[1] - self._j)
    

    def _validate_ij_slices(self, rslice, cslice):
        rstart = rslice.start
        rstop = rslice.stop
        cstart = cslice.start
        cstop = cslice.stop

        if rslice.start is None:
            rstart = self.rows[0]
        if rslice.stop is None:
            rstop = self.rows[-1] + 1
        if cslice.start is None:
            cstart = self.cols[0]
        if cslice.stop is None:
            cstop = self.cols[-1] + 1

        min_pos = self._validate_ij_pos((rstart, cstart))
        max_pos = self._validate_ij_pos((rstop-1, cstop-1))
        rslice = slice(min_pos[0], max_pos[0]+1, rslice.step)
        cslice = slice(min_pos[1], max_pos[1]+1, rslice.step)
        return (rslice, cslice)



class ChessGameState:

    def __init__(self, state):
        self.fen = state['fen']
        self.pgn = state['pgn']
        self.clocks = np.array(state['clocks'])

        board = enumerate(state['board'])
        new_piece = lambda i,j,info: ChessPiece(ChessBoard.IJ_TO_SAN[(i,j)], **info)
        self.board = ChessBoard([[None if pinfo is None else new_piece(i,j,pinfo) for j,pinfo in enumerate(r)] for i,r in board])

        self.turn = state['turn']
        self.in_check = state['check']
        self.gameover = state['gameover_info'] is not None
        if self.gameover:
            self.winner = state['gameover_info']['winner']
            self.endgame_type = state['gameover_info']['type']
        else:
            self.winner = None
            self.endgame_type = None


    @property
    def all_valid_moves(self):
        return sum([sum([piece.valid_moves for piece in row if piece is not None], []) for row in self.board._board], [])



class ChessInterface(EngineInterface):

    def __init__(self):
        super().__init__(ChessGameState)


    def make_pseudo_move(self, gs: ChessGameState, move: str) -> ChessGameState:
        self._send('make-pseudo-move', {'pgn': gs.pgn, 'fen': gs.fen, 'move': move})
        resp = self._receive()

        if 'error' in resp:
            raise ValueError(resp['error'])

        return ChessGameState(resp)


    def _game_loop(self, algo) -> None:
        gs = self._get_gs()
        while not gs.gameover:
            move = algo.take_turn(gs)
            if not isinstance(move, str):
                raise TypeError(f"`take_turn` must return a string representing the desired move. Returned `{move}`")

            self._send('make-move', {'move': move})
            gs = self._get_gs()
