import pygame
import screen
import game
import menu
import play
import client
import gamecontroller
import eventbus

def main():
    pygame.init()
    eventbus_ = eventbus.EventBus()
    screen_ = screen.Screen()
    game_ = game.Game()
    gameController_ = gamecontroller.GameController()
    connection_ = client.Client(gameController_, game_, eventbus_)
    menu_ = menu.Menu(screen_, gameController_, connection_, eventbus_)
    play_ = play.Play(screen_, gameController_, connection_, game_)
    clock = pygame.time.Clock()
    screen_.fill_background((0, 0, 0))
  
    try:
        connection_.startConnection()
        clear = True
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
                    elif event.type == pygame.MOUSEBUTTONUP:
                        play_.handleEvent(mousePosition, event)
                    elif event.type == pygame.KEYDOWN:
                        play_.handleKeyboardEvent(event)
                    elif event.type == pygame.VIDEOEXPOSE or event.type == pygame.ACTIVEEVENT:
                        play_.setAllDirty()
                        screen_ = screen.Screen()
                        screen_.fill_background((0, 0, 0))
                   
            
            if gameController_.getInGame():
                menu_.render()

                if connection_.getAction() != None:
                    connection_.gameClient()
                    connection_.setAction(None)
            else:
                if clear:
                    play_.drawMap(mousePosition)
                    play_.addReinforcement()
                    play_.addReinforcementGraphics()
                    clear = False
    
                play_.render(mousePosition)
                play_.updateMovement(key)
                play_.handleMouseMotion(mousePosition, event)
                
            clock.tick(60)

    except KeyboardInterrupt:
        connection_.close_connection()
        pygame.quit()
        quit()

if __name__ == "__main__":
    main()