import socket
import database
from Game import Game
from Player import Player
from PieceType import PieceType
from Log import Log
from datetime import datetime
import json
import threading
import signal
import sys
from typing import List

p1 = Player("Player1", None)
p2 = Player("Player2", None)
game = Game(p1, p2)
database.addPlayer(p1)
database.addPlayer(p2)

turnNo = 1 
playersNo = 0

server_p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_p1.bind(('localhost', 1234))
server_p1.listen(1)

server_p2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_p2.bind(('localhost', 4321))
server_p2.listen(1)

conn_socket_p1 = None
conn_socket_p2 = None

thread_p1 = None
thread_p2 = None

def signal_handler(sig, frame):
    print("\nCtrl+C pressed. Exiting gracefully...")
    #thread_p1.join()
    #thread_p2.join()
    sys.exit(0)

def game_setup():
    print("Setting up the game...")
    king_p_t = PieceType(1, "King")
    queen_p_t = PieceType(2, "Queen")
    rook_p_t = PieceType(3, "Rook")
    knight_p_t = PieceType(4, "Knight")
    bishop_p_t = PieceType(5, "Bishop")
    pawn_p_t = PieceType(6, "Pawn")
    pieceTypes = [king_p_t, queen_p_t, rook_p_t, knight_p_t, bishop_p_t, pawn_p_t]
    database.addPieceTypes(pieceTypes)

def get_white_pieces():
    w_pawn1 = database.getPiece("w_pawn1", game.gameId)
    w_pawn2 = database.getPiece("w_pawn2", game.gameId)
    w_pawn3 = database.getPiece("w_pawn3", game.gameId)
    w_pawn4 = database.getPiece("w_pawn4", game.gameId)
    w_pawn5 = database.getPiece("w_pawn5", game.gameId)
    w_pawn6 = database.getPiece("w_pawn6", game.gameId)
    w_pawn7 = database.getPiece("w_pawn7", game.gameId)
    w_pawn8 = database.getPiece("w_pawn8", game.gameId)

    w_rook1 = database.getPiece("w_rook1", game.gameId)
    w_rook2 = database.getPiece("w_rook2", game.gameId)

    w_bishop1 = database.getPiece("w_bishop1", game.gameId)
    w_bishop2 = database.getPiece("w_bishop2", game.gameId)

    w_knight1 = database.getPiece("w_knight1", game.gameId)
    w_knight2 = database.getPiece("w_knight2", game.gameId)

    w_king = database.getPiece("w_king", game.gameId)
    w_queen = database.getPiece("w_queen", game.gameId)
    return w_pawn1,w_pawn2,w_pawn3,w_pawn4,w_pawn5,w_pawn6,w_pawn7,w_pawn8,w_rook1,w_rook2,w_bishop1,w_bishop2,w_knight1,w_knight2,w_king,w_queen

def get_black_pieces():
    b_pawn1 = database.getPiece("b_pawn1", game.gameId)
    b_pawn2 = database.getPiece("b_pawn2", game.gameId)
    b_pawn3 = database.getPiece("b_pawn3", game.gameId)
    b_pawn4 = database.getPiece("b_pawn4", game.gameId)
    b_pawn5 = database.getPiece("b_pawn5", game.gameId)
    b_pawn6 = database.getPiece("b_pawn6", game.gameId)
    b_pawn7 = database.getPiece("b_pawn7", game.gameId)
    b_pawn8 = database.getPiece("b_pawn8", game.gameId)

    b_rook1 = database.getPiece("b_rook1", game.gameId)
    b_rook2 = database.getPiece("b_rook2", game.gameId)

    b_bishop1 = database.getPiece("b_bishop1", game.gameId)
    b_bishop2 = database.getPiece("b_bishop2", game.gameId)

    b_knight1 = database.getPiece("b_knight1", game.gameId)
    b_knight2 = database.getPiece("b_knight2", game.gameId)

    b_king = database.getPiece("b_king", game.gameId)
    b_queen = database.getPiece("b_queen", game.gameId)
    return b_pawn1,b_pawn2,b_pawn3,b_pawn4,b_pawn5,b_pawn6,b_pawn7,b_pawn8,b_rook1,b_rook2,b_bishop1,b_bishop2,b_knight1,b_knight2,b_king,b_queen

def start_game_p1():
    try:
        game_json = json.dumps({'game': 'wait'})
        return game_json
    except Exception as e:
        print(f"Error: {e}")

def start_game_p2():
    try:
        global game
        global playersNo

        playersNo = 0

        player1 = Player("Player1", None)
        player2 = Player("Player2", None)
        new_game = Game(player1, player2)

        database.addGame(new_game)
        #game = database.getGame(new_game.gameId)
        game = new_game

        print("gameId:",game.gameId)
        
        #game_json = json.dumps({'game': game.gameId})

        w_pawn1,w_pawn2,w_pawn3,w_pawn4,w_pawn5,w_pawn6,w_pawn7,w_pawn8,w_rook1,w_rook2,w_bishop1,w_bishop2,w_knight1,w_knight2,w_king,w_queen = get_white_pieces()
        b_pawn1,b_pawn2,b_pawn3,b_pawn4,b_pawn5,b_pawn6,b_pawn7,b_pawn8,b_rook1,b_rook2,b_bishop1,b_bishop2,b_knight1,b_knight2,b_king,b_queen = get_black_pieces()

        #next_move = ""

        #if turnNo != 1:
        #    last_log = database.getLogByTurnNo(turnNo, game.gameId)
        #    next_move = last_log.next_move
        #else:
        #    next_move = "white"
        
        board_json = json.dumps({"game": game.gameId,
                                 "w_pawn1": w_pawn1.currentPosition,
                                 "w_pawn2": w_pawn2.currentPosition,
                                 "w_pawn3": w_pawn3.currentPosition,
                                 "w_pawn4": w_pawn4.currentPosition,
                                 "w_pawn5": w_pawn5.currentPosition,
                                 "w_pawn6": w_pawn6.currentPosition,
                                 "w_pawn7": w_pawn7.currentPosition,
                                 "w_pawn8": w_pawn8.currentPosition,
                                 "w_rook1": w_rook1.currentPosition,
                                 "w_rook2": w_rook2.currentPosition,
                                 "w_bishop1": w_bishop1.currentPosition,
                                 "w_bishop2": w_bishop2.currentPosition,
                                 "w_knight1": w_knight1.currentPosition,
                                 "w_knight2": w_knight2.currentPosition,
                                 "w_king": w_king.currentPosition,
                                 "w_queen": w_queen.currentPosition,

                                 "b_pawn1": b_pawn1.currentPosition, 
                                 "b_pawn2": b_pawn2.currentPosition,
                                 "b_pawn3": b_pawn3.currentPosition,
                                 "b_pawn4": b_pawn4.currentPosition,
                                 "b_pawn5": b_pawn5.currentPosition,
                                 "b_pawn6": b_pawn6.currentPosition,
                                 "b_pawn7": b_pawn7.currentPosition,
                                 "b_pawn8": b_pawn8.currentPosition,
                                 "b_rook1": b_rook1.currentPosition,
                                 "b_rook2": b_rook2.currentPosition,
                                 "b_bishop1": b_bishop1.currentPosition,
                                 "b_bishop2": b_bishop2.currentPosition,
                                 "b_knight1": b_knight1.currentPosition,
                                 "b_knight2": b_knight2.currentPosition,
                                 "b_king": b_king.currentPosition,
                                 "b_queen": b_queen.currentPosition})
        print("board_json_start:",board_json)
        return board_json
    except Exception as e:
        return f"Error: {e}", 500

def define_moves(piece_name):
    try:
        print("Piece name from Unity:",piece_name)
        piece = database.getPiece(piece_name, game.gameId)
        moves = game.filtratedMoves(piece)
        #jsonify
        #return jsonify({'moves': moves})

        moves_json = json.dumps({"moves": moves})
        print("moves_json:", moves_json)
        return moves_json
    except Exception as e:
        return f"Error: {e}", 500

def make_move(piece_name, x, y):
    try:
        global game
        global turnNo

        print("Piece name from Unity:",piece_name)
        print("x:",x)
        print("y:",y)

        piece = database.getPiece(piece_name, game.gameId)
        print("piece.position1:",piece.currentPosition)

        print("turnNo:",turnNo)

        next_position = [int(x), int(y)]

        game.makeMove(piece, next_position)

        database.updatePiece(piece, piece_name, game.gameId)
        piece = database.getPiece(piece_name, game.gameId)

        print("piece.position2:",piece.currentPosition)
        
        # treba li updateGame()?
        #gameToUpdate = database.getGame(game.gameId)
        #gameId = game.gameId
        #print("gameId1:",gameId)
        #updatedGame = game
        #print("gameId2:",updatedGame.gameId)
        #database.updateGame(updatedGame)
        #game = updatedGame
        turnNo = turnNo + 1

        log = Log(turnNo, game.board, datetime.now(), game.gameId)
        database.addLog(log, game.gameId)

        w_pawn1,w_pawn2,w_pawn3,w_pawn4,w_pawn5,w_pawn6,w_pawn7,w_pawn8,w_rook1,w_rook2,w_bishop1,w_bishop2,w_knight1,w_knight2,w_king,w_queen = get_white_pieces()
        b_pawn1,b_pawn2,b_pawn3,b_pawn4,b_pawn5,b_pawn6,b_pawn7,b_pawn8,b_rook1,b_rook2,b_bishop1,b_bishop2,b_knight1,b_knight2,b_king,b_queen = get_black_pieces()
        
        board_json = json.dumps({
                                "w_pawn1": w_pawn1.currentPosition, 
                                "w_pawn2": w_pawn2.currentPosition,
                                "w_pawn3": w_pawn3.currentPosition,
                                "w_pawn4": w_pawn4.currentPosition,
                                "w_pawn5": w_pawn5.currentPosition,
                                "w_pawn6": w_pawn6.currentPosition,
                                "w_pawn7": w_pawn7.currentPosition,
                                "w_pawn8": w_pawn8.currentPosition,
                                "w_rook1": w_rook1.currentPosition,
                                "w_rook2": w_rook2.currentPosition,
                                "w_bishop1": w_bishop1.currentPosition,
                                "w_bishop2": w_bishop2.currentPosition,
                                "w_knight1": w_knight1.currentPosition,
                                "w_knight2": w_knight2.currentPosition,
                                "w_king": w_king.currentPosition,
                                "w_queen": w_queen.currentPosition,

                                "b_pawn1": b_pawn1.currentPosition, 
                                "b_pawn2": b_pawn2.currentPosition,
                                "b_pawn3": b_pawn3.currentPosition,
                                "b_pawn4": b_pawn4.currentPosition,
                                "b_pawn5": b_pawn5.currentPosition,
                                "b_pawn6": b_pawn6.currentPosition,
                                "b_pawn7": b_pawn7.currentPosition,
                                "b_pawn8": b_pawn8.currentPosition,
                                "b_rook1": b_rook1.currentPosition,
                                "b_rook2": b_rook2.currentPosition,
                                "b_bishop1": b_bishop1.currentPosition,
                                "b_bishop2": b_bishop2.currentPosition,
                                "b_knight1": b_knight1.currentPosition,
                                "b_knight2": b_knight2.currentPosition,
                                "b_king": b_king.currentPosition,
                                "b_queen": b_queen.currentPosition})

        print("board_json_make_move:",board_json)
        return board_json
    except Exception as e:
        print("Error make_move:", e)
        return "invalid"
    
def socket_p2():
    global conn_socket_p1
    global conn_socket_p2
    global turnNo
    while True:
        conn_socket_p2, addr = server_p2.accept()
        cs_coded = conn_socket_p2.recv(1024)
        response = cs_coded.decode()
        print("response_p2:", response)
        parts = response.split("-")
        method = parts[0]
        print("method:",method)
        if method == "start":
            turnNo = 0
            message = start_game_p2()
            print("Sending board to p1")
            print("Sending board to p2")
            conn_socket_p1.sendall(message.encode('utf-8'))
            conn_socket_p2.sendall(message.encode('utf-8'))
        elif method == "defineMoves":
            piece_name = parts[1]
            message = define_moves(piece_name)
            conn_socket_p2.sendall(message.encode('utf-8'))
        elif method == "makeMove":
            piece_name = parts[1]
            x = parts[2]
            y = parts[3]
            message = make_move(piece_name, x, y)
            conn_socket_p2.sendall(message.encode('utf-8'))
            conn_socket_p1.sendall(message.encode('utf-8'))

def socket_p1():
    global conn_socket_p1
    global conn_socket_p2
    while True:
        conn_socket_p1, addr = server_p1.accept()
        cs_coded = conn_socket_p1.recv(1024)
        response = cs_coded.decode()
        print("response_p1:", response)
        parts = response.split("-")
        method = parts[0]
        if method == "start":
            message = start_game_p1()
            conn_socket_p1.sendall(message.encode('utf-8'))
        elif method == "defineMoves":
            piece_name = parts[1]
            message = define_moves(piece_name)
            conn_socket_p1.sendall(message.encode('utf-8'))
        elif method == "makeMove":
            piece_name = parts[1]
            x = parts[2]
            y = parts[3]
            message = make_move(piece_name, x, y)
            conn_socket_p1.sendall(message.encode('utf-8'))
            conn_socket_p2.sendall(message.encode('utf-8'))

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    game_setup()

    thread_p1 = threading.Thread(target=socket_p1)
    thread_p2 = threading.Thread(target=socket_p2)
    
    thread_p1.start()
    thread_p2.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
