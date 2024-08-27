from persistent import Persistent
import uuid

class Player(Persistent):
    def __init__(self,name,pieces):
        self.id=str(uuid.uuid4())
        self.name=name
        self.pieces=pieces
        
    def getPieces(self):
        return self.pieces