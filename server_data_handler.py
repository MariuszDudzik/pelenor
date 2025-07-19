import gamelogic
import player
import board

class MsgFClient(object):

    
    def create_game(self, client_socket, data, server_con):
        login = data.get('login')
        site = data.get('site')              
        name = gamelogic.GameLogic.describe_name(site)
        spell_power = gamelogic.GameLogic.describe_spell_power(site)
        player_ = player.Player(name, site, login, spell_power, client_socket)
        player_.set_units(player_.create_army(site, server_con))
        player_.shuffle()
        board_ = board.Board()
        return(player_, board_)


    def open_sessions_game(self, server_sessions):
            sessions = []
            for session_id, session_data in server_sessions.items():
                if len(session_data['players']) == 1:
                    player = session_data['players'][0]
                    sessions.append({
                        'sesja': session_id,
                        'gracz': player.login,
                        'jako': player.name,            
                    })
            return sessions

    def prepare_second_player(self, client_socket, data, server_sessions):
        session_id = data.get('session_id')
        login = data.get('login')
        site = 'Z' if server_sessions[session_id]['players'][0].site == 'C' else 'C'
        name = gamelogic.GameLogic.describe_name(site)
        spell_power = gamelogic.GameLogic.describe_spell_power(site)
        player_ = player.Player(name, site, login, spell_power, client_socket)
        player_.set_units(player_.create_army(site, server_sessions[session_id]['handler']))
        player_.shuffle()
        return player_


    def is_full(self, server_sessions, session_id):
        if len(server_sessions[session_id]['players']) >= 2:
            return True
        return False


    def start_game(self, players, board):
        player_w = None
        player_s = None
        for player_ in players:
            if player_.site == 'Z':
                player_w = player_
            else:
                player_s = player_
        parcel = {
            'player_w': player_w.to_dict(),
            'player_s': player_s.to_dict(),
            'board': board.to_dict()
            }
        return parcel


    def deploy_unit(self, server_session, data):
        site = data.get('site')
        stage = data.get('stage')
        phaze = data.get('phaze')
        unit_id = data.get('unit_id')
        qrs = tuple(data.get('qrs'))
        if server_session['handler'].get_akt_player() == site:
            if stage == server_session['handler'].get_akt_stage() and phaze == server_session['handler'].get_akt_phaze():
                if server_session['handler'].get_deploy():
                    if gamelogic.GameLogic.base_deploy(unit_id, site, qrs, server_session['arena'].hexes[qrs].get_terrain_sign(), phaze, server_session['arena'], 's', server_session['players']):
                        for player in server_session['players']:
                            if player.get_site() == site:
                                if unit_id in player.get_units():
                                    player.get_units()[unit_id].set_deploy()
                                    player.get_units()[unit_id].set_qrs(qrs)
                                    server_session['arena'].hexes[qrs].pawn_list.append(unit_id)
                                    if stage != 0:
                                        pass
                                        #dopisac pomniejszenie ruchu jednostki
                                    parcel = {
                                        'player': site,
                                        'unit': {
                                            'id': unit_id,
                                            'deploy': True,
                                            'qrs': qrs
                                            },
                                        'message': 12
                                        }
                                    return parcel
                        
                       