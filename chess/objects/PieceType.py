from persistent import Persistent

class PieceType(Persistent):
    def __init__(self, typeid, typename):
        self.typeid = typeid
        self.typename = typename

"""
ubaci ovih 6 tipova rucno u bazu

1-King
2-Queen
3-Rook
4-Knight
5-Bishop
6-Pawn
"""
