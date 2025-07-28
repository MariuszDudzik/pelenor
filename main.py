import pygame
import screen
import game
import menu
import play
import client
import gamecontroller
import eventbus
import play_handler

def main():
    pygame.init()
    eventbus_ = eventbus.EventBus()
    screen_ = screen.Screen()
    game_ = game.Game()
    game_controller_ = gamecontroller.GameController()
    connection_ = client.Client(game_controller_, game_, eventbus_)
    menu_ = menu.Menu(screen_, game_controller_, connection_, eventbus_)
    play_ = play.Play(screen_, game_controller_, connection_, game_)
    connection_.set_play(play_)
    clock = pygame.time.Clock()
    screen_.fill_background((0, 0, 0))
  
    try:
        connection_.start_connection()
        clear = True
        while True:
            mouse_position = pygame.mouse.get_pos()
            key = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if connection_.get_connection_status() == "Connected":
                        connection_.close_connection()
                    pygame.quit()
                    quit()

                if game_controller_.get_in_game():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu_.handle_event(mouse_position, event)
                    elif event.type == pygame.KEYDOWN:
                        menu_.handle_keyboard_event(event)
                    elif event.type == pygame.VIDEOEXPOSE or event.type == pygame.ACTIVEEVENT:
                        menu_.set_all_dirty()
                        screen_ = screen.Screen()
                        screen_.fill_background((0, 0, 0))
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        play_.handle_event(mouse_position, event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        play_.handle_event(mouse_position, event)
                    elif event.type == pygame.KEYDOWN:
                        play_.handle_keyboard_event(mouse_position, event)
                    elif event.type == pygame.VIDEOEXPOSE or event.type == pygame.ACTIVEEVENT:
                        play_.set_all_dirty()
                        screen_ = screen.Screen()
                        screen_.fill_background((0, 0, 0))


            if game_controller_.get_in_game():
                menu_.render()

                if connection_.get_action() != None:
                    connection_.game_client()
                    connection_.set_action(None)
            else:
                if clear:
                    play_.game.set_minas_tirith_dict()
                    play_.add_reinforcement()
                    play_.add_reinforcement_graphics()
                    play_handler.Refresh.refresh_login(play_)
                    play_handler.PlayHandler.change_hex_colour_handler(play_, False, 'C', 0)
                    clear = False

                play_.render(mouse_position)
                play_.update_movement(key)
                play_.handle_mouse_motion(mouse_position, event)

            clock.tick(60)

    except KeyboardInterrupt:
        connection_.close_connection()
        pygame.quit()
        quit()

if __name__ == "__main__":
    main()