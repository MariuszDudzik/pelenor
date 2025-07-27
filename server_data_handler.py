from email.mime import message
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


    def check_right_turn(self, server_session, site, stage, phaze):
        if server_session['handler'].get_akt_player() == site:
            if stage == server_session['handler'].get_akt_stage() and phaze == server_session['handler'].get_akt_phaze():
                return True
        return False
    

    def error_parcel(self, message):
        parcel = {'message': message}
        return parcel
    

    def handle_deploy(self, site, server_session, unit_id, qrs, stage, phaze, flag, old_qrs=None):

        units = gamelogic.GameLogic.get_units_for_player(site, server_session['players'][0], server_session['players'][1])
        akt_movement = gamelogic.GameLogic.set_akt_movement_after_deploy(unit_id, units, stage, server_session['arena'],qrs, site)
        units[unit_id].set_deploy()
        units[unit_id].set_qrs(qrs)
        units[unit_id].set_akt_movement(akt_movement)
        server_session['arena'].hexes[qrs].pawn_list.append(unit_id)
        
        parcel = {
            'player': site,
            'phaze': phaze,
            'flag': flag,
            'unit': [{
                'id': unit_id,
                'deploy': True,
                'qrs': qrs,
                'akt_movement': akt_movement
                }],
            'hex': [{
                'qrs': qrs,
                'unit_add': True,
                'unit_remove': False
            }],
            'message': 12
            }
        if flag == 'U':
            parcel['hex'].append({
                'qrs': old_qrs,
                'unit_add': False,
                'unit_remove': True
            })
        return parcel

    def deploy_unit(self, server_session, data):
        site = data.get('site')
        stage = data.get('stage')
        phaze = data.get('phaze')
        unit_id = data.get('unit_id')
        qrs = tuple(data.get('qrs'))
        flag = data.get('flag')

        if not self.check_right_turn(server_session, site, stage, phaze):
            return self.error_parcel(11)
        if not server_session['handler'].get_deploy():
            return self.error_parcel(11)
        
        check, message = gamelogic.GameLogic.base_deploy(unit_id, site, qrs, phaze, server_session['arena'],server_session['players'][0], server_session['players'][1])
        if not check:
            return self.error_parcel(message)
        
        old_qrs = None
        if flag == 'U':
            old_qrs = gamelogic.GameLogic.get_unit_qrs(unit_id, server_session['players'][0], server_session['players'][1]) 
            check, message = gamelogic.GameLogic.check_commander_not_alone(unit_id, old_qrs, server_session['arena'], server_session['players'][0], server_session['players'][1], message)
            if not check:
                return self.error_parcel(message)

            if stage == 0 and site == 'Z':
                check, message = gamelogic.GameLogic.check_palace_gward(unit_id, server_session['arena'], server_session['players'][0], server_session['players'][1], message)
                if not check:
                    return self.error_parcel(message)

            server_session['arena'].hexes[old_qrs].pawn_list.remove(unit_id)

        parcel = self.handle_deploy(site, server_session, unit_id, qrs, stage, phaze, flag, old_qrs)
        return parcel
   
                        
    def end_turn(self, server_session, data):
        site = data.get('site')
        stage = data.get('stage')
        phaze = data.get('phaze')
        if self.check_right_turn(server_session, site, stage, phaze):
            if phaze == 0:
                deployed = gamelogic.GameLogic.chceck_if_deployed(site, stage, server_session['players'][0], server_session['players'][1])
                if deployed:
                    if site == 'C':
                        server_session['handler'].set_akt_player('Z')
                        parcel = {'game': {'akt_player': 'Z', 'phaze': 0, 'stage': 0, 'deploy': True},
                                    'message': 1
                                    }
                        
                        units = gamelogic.GameLogic.get_units_for_player('Z', server_session['players'][0], server_session['players'][1])
                        unit_id = None
                        for unit in units.values():
                            if unit.get_name() == "Gwardia pałacowa":
                                unit_id = unit.get_id()
                                break

                        parcel2 = self.handle_deploy('Z', server_session, unit_id, (18, -7, -11), stage, phaze, 'R', None)
                        return parcel, parcel2
                    else:
                        server_session['handler'].set_akt_stage(1)
                        server_session['handler'].set_akt_phaze(1)
                        server_session['handler'].set_deploy(False)
                        parcel = {'game': {'akt_player': 'Z', 'phaze': 1, 'stage': 1, 'deploy': False},
                                    'message': 7
                                    }
                        parcel2 = None
                        return parcel, parcel2
                else:
                    parcel = {'message': 21}
                    parcel2 = None
                    return parcel, parcel2
