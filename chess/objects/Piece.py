from persistent import Persistent
from PieceType import PieceType
import uuid

class Piece():
    def __init__(self,pieceTypeId,currentPosition,color):
        self.id=str(uuid.uuid4())
        self.currentPosition=currentPosition
        self.color=color
        self.pieceTypeId=pieceTypeId
        self.isDead=False
        self.moved=False

    #removing dead piece from the board
    def removePiece(self):
        self.isDead=True
        self.currentPosition=[100,100]

    
    #all possible moves, boarders taken into consideration, but not the positions of other pieces
    def defineMoves(self,currentPosition):   
        possiblePositions=[]
        possiblePositionsFinal=[]
        #KING
        #castling taken into consideration
        if self.pieceTypeId==1:
            possiblePositions=[(currentPosition[0] +1,currentPosition[1]),
                                (currentPosition[0]-1,currentPosition[1]),
                                (currentPosition[0],currentPosition[1]+1),
                                (currentPosition[0],currentPosition[1]-1),
                                (currentPosition[0]+1,currentPosition[1]+1),
                                (currentPosition[0]-1,currentPosition[1]-1),
                                (currentPosition[0]+1,currentPosition[1]-1),
                                (currentPosition[0]-1,currentPosition[1]+1),
                                (currentPosition[0]-2,currentPosition[1]),
                                (currentPosition[0]+2,currentPosition[1])]
        #QUEEN    
        elif self.pieceTypeId==2:
            possiblePositions.extend((i, currentPosition[1]) for i in range(8) if i != currentPosition[0])
            possiblePositions.extend((currentPosition[0], j) for j in range(8) if j != currentPosition[1])
            possiblePositions.extend((i, j) for i in range(8) for j in range(8) if abs(i - currentPosition[0]) == abs(j - currentPosition[1]) and (i, j) != currentPosition)

        #ROOK
        elif self.pieceTypeId==3:
            for i in range(8):
                if i != currentPosition[0]:
                    possiblePositions.append((i, currentPosition[1]))
            for j in range(8):
                if j != currentPosition[1]:
                    possiblePositions.append((currentPosition[0], j))
            
        #KNIGHT
        elif self.pieceTypeId==4:
            possiblePositions=[(currentPosition[0] + 2, currentPosition[1] + 1),
                                (currentPosition[0] + 2, currentPosition[1] - 1),
                                (currentPosition[0] - 2, currentPosition[1] + 1),
                                (currentPosition[0] - 2, currentPosition[1] - 1),
                                (currentPosition[0] + 1, currentPosition[1] + 2),
                                (currentPosition[0] + 1, currentPosition[1] - 2),
                                (currentPosition[0] - 1, currentPosition[1] + 2),
                                (currentPosition[0] - 1, currentPosition[1] - 2),]
        #BISHOP
        elif self.pieceTypeId==5:
            for i in range(1, 8):
                possiblePositions.extend([
                    (currentPosition[0] + i, currentPosition[1] + i),
                    (currentPosition[0] - i, currentPosition[1] - i),
                    (currentPosition[0] + i, currentPosition[1] - i),
                    (currentPosition[0] - i, currentPosition[1] + i)])
        #PAWN    
        #an pasan taken into consideration    
        else:
            if(self.color=="white"):
                possiblePositions.extend([
                    (currentPosition[0], currentPosition[1] + 1),
                    (currentPosition[0] - 1, currentPosition[1] + 1),
                    (currentPosition[0] + 1, currentPosition[1] + 1),
                    (currentPosition[0], currentPosition[1] + 2),
                    (currentPosition[0]+1, currentPosition[1]),
                    (currentPosition[0]-1, currentPosition[1])
                ])
            if(self.color=="black"): 
                 possiblePositions.extend([
                    (currentPosition[0], currentPosition[1] - 1),
                    (currentPosition[0] - 1, currentPosition[1] - 1),
                    (currentPosition[0] + 1, currentPosition[1] - 1),
                    (currentPosition[0], currentPosition[1] - 2),
                    (currentPosition[0]+1, currentPosition[1]),
                    (currentPosition[0]-1, currentPosition[1])
                ])

        #removing positions beyond borders    
        for item in possiblePositions:
           if item[0]>=0 and item[0]<=7 and item[1]>=0 and item[1]<=7:
                possiblePositionsFinal.append(item)

        #return possiblePositions
        return self.sortPiece(currentPosition,possiblePositionsFinal)

    #if pawn has reached the end of the board
    def swapPieceType(self,pieceTypeId):
        self.pieceTypeId=pieceTypeId

    def movePiece(self,newCurrentPosition):
        self.currentPosition=newCurrentPosition
        
    def __str__(self):
        return f"{self.pieceTypeId}-{self.color}"
    
    #Function to calculate the square of the Euclidean distance
    def sortPiece(self, currentPosition, possibleMoves):
        
        def distance_square(move):
            x, y = move
            return (x - currentPosition[0])**2 + (y - currentPosition[1])**2

        #Sort moves according to the square of the Euclidean distance from the currentPosition
        sortedMoves = sorted(possibleMoves, key=distance_square)
        return sortedMoves


#p=Piece(1,(1,1),"white")
#print(p.defineMoves(*p.currentPosition))
