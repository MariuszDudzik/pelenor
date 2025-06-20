import pygame
import screen
import game
import menu
import play
import client
import gamecontroller

def main():
    pygame.init()
    screen_ = screen.Screen()
    game_ = game.Game()
    gameController_ = gamecontroller.GameController()
    connection_ = client.Client(gameController_, game_)
    menu_ = menu.Menu(screen_, gameController_, connection_)
    play_ = play.Play(screen_, gameController_, connection_, game_)
    clock = pygame.time.Clock()
    screen_.fill_background((0, 0, 0))

    try:
        connection_.startConnection()
        while True:
            mousePosition = pygame.mouse.get_pos()
            key = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if connection_.getConnectionStatus() == "Connected":
                        connection_.close_connection()
                    pygame.quit()
                    quit()
                
                if gameController_.getInGame():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu_.handleEvent(mousePosition, event)
                    elif event.type == pygame.KEYDOWN:
                        menu_.handleKeyboardEvent(event)
                    elif event.type == pygame.VIDEOEXPOSE or event.type == pygame.ACTIVEEVENT:
                        menu_.setAllDirty()
                        screen_ = screen.Screen()
                        screen_.fill_background((0, 0, 0))
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        play_.handleEvent(mousePosition, event)
                    elif event.type == pygame.KEYDOWN:
                        play_.handleKeyboardEvent(event)
                   
            
            if gameController_.getInGame():
                if gameController_.getRedraw():
                    menu_.stateLabel.changeText(connection_.getConnectionStatus())
                    menu_.redraw()
                    gameController_.setRedraw(False)
                
                menu_.graphics.clear(screen_.get_screen(),  screen_.get_background())
                menu_.update()
                dirty_rects = menu_.graphics.draw(screen_.get_screen(),  screen_.get_background())
                pygame.display.update(dirty_rects)
                
                if connection_.getAction() != None:
                    connection_.gameClient()
                    connection_.setAction(None)
            else:
                play_.updateMovement(screen_, key)
                
                
                screen_.get_screen().fill((0, 0, 0))
                play_.drawPlay(screen_.get_screen(), mousePosition)
                screen_.set_redraw2(False)
                pygame.display.flip()

            clock.tick(30)

    except KeyboardInterrupt:
        connection_.close_connection()
        pygame.quit()
        quit()

if __name__ == "__main__":
    main()