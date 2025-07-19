import control_obj
import kolor
import sys
import pygame
import support

class Menu(object):

    def __init__(self, screen, game_controller, connection, eventbus):

        self.screen = screen
        self.game_controller = game_controller
        self.connection = connection
        self.graphics = pygame.sprite.LayeredDirty()
        self.eventbus = eventbus
        
                 
        self.choice_s_button = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.14, 
            screen.get_height() / 3 - screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.DGREY, "Sauron", game_controller.get_default_font(), int(screen.get_height() * 0.035), kolor.WHITE, 
            self.choice_s_button_lc, None, None, None, None, None)    
        self.choice_w_button = control_obj.Button(screen.get_width() / 2 + screen.get_width() * 0.014, 
            screen.get_height() / 3 - screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.DGREY, "Westerneńczyk", game_controller.get_default_font(), int(screen.get_height() * 0.035), kolor.WHITE, self.choice_w_button_lc, None, None, None, None, None)
        self.create_button = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.07, 
            screen.get_height() / 3, screen.get_width() * 0.14, screen.get_height() * 0.065, kolor.BLUE, "Stwórz Grę", 
            game_controller.get_default_font(), int(screen.get_height() * 0.035), kolor.WHITE, self.create_game, None, None, None, None, None)
        self.join_button = control_obj.Button(screen.get_width() / 2 + screen.get_width() * 0.014, 
            screen.get_height() / 3 + screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.GREEN, "Dołącz do Gry", game_controller.get_default_font(), int(screen.get_height() * 0.035), kolor.WHITE, self.join_game,  None, None, None, None, None)   
        self.exit_button = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.07, 
            screen.get_height() / 3 + screen.get_height() * 0.45, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.RED, "Zakończ", game_controller.get_default_font(), int(screen.get_height() * 0.035), kolor.WHITE, self.exit_game, None, None, None, None, None)
        self.login_label = control_obj.Label(screen.get_width() / 2 - screen.get_width() * 0.15, 
            screen.get_height() / 3 - screen.get_height() * 0.15, screen.get_width() * 0.08, screen.get_height() * 0.032, 
            kolor.BLACK, "Wpisz login:", game_controller.get_default_font(), int(screen.get_height() * 0.025), kolor.WHITE, None, None, None, None, None, None)
        self.login_text = control_obj.TextBox(screen.get_width() / 2 - screen.get_width() * 0.07, 
            screen.get_height() / 3 - screen.get_height() * 0.15, screen.get_width() * 0.14, screen.get_height() * 0.032, 
            kolor.GREY, "", game_controller.get_default_font(), int(screen.get_height() * 0.025), kolor.BLACK, self.login_text_active, None, None, None, None, None, kolor.WHITE,)
        self.session_label = control_obj.LabelWithScroll(screen.get_width() / 2 - screen.get_width() * 0.175, 
            screen.get_height() / 3 + screen.get_height() * 0.18, screen.get_width() * 0.37, screen.get_height() * 0.16, 
            kolor.GREY, "", game_controller.get_default_font(), int(screen.get_height() * 0.025), kolor.BLACK, self.choose_session, None, self.set_scroll_offset_up, self.set_scroll_offset_down, None, None)
        self.count_session_label = control_obj.Label(screen.get_width() / 2 - screen.get_width() * 0.175, 
            screen.get_height() / 3 + screen.get_height() * 0.345, screen.get_width() * 0.37, screen.get_height() * 0.032, kolor.GREY, f"Liczba dostępnych sesji: {self.game_controller.get_count_open_sessions()}", 
            game_controller.get_default_font(), int(screen.get_height() * 0.025), kolor.BLACK, None, None, None, None, None, None)
        self.show_session_button = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.14, 
            screen.get_height() / 3 + screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.GREEN, "Pokaż Sesje", game_controller.get_default_font(), int(screen.get_height() * 0.035), kolor.WHITE, self.show_session, None, None, None, None, None)
        self.state_label = control_obj.Label(screen.get_width() / 2 - screen.get_width() * 0.39, 
            screen.get_height() / 3 + screen.get_height() * 0.38, screen.get_width() * 0.80, screen.get_height() * 0.032, 
            kolor.BLACK, self.connection.get_connection_status() , game_controller.get_default_font(), int(screen.get_height() * 0.025), kolor.WHITE, None, None, None, None, None, None)

        self.eventbus.subscribe("sessions_updated", self.refresh_sessions_view)
        self._prepare_graphics()


    def _prepare_graphics(self):
        self.graphics.add(self.choice_s_button, self.choice_w_button, self.create_button, 
                          self.join_button, self.exit_button, self.login_label, 
                          self.login_text, self.session_label, self.count_session_label, 
                          self.show_session_button, self.state_label)


    def set_all_dirty(self):
        for sprite in self.graphics:
            sprite.set_dirty()


    def update(self):
         self.graphics.update()


    def draw(self):
        self.graphics.draw(self.screen.get_screen())


    def render(self):
        self.graphics.clear(self.screen.get_screen(),  self.screen.get_background())
        self.update()
        dirty_rects = self.graphics.draw(self.screen.get_screen(),  self.screen.get_background())
        pygame.display.update(dirty_rects)

    
    def refresh_sessions_view(self, sessions):
        self.session_label.set_sessions(sessions)
        self.count_session_label.change_text(f"Liczba dostępnych sesji: {len(sessions)}")
        self.count_session_label.set_dirty()
        self.state_label.change_text(self.connection.get_connection_status())
        self.state_label.set_dirty()


    def handle_event(self, mouse_position, event):
        self.login_text_inactive()
        self.choice_s_button.handle_event(mouse_position, event)
        self.choice_w_button.handle_event(mouse_position, event)
        self.create_button.handle_event(mouse_position, event)
        self.join_button.handle_event(mouse_position, event)
        self.exit_button.handle_event(mouse_position, event)
        self.login_text.handle_event(mouse_position, event)
        self.session_label.handle_event(mouse_position, event)
        self.show_session_button.handle_event(mouse_position, event)


    def handle_keyboard_event(self, event):
        if self.login_text.get_active():
            if event.key == pygame.K_BACKSPACE:
                self.login_text.change_text(self.login_text.get_text()[:-1])
                self.login_text.set_dirty()
            else:
                new_text = self.login_text.get_text() + event.unicode
                self.login_text.change_text(support.Validation.validate_text(new_text))
                self.login_text.set_dirty()

    def choice_s_button_lc(self, mouse_position=None):
        self.game_controller.set_site('C')
        self.choice_s_button.change_colour(kolor.BLUE)
        self.choice_w_button.change_colour(kolor.DGREY)
        self.choice_s_button.set_dirty()
        self.choice_w_button.set_dirty()

    def choice_w_button_lc(self, mouse_position=None):
        self.game_controller.set_site('Z')
        self.choice_w_button.change_colour(kolor.BLUE)
        self.choice_s_button.change_colour(kolor.DGREY)
        self.choice_w_button.set_dirty()
        self.choice_s_button.set_dirty()


    def create_game(self, mouse_position=None):
        if self.game_controller.get_site() is not None and self.login_text.get_text() != "":
            self.game_controller.set_login(self.login_text.get_text())
            self.connection.set_action('create_game')

    def show_session(self, mouse_position=None):
        self.connection.set_action('list_sessions')

    def join_game(self, mouse_position=None):
        self.game_controller.set_marked_session_id(self.session_label.get_session_id())
        if self.game_controller.get_marked_session_id() is not None and self.login_text.get_text() != "":
            self.game_controller.set_login(self.login_text.get_text())
            self.connection.set_action('join_game')

    def exit_game(self, mouse_position=None):
        self.connection.close_connection()
        pygame.quit()
        sys.exit()


    def login_text_active(self, mouse_position=None):
        self.login_text.set_active(True)
        self.login_text.change_colour(self.login_text.get_active_colour())
        self.login_text.set_dirty()

    def login_text_inactive(self, mouse_position=None):
        self.login_text.set_active(False)
        self.login_text.change_colour(kolor.GREY)
        self.login_text.set_dirty()

    def set_scroll_offset_up(self):
        self.session_label.set_scroll_offset(self.session_label.scroll_offset - 1)


    def set_scroll_offset_down(self):
        self.session_label.set_scroll_offset(self.session_label.scroll_offset + 1)

    def choose_session(self, mouse_position=None):
        selected_idx = self.session_label.get_selected_idx()
        if selected_idx is not None:
            self.game_controller.set_marked_session_id(selected_idx)
