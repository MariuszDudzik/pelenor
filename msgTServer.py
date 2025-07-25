import json
import struct

class MsgTServer(object):
    def __init__(self, game_controller, game):
        self.game_controller = game_controller
        self.game = game


    def _send_request(self, action, payload, client_socket):
        request = json.dumps({
            'action': action,
            **payload  # Łączy zawartość słownika `payload` z akcją
        }, ensure_ascii=False)
        
        request_bytes = request.encode('utf-8')
        request_length = len(request_bytes)
        client_socket.sendall(struct.pack('!I', request_length))
        client_socket.sendall(request_bytes)

    def ping(self, client_socket): 
        payload = {
        'session_id': self.game_controller.get_session_id()
        }
        self._send_request('ping', payload, client_socket)


    def create_game(self, client_socket): 
        payload = {
        'login': self.game_controller.get_login(),
        'site': self.game_controller.get_chosen_site()
        }
        self._send_request('create_game', payload, client_socket)


    def list_sessions(self, client_socket):
        payload = {}
        self._send_request('list_sessions', payload, client_socket)


    def join_game(self, client_socket):
        payload = {
            'session_id': self.game_controller.get_marked_session_id(),
            'login': self.game_controller.get_login()
        }
        self._send_request('join_game', payload, client_socket)


    def deploy(self, session_id, client_socket, site, stage, phaze, unit_id, qrs, flag):

        payload = {
            'session_id': session_id,
            'site': site,
            'stage': stage,
            'phaze': phaze,
            'unit_id': unit_id,
            'qrs': qrs,
            'flag': flag
        }
        self._send_request('deploy', payload, client_socket)


    def end_turn(self, session_id, client_socket, site, stage, phaze):
        payload = {
            'session_id': session_id,
            'site': site,
            'stage': stage,
            'phaze': phaze,
            
        }
        self._send_request('end_turn', payload, client_socket)
