import gamelogic
import player
import board

class MessageFromClient(object):

    
    def create_game(self, clientSocket, data, serverCon):
        login = data.get('login')
        site = data.get('site')              
        name = gamelogic.GameLogic.describeName(site)
        spellPower = gamelogic.GameLogic.describeSpellPower(site)
        player_ = player.Player(name, site, login, spellPower, clientSocket)
        player_.setUnits(player_.createArmy(site, serverCon))
        player_.shuffle()
        board_ = board.Board()
        return(player_, board_)
    
  
    def openSessionsGame(self, serverSessions):
            sessions = []
            for sessionID, sessionData in serverSessions.items():
                if len(sessionData['players']) == 1:
                    player = sessionData['players'][0]
                    sessions.append({
                        'sesja': sessionID,
                        'gracz': player.login,
                        'jako': player.name,            
                    })
            return sessions
    
    def prepareSecondPlayer(self, clientSocket, data, serverSessions):
        sessionID = data.get('sessionID')
        login = data.get('login')          
        site = 'Z' if serverSessions[sessionID]['players'][0].site == 'C' else 'C'
        name = gamelogic.GameLogic.describeName(site)
        spellPower = gamelogic.GameLogic.describeSpellPower(site)
        player_ = player.Player(name, site, login, spellPower, clientSocket)
        player_.setUnits(player_.createArmy(site, serverSessions[sessionID]['handler']))
        player_.shuffle()
        return player_
    
    
    def isFull(self, serverSessions, sessionID):
        if len(serverSessions[sessionID]['players']) >= 2:
            return True
        return False
    
    
    def startGame(self, players, board):
        playerW = None
        playerS = None
        for player_ in players:
            if player_.site == 'Z':
                playerW = player_
            else:
                playerS = player_
        parcel = {
            'playerW': playerW.to_dict(),
            'playerS': playerS.to_dict(),
            'board': board.to_dict()
            }
        return parcel


                        
                       