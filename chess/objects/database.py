from ZODB import DB
from ZEO.ClientStorage import ClientStorage
import transaction
from typing import List
import threading
from persistent.mapping import PersistentMapping

lock = threading.Lock()

def getLogsByGameId(gameId):
    with lock:
        logs = []
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        try:
            valid_game_id = False
            game_keys = root['games'].keys()
            for key in game_keys:
                if key == gameId:
                    valid_game_id = True
            if valid_game_id == True:
                for log_entry in root['logs'].keys():
                    parts = log_entry.split('_')
                    id = parts[0]
                    if id == gameId:
                        root['logs'][log_entry].turnNo
                        logs.append(root['logs'][log_entry])
            else:
                print("DB: Game with Id:", gameId, "not in the database")
        except Exception as e:
            print(f"DB: Error while reading logs: {e}")
        finally:
            connection.close()
            db.close()

        return logs

def getLogByTurnNo(turnNo, gameId):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        try:
            valid_game_id = False
            game_keys = root['games'].keys()
            for key in game_keys:
                if key == gameId:
                    valid_game_id = True
            if valid_game_id == True:
                object_name = str(gameId)+'_log_'+str(turnNo)
                log = root['logs'][object_name]
                log.turnNo
                return log
            else:
                print("DB: Game with Id:", gameId, "not in the database")
        except Exception as e:
            print(f"DB: Error while reading log: {e}")
        finally:
            connection.close()
            db.close()

def getGame(gameId):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()
        games = root['games'].values()

        try:
            for game in games:
                if game.gameId == gameId:
                    return game
        except Exception as e:
            print(f"DB: Error while reading object game: {e}")
        finally:
            connection.close()
            db.close()

def getPlayer(playerName):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        try:
            player = root['players'][playerName]
            player.id
        except Exception as e:
            print(f"DB: Error while reading object {playerName}: {e}")
        finally:
            connection.close()
            db.close()

        return player

def getPiece(pieceName, gameId):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        try:
            object_name = str(gameId)+'_piece_'+pieceName
            piece = root['pieces'][object_name]
            piece.color
        except Exception as e:
            print(f"DB: Error while reading object {pieceName}: {e}")
        finally:
            connection.close()
            db.close()

        return piece

def getPieceTypes():
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        try:
            pieceTypes = list(root['piece_types'].values())
            pieceTypes[0].typeid
        except Exception as e:
            print(f"DB: Error while reading object pieceType: {e}")
        finally:
            connection.close()
            db.close()

        return pieceTypes

def addLog(log, gameId):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()
        
        try:
            valid_game_id = False
            game_keys = root['games'].keys()
            for key in game_keys:
                if key == gameId:
                    valid_game_id = True
            if valid_game_id == True:
                with transaction.manager:
                    object_name = str(gameId)+'_log_'+str(log.turnNo)
                    root['logs'][object_name] = log

                print("DB: New Log entry added")
            else:
                print("DB: Given invalid game id")
        except Exception as e:
            print(f"DB: Error while adding log: {e}")
            transaction.abort()
        finally:
            connection.close()
            db.close()

def addGame(game):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        try:
            if 'games' not in root:
                with transaction.manager:
                    root['games'] = PersistentMapping()
                    root['logs'] = PersistentMapping()

            with transaction.manager:
                root['games'][game.gameId] = game
            
            print("DB: Game with id", game.gameId, "added")
            
        except Exception as e:
            print(f"DB: Error during transaction: {e}")
            transaction.abort()
        finally:
            connection.close()
            db.close()

def updateGame(game):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        with transaction.manager:
            root['games'][game.gameId] = game
            
        print("DB: Game with id", game.gameId, "updated")

        try:
            updatedGame = root['games'][game.gameId]
            return updatedGame
        except Exception as e:
            print(f"DB: Error while reading object game: {e}")
        finally:
            connection.close()
            db.close()

def addPlayer(player):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        if 'players' not in root:
            with transaction.manager:
                root['players'] = PersistentMapping()

        with transaction.manager:
            root['players'][player.name] = player
        
        print("DB:",player.name, "added")

        connection.close()
        db.close()

def addPieces(pieces:List[any], namesOfPieces, gameId):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        if 'pieces' not in root:
                with transaction.manager:
                    root['pieces'] = PersistentMapping()

        for i, piece in enumerate(pieces):
            with transaction.manager:
                object_name = str(gameId)+'_piece_'+str(namesOfPieces[i])
                root['pieces'][object_name] = piece

        print("DB: Pieces added")

        connection.close()
        db.close()

def updatePiece(piece, piece_name, gameId):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        with transaction.manager:
            object_name = str(gameId)+'_piece_'+piece_name
            root['pieces'][object_name] = piece

        print("DB: Piece", piece_name ,"updated")

        connection.close()
        db.close()

def addPieceTypes(pieceTypes:List[any]):
    with lock:
        storage = ClientStorage( ( 'localhost', 8090 ) )
        db = DB(storage)
        connection = db.open()
        root = connection.root()

        if 'piece_types' not in root:
                with transaction.manager:
                    root['piece_types'] = PersistentMapping()

        for pieceType in pieceTypes:
            with transaction.manager:
                root['piece_types'][pieceType.typename] = pieceType

        print("DB: Piece types added")

        connection.close()
        db.close()
