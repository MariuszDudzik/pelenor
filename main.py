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
    menu_ = menu.Menu(screen_.get_width(), screen_.get_height(), gameController_, connection_)
    play_ = play.Play(screen_.get_width(), screen_.get_height(), gameController_, connection_, game_)
    clock = pygame.time.Clock()

    try:
        connection_.startConnection()

        while True:
            mousePosition = pygame.mouse.get_pos()
            key = pygame.key.get_pressed()
            if gameController_.getInGame():
                menu_.stateLabel.changeText(connection_.getConnectionStatus())
                menu_.countSessionLabel.changeText(f"Liczba sesji: {gameController_.getCountOpenSessions()}")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        connection_.close_connection()
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:   
                        menu_.handleEvent(mousePosition, event)  
                    elif event.type == pygame.KEYDOWN:
                        menu_.handleKeyboardEvent(event)
                        
                menu_.drawMenu(screen_.get_screen())

                if connection_.getAction() != None:
                    connection_.gameClient()  
                    connection_.setAction(None)
                    
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        connection_.close_connection()
                        pygame.quit()
                        quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:   
                        play_.handleEvent(mousePosition, event)
                    elif event.type == pygame.KEYDOWN:
                        play_.handleKeyboardEvent(event)
            
                play_.updateMovement(screen_.get_width(), screen_.get_height(), key)
                screen_.get_screen().fill((0, 0, 0))
                play_.drawPlay(screen_.get_screen(), mousePosition)

            pygame.display.flip()
            clock.tick(20)

    except KeyboardInterrupt:
        connection_.close_connection()
        pygame.quit()
        quit()

if __name__ == "__main__":
    main()