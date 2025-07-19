
import dictionary

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
                self.game_controller.set_site(player.get_site())
        print("Gra rozpoczęta")
        self.game_controller.set_in_game(False)


    def deploy(self, data):
        unit_id = data['data']['unit']['id']
        site = data['data']['player']
        qrs = tuple(data['data']['unit']['qrs'])
        msg = data['data']['message']
        if site == 'Z':
            player = self.game.player_w
        elif site == 'C':
            player = self.game.player_s

        player.get_units()[unit_id].set_qrs(qrs)
        self.play.remove_reinforcement(unit_id)
        self.play.add_unit(site, unit_id, qrs)
        self.play.set_message(dictionary.message[msg])
        self.play.message_field.set_dirty()

                

        

