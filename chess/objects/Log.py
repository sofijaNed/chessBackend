from persistent import Persistent

class Log(Persistent):
    def __init__(self,turnNo,board,time,gameId):
        self.turnNo = turnNo
        self.board = board
        self.time = time
        self.gameId = gameId
