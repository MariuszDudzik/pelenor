
import dictionary
import play_handler

class MsgFServer(object):
    def __init__(self, game_controller, game, eventbus):
        self.game_controller = game_controller
        self.game = game
        self.eventbus = eventbus
        self.play = None


    def set_play(self, play):
        self.play = play


    def server_response_handle(self, data):
        if 'action' in data:
            action = data['action']      
            match action:
                case 'game_created':
                    self.game_created(data)
                case 'list_sessions':
                    self.list_sessions(data)
                case 'joined_game':
                    self.joined_game(data)
                case 'start_game':
                    self.start_game(data)
                case 'deploy':
                    self.deploy(data)
                case 'end_turn':
                    self.end_turn(data)


    def game_created(self, data):
        if 'session_id' in data:
            self.game_controller.set_session_id(data['session_id'])
            self.list_sessions(data)
            return ("Czekam na dołączenie drugiego gracza...")
        else:
            return (f"Błąd przy tworzeniu gry: {data.get('error', 'Nieznany błąd')}")
        

    def list_sessions(self, data):
            self.game_controller.set_open_sessions(data['sessions'])
            self.eventbus.emit("sessions_updated", data['sessions'])


    def joined_game(self, data):
        if 'session_id' in data:
            self.game_controller.set_session_id(data['session_id'])
            self.eventbus.emit("sessions_updated", self.game_controller.get_open_sessions())
            print(f"Dołączono do gry: {self.game_controller.get_session_id()}")
        else:
            print(f"Nie można dołączyć do gry: {data.get('error', 'Nieznany błąd')}")


    def start_game(self, data):  
        player_data = data['data']['player_w']
        self.game.player_w.from_dict(player_data)
        player_data = data['data']['player_s']
        self.game.player_s.from_dict(player_data)
        player_data = data['data']['board']
        self.game.board.from_dict(player_data)
        for player in [self.game.player_w, self.game.player_s]:
            if player.get_login() == self.game_controller.get_login():
                self.game_controller.set_chosen_site(player.get_site())
        print("Gra rozpoczęta")
        self.game_controller.set_in_game(False)


    def deploy(self, data):
        msg = data['data']['message']
        if 'unit' in data['data']:
            flag = data['data']['flag']
            site = data['data']['player']
            if site == 'Z':
                player = self.game.player_w
            elif site == 'C':
                player = self.game.player_s
            for unit in data['data']['unit']:
                unit_id = unit['id']
                qrs = tuple(unit['qrs'])
             
                player.get_units()[unit_id].set_qrs(qrs)
                if flag == 'R':
                    self.play.remove_reinforcement(unit_id)
                    self.play.add_unit(site, unit_id, qrs)
                if flag == 'U':
                    self.play.remove_unit(unit_id)
                    self.play.add_unit(site, unit_id, qrs)
                    for hex in data['data']['hex']:
                        if hex['unit_remove']:
                            self.play.game.board.hexes[tuple(hex['qrs'])].pawn_list.remove(unit_id)
                            self.play.game.board.hexes[tuple(hex['qrs'])].pawn_graph_list.remove(unit_id)
                            self.play.hex[tuple(hex['qrs'])].set_dirty()

        self.play.set_message(dictionary.message[msg])
        self.play.message_field.set_dirty()


    def end_turn(self, data):
        msg = data['data']['message']
        if 'game' in data['data']:
            game_data = data['data']['game']
            stage = game_data['stage']
            phaze = game_data['phaze']
            akt_player = game_data['akt_player']
            self.game_controller.set_akt_stage(stage)
            self.game_controller.set_akt_phaze(phaze)
            self.game_controller.set_akt_player(akt_player)
            if phaze == 0 and akt_player == 'Z':
                play_handler.PlayHandler.change_hex_colour_handler(self.play, True, 'C', 0)
                play_handler.PlayHandler.change_hex_colour_handler(self.play, False, 'Z', 0)

        self.play.set_message(dictionary.message[msg])
        self.play.message_field.set_dirty()
