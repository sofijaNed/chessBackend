from Piece import Piece
from persistent import Persistent
from Player import Player
import uuid
import database
from typing import List

class Game(Persistent):
    def __init__(self, whitePlayer:Player, blackPlayer:Player):
        self.gameId = str(uuid.uuid4())
        self.blackPlayer = blackPlayer
        self.whitePlayer=whitePlayer
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.blackPlayer.pieces=self.initializeBlackPieces()
        self.whitePlayer.pieces=self.initializeWhitePieces()
        self.whiteKing=(4,0)
        self.blackKing=(4,7)
 
    def printBoard(self):
        
        transposed_matrix = list(zip(*self.board))

        for row in reversed(transposed_matrix):
            for item in reversed(row):
                print(item, end=' ')
            print()  
        # result = []
        # for row in reversed(transposed_matrix):
        #     row_list = []
        #     for item in reversed(row):
        #         row_list.append(str(item))
        #     result.append(row_list)
        # return result
    """izbrisan id za piece svuda ispod"""
    def initializeBlackPieces(self):
        b_pawn1=Piece(6,(0,6),"black")
        self.board[0][6]=b_pawn1
        b_pawn2=Piece(6,(1,6),"black")
        self.board[1][6]=b_pawn2
        b_pawn3=Piece(6,(2,6),"black")
        self.board[2][6]=b_pawn3
        b_pawn4=Piece(6,(3,6),"black")
        self.board[3][6]=b_pawn4
        b_pawn5=Piece(6,(4,6),"black")
        self.board[4][6]=b_pawn5
        b_pawn6=Piece(6,(5,6),"black")
        self.board[5][6]=b_pawn6
        b_pawn7=Piece(6,(6,6),"black")
        self.board[6][6]=b_pawn7
        b_pawn8=Piece(6,(7,6),"black")
        self.board[7][6]=b_pawn8

        b_rook1=Piece(3,(0,7),"black")
        self.board[0][7]=b_rook1
        b_rook2=Piece(3,(7,7),"black")
        self.board[7][7]=b_rook2

        b_bishop1=Piece(5,(2,7),"black")
        self.board[2][7]=b_bishop1
        b_bishop2=Piece(5,(5,7),"black")
        self.board[5][7]=b_bishop2
        b_knight1=Piece(4,(1,7),"black")
        self.board[1][7]=b_knight1
        b_knight2=Piece(4,(6,7),"black")
        self.board[6][7]=b_knight2

        b_king=Piece(1,(3,7),"black")
        self.board[3][7]=b_king
        b_queen=Piece(2,(4,7),"black")
        self.board[4][7]=b_queen

        blackPieces=[b_pawn1,b_pawn2,b_pawn3,b_pawn4,b_pawn5,b_pawn6,b_pawn7,b_pawn8,
                    b_rook1,b_rook2,b_bishop1,b_bishop2,b_knight1,b_knight2,b_king,b_queen]
        
        namesOfBlackPieces = [varName for varName, varValue in locals().items() if varValue in blackPieces]

        database.addPieces(blackPieces, namesOfBlackPieces, self.gameId)

        return blackPieces
    """izbrisan id za piece svuda ispod"""
    def initializeWhitePieces(self):
            w_pawn1=Piece(6,(0,1),"white")
            self.board[0][1]=w_pawn1
            w_pawn2=Piece(6,(1,1),"white")
            self.board[1][1]=w_pawn2
            w_pawn3=Piece(6,(2,1),"white")
            self.board[2][1]=w_pawn3
            w_pawn4=Piece(6,(3,1),"white")
            self.board[3][1]=w_pawn4
            w_pawn5=Piece(6,(4,1),"white")
            self.board[4][1]=w_pawn5
            w_pawn6=Piece(6,(5,1),"white")
            self.board[5][1]=w_pawn6
            w_pawn7=Piece(6,(6,1),"white")
            self.board[6][1]=w_pawn7
            w_pawn8=Piece(6,(7,1),"white")
            self.board[7][1]=w_pawn8

            w_rook1=Piece(3,(0,0),"white")
            self.board[0][0]=w_rook1
            w_rook2=Piece(3,(7,0),"white")
            self.board[7][0]=w_rook2

            w_bishop1=Piece(5,(2,0),"white")
            self.board[2][0]=w_bishop1
            w_bishop2=Piece(5,(5,0),"white")
            self.board[5][0]=w_bishop2

            w_knight1=Piece(4,(1,0),"white")
            self.board[1][0]=w_knight1
            w_knight2=Piece(4,(6,0),"white")
            self.board[6][0]=w_knight2

            w_king=Piece(1,(3,0),"white")
            self.board[3][0]=w_king
            w_queen=Piece(2,(4,0),"white")
            self.board[4][0]=w_queen

            whitePieces=[w_pawn1,w_pawn2,w_pawn3,w_pawn4,w_pawn5,w_pawn6,w_pawn7,w_pawn8,
                        w_rook1,w_rook2,w_bishop1,w_bishop2,w_knight1,w_knight2,w_king,w_queen]

            namesOfWhitePieces = [varName for varName, varValue in locals().items() if varValue in whitePieces]

            database.addPieces(whitePieces, namesOfWhitePieces, self.gameId)

            return whitePieces
    

    def showPossibleMoves(self, piece:Piece):
        moves=piece.defineMoves(piece.currentPosition)
        #print(moves)
        movesFinal=[]
        #kralj ne sme drugog kralja
        #da li kralj moze da se pomeri i sam sebe stavi u mat 
        #KING
        if(piece.pieceTypeId==1):
            for item in moves:
                if(self.board[item[0]][item[1]]==None and not(piece.currentPosition[0]+2==item[0] or 
                                                              piece.currentPosition[0]-2==item[0])):

                    movesFinal.append(item)

                elif(self.board[item[0]][item[1]]!=None and not(piece.currentPosition[0]+2==item[0] or 
                                                              piece.currentPosition[0]-2==item[0])):
                    p:Piece
                    p=self.board[item[0]][item[1]]
                    if(p.color != piece.color):
                        movesFinal.append(item)

                #kingside castling, queenside castling
                elif piece.moved==False:
                    flag=False
                    if self.board[0][piece.currentPosition[1]].moved==False and item[0]==3:
                        for i in range(1,4):
                            if(self.board[i][piece.currentPosition[1]]!=None):
                                flag=True

                        if flag==False:
                            movesFinal.append(item)

                    flag=False
                    if self.board[7][piece.currentPosition[1]].moved==False and item[0]==5:
                        for i in range(5,7):
                            if(self.board[i][piece.currentPosition[1]]!=None):
                                flag=True

                        if flag==False:
                            movesFinal.append(item)

               


        #QUEEN    
        elif(piece.pieceTypeId==2):
        #left-up
            for item in moves:
                if(item[0]<piece.currentPosition[0] and item[1]>piece.currentPosition[1]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break 
                    break  
        #left-down
            for item in moves:
                    if(item[0]<piece.currentPosition[0] and item[1]<piece.currentPosition[1]):
                        if(self.board[item[0]][item[1]]==None):
                            movesFinal.append(item)
                        else:
                            p=self.board[item[0]][item[1]]
                            if(p.color != piece.color):
                                movesFinal.append(item)
                                break
                        break
        #right-up
            for item in moves:
                    if(item[0]>piece.currentPosition[0] and item[1]>piece.currentPosition[1]):
                        if(self.board[item[0]][item[1]]==None):
                            movesFinal.append(item)
                        else:
                            p=self.board[item[0]][item[1]]
                            if(p.color != piece.color):
                                movesFinal.append(item)
                                break
                        break
        #right-down        
            for item in moves:
                    if(item[0]>piece.currentPosition[0] and item[1]<piece.currentPosition[1]):
                        if(self.board[item[0]][item[1]]==None):
                            movesFinal.append(item)
                        else:
                            p=self.board[item[0]][item[1]]
                            if(p.color != piece.color):
                                movesFinal.append(item)
                                break 
                        break
        #left
            for item in moves:
                if(item[0]<piece.currentPosition[0]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break  
                    break              
        #right
            for item in moves:
                if(item[0]>piece.currentPosition[0]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break  
                    break          
        #up
            for item in moves:
                if(item[1]>piece.currentPosition[1]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break     
                    break       
        #down
            for item in moves:
                if(item[1]<piece.currentPosition[1]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break
                    break

        #ROOK
        elif(piece.pieceTypeId==3):
            #left
            for item in moves:
                if(item[0]<piece.currentPosition[0]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break  
                    break              
            #right
            for item in moves:
                if(item[0]>piece.currentPosition[0]):
                    if(self.board[item[0]][item[1]]==None):
                        
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            
                            movesFinal.append(item)
                            break   
                    break        

                        
            #up
            for item in moves:
                if(item[1]>piece.currentPosition[1]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                        
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            
                            break
                    break            
            #down
            for item in moves:
                if(item[1]<piece.currentPosition[1]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break
                    break
            
        #KNIGHT
        elif(piece.pieceTypeId==4):
            for item in moves:
                if(self.board[item[0]][item[1]]==None):
                    movesFinal.append(item)
                else:
                    p:Piece
                    p=self.board[item[0]][item[1]]
                    if(p.color != piece.color):
                        movesFinal.append(item)
        
        #BISHOP
        elif(piece.pieceTypeId==5):
        #left-up
            for item in moves:
                if(item[0]<piece.currentPosition[0] and item[1]>piece.currentPosition[1]):
                    if(self.board[item[0]][item[1]]==None):
                        movesFinal.append(item)
                    else:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                            break   
                    break
        #left-down
            for item in moves:
                    if(item[0]<piece.currentPosition[0] and item[1]<piece.currentPosition[1]):
                        if(self.board[item[0]][item[1]]==None):
                            movesFinal.append(item)
                        else:
                            p=self.board[item[0]][item[1]]
                            if(p.color != piece.color):
                                movesFinal.append(item)
                                break
                        break
        #right-up
            for item in moves:
                    if(item[0]>piece.currentPosition[0] and item[1]>piece.currentPosition[1]):
                        if(self.board[item[0]][item[1]]==None):
                            movesFinal.append(item)
                        else:
                            p=self.board[item[0]][item[1]]
                            if(p.color != piece.color):
                                movesFinal.append(item)
                                break
                        break
        #right-down        
            for item in moves:
                    if(item[0]>piece.currentPosition[0] and item[1]<piece.currentPosition[1]):
                        if(self.board[item[0]][item[1]]==None):
                            movesFinal.append(item)
                        else:
                            p=self.board[item[0]][item[1]]
                            if(p.color != piece.color):
                                movesFinal.append(item)
                                break  
                        break          
        
        #an pasan
        #PAWN  
        else:
            for item in moves:
                #can it move two squares forward
                if(piece.currentPosition[1]+2==item[1] and piece.currentPosition[1]==1 and piece.color=="white"):
                    movesFinal.append(item)
                elif(piece.currentPosition[1]-2==item[1] and piece.currentPosition[1]==6 and piece.color=="black"):
                    movesFinal.append(item)
        
                else:
                    #Can it eat a figure, including both diagonally and horizontally
                    if(piece.currentPosition[0]!=item[0] or piece.currentPosition[1]==item[1])  and self.board[item[0]][item[1]]!=None:
                        p=self.board[item[0]][item[1]]
                        if(p.color != piece.color):
                            movesFinal.append(item)
                    elif self.board[item[0]][item[1]]==None and piece.currentPosition[0]==item[0]:
                          movesFinal.append(item)

        """izbrisano onaj segment sa checkom"""

        
        return movesFinal
    
        """nova funkcija"""
    def filtratedMoves(self,piece:Piece):
        movesFinalFinal=[]
        possibleMoves=self.showPossibleMoves(piece)
        cp=piece.currentPosition 
        self.board[cp[0]][cp[1]]=None       
        for m in possibleMoves:
            firstPiece=self.board[m[0]][m[1]] 
            if firstPiece != None:
                firstPiece.isDead=True
                
            piece.currentPosition=m
            self.board[m[0]][m[1]]=piece
            check=self.checkCheck()
            if piece.color=="white" and check[1]==0:
                movesFinalFinal.append(m)
            elif piece.color=="black" and check[0]==0:
                movesFinalFinal.append(m)

            piece.currentPosition=cp
            if firstPiece != None:
                firstPiece.isDead=False
            self.board[m[0]][m[1]]=firstPiece
            self.board[cp[0]][cp[1]]=piece
        
        return movesFinalFinal

    """dodate zagrade kod getPieces"""
    def checkCheck(self):
        #0,0 - no checks
        #1,0 - white checks black 
        #0,1 - black checks white
        check=(0,0)

        whitePlayer = database.getPlayer("Player1")
        blackPlayer = database.getPlayer("Player2")

        for pc in whitePlayer.pieces:
            if pc.isDead==False:
                moves=self.showPossibleMoves(pc)
                for m in moves:
                    if m==self.blackKing:
                        check[0]=1    

        for pc in blackPlayer.pieces:
            if pc.isDead==False:
                moves=self.showPossibleMoves(pc)
                for m in moves:
                    if m==self.whiteKing:
                        check[1]=1

        return check 


    def checkCheckmate(self,piece):
        whitePlayer = database.getPlayer("Player1", self.gameId)
        blackPlayer = database.getPlayer("Player2", self.gameId)

        if(piece.color=="white"):
            for pc in blackPlayer.pieces:
                moves=self.showPossibleMoves(pc)
                if len(moves)>0:
                    return False    
        else:
            for pc in whitePlayer.pieces:
                moves=self.showPossibleMoves(pc)
                if len(moves)>0:
                    return False         
        return True
    
    """promenjen parametar, nema *"""
    def makeMove(self,piece:Piece,nextPosition:List[int]):
        #nextPosition se uzima sa fronta!!
        #check who's turn by taking the log from the database
        #postavljena je vrednost white samo da ne bi bacalo gresku
        #nextMove="white"
        #checking if there is a castling and if so, moving the rook
        """kod druge ugaone zagrade falile ugaone zagrade [1]-1 i [1]+1"""
        if piece.pieceTypeId==1 and nextPosition[0]==piece.currentPosition[0]+2:
            self.board[nextPosition[0]][nextPosition[1]-1]=self.board[piece.currentPosition[0]][7]
            self.board[piece.currentPosition[0]][7]=None
        elif piece.pieceTypeId==1 and nextPosition[0]==piece.currentPosition[0]-2:
            self.board[nextPosition[0]][nextPosition[1]+1]=self.board[piece.currentPosition[0]][0]
            self.board[piece.currentPosition[0]][0]=None
        #removing piece out of the game
            """pisalo je piece.nextposition, treba bez piece"""
        if self.board[nextPosition[0]][nextPosition[1]] is not None:
            self.board[nextPosition[0]][nextPosition[1]].removePiece()
        #changing board
        self.board[piece.currentPosition[0]][piece.currentPosition[1]]=None
        self.board[nextPosition[0]][nextPosition[1]]=piece
        #updating position of the piece
        """obrisana * iz parametra"""
        piece.movePiece(nextPosition)
        #checking if the king was moved and in that case updating his position
        if(piece.pieceTypeId==1):
            if(piece.color=="white"):
                self.whiteKing=(nextPosition[0],nextPosition[1])
            else:
                self.blackKing=(nextPosition[0],nextPosition[1])
        #checking if the pawn has reached the end of the board
        if piece.pieceTypeId==6 and (nextPosition[1]==7 or nextPosition[1]==0):
            #uzimamo sa fronta novi tip, moze biti kraljica,top, lovac,konj
            #za kraljicu se vraca 2, za topa 3, za konja 4 i za lovca 5
            piece.swapPieceType(2)
        #checking if there is a check or checkmate
        check=self.checkCheck()
        """promenjen uslov"""
        if check[0]==1 or check[1]==1:
            checkmate=self.checkCheckmate()
            if checkmate:
                #game end
                pass
        #putting the log into the database

#if __name__ == "__main__":
    #print("main")
    #ovo smo mi koristile za proveru, probaj i ti tako
# p1=Player("Milica",None)
# p2=Player("Ana",None)
# g=Game(p1,p2)
    #database.addPlayer(p1)
    #database.addPlayer(p2)
    #pl1 = database.getPlayer(p1.name)
    #pl2 = database.getPlayer(p2.name)
    #print("pl1:",pl1.name)
    #print("pl2:",pl2.name)
    #p = Piece(2,(0,4),"white",1)
    #database.addGame(g)
    #g = database.getGame()
    #print("g.gameId:", g.gameId)
#g.printBoard()
    #print(p1.getPieces()[0])
    #pm=g.showPossibleMoves(p1.getPieces()[0])
    #print(pm)


    #currPosPawn = p1.getPieces()[0].currentPosition
    #p1.getPieces()[0].currentPosition = (5,5)
#currBoard=g.board[1][6]
    #c2 = g.board[2][6]
    #g.board[1][3]=currBoard
    #g.board[1][3].currentPosition = (1,3)
    #g.board[2][4]=c2

    #fm=g.filtratedMoves(g.board[1][3])
#pm=g.showPossibleMoves(currBoard)
    #newPos=(2,4)
    #g.makeMove(currBoard,newPos)
#print(pm)

    #g.printBoard()