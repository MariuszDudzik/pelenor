import control_obj
import kolor
import sys
import pygame
import support

class Menu(object):

    def __init__(self, screen, gameController, connection, eventbus):

        self.screen = screen
        self.gameController = gameController
        self.connection = connection
        self.graphics = pygame.sprite.LayeredDirty()
        self.eventbus = eventbus
        
                 
        self.choiceSbutton = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.14, 
            screen.get_height() / 3 - screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.DGREY, "Sauron", gameController.getDefaultFont(), int(screen.get_height() * 0.035), kolor.WHITE, 
            self.choiceSbuttonLC, None, None, None, None, None)    
        self.choiceWbutton = control_obj.Button(screen.get_width() / 2 + screen.get_width() * 0.014, 
            screen.get_height() / 3 - screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.DGREY, "Westerneńczyk", gameController.getDefaultFont(), int(screen.get_height() * 0.035), kolor.WHITE, 
            self.choiceWbuttonLC, None, None, None, None, None)
        self.createButton = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.07, 
            screen.get_height() / 3, screen.get_width() * 0.14, screen.get_height() * 0.065, kolor.BLUE, "Stwórz Grę", 
            gameController.getDefaultFont(), int(screen.get_height() * 0.035), kolor.WHITE, self.createGame, None, None, None, None, None)
        self.joinButton = control_obj.Button(screen.get_width() / 2 + screen.get_width() * 0.014, 
            screen.get_height() / 3 + screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.GREEN, "Dołącz do Gry", gameController.getDefaultFont(), int(screen.get_height() * 0.035), kolor.WHITE, self.joinGame,  None, None, None, None, None)   
        self.exitButton = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.07, 
            screen.get_height() / 3 + screen.get_height() * 0.45, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.RED, "Zakończ", gameController.getDefaultFont(), int(screen.get_height() * 0.035), kolor.WHITE, self.exitGame, None, None, None, None, None)
        self.loginLabel = control_obj.Label(screen.get_width() / 2 - screen.get_width() * 0.15, 
            screen.get_height() / 3 - screen.get_height() * 0.15, screen.get_width() * 0.08, screen.get_height() * 0.032, 
            kolor.BLACK, "Wpisz login:", gameController.getDefaultFont(), int(screen.get_height() * 0.025), kolor.WHITE, None, None, None, None, None, None)
        self.loginText = control_obj.TextBox(screen.get_width() / 2 - screen.get_width() * 0.07, 
            screen.get_height() / 3 - screen.get_height() * 0.15, screen.get_width() * 0.14, screen.get_height() * 0.032, 
            kolor.GREY, "", gameController.getDefaultFont(), int(screen.get_height() * 0.025), kolor.BLACK, self.loginTextActive, None, None, None, None, None, kolor.WHITE,)
        self.sessionLabel = control_obj.LabelWithScroll(screen.get_width() / 2 - screen.get_width() * 0.175, 
            screen.get_height() / 3 + screen.get_height() * 0.18, screen.get_width() * 0.37, screen.get_height() * 0.16, 
            kolor.GREY, "", gameController.getDefaultFont(), int(screen.get_height() * 0.025), kolor.BLACK, self.chooseSession, None, self.setScrollOffsetUp, self.setScrollOffsetDown, None, None)
        self.countSessionLabel = control_obj.Label(screen.get_width() / 2 - screen.get_width() * 0.175, 
            screen.get_height() / 3 + screen.get_height() * 0.345, screen.get_width() * 0.37, screen.get_height() * 0.032, kolor.GREY, f"Liczba dostępnych sesji: {self.gameController.getCountOpenSessions()}", 
            gameController.getDefaultFont(), int(screen.get_height() * 0.025), kolor.BLACK, None, None, None, None, None, None)
        self.showSessionButton = control_obj.Button(screen.get_width() / 2 - screen.get_width() * 0.14, 
            screen.get_height() / 3 + screen.get_height() * 0.09, screen.get_width() * 0.14, screen.get_height() * 0.065, 
            kolor.GREEN, "Pokaż Sesje", gameController.getDefaultFont(), int(screen.get_height() * 0.035), kolor.WHITE, self.showSession, None, None, None, None, None)
        self.stateLabel = control_obj.Label(screen.get_width() / 2 - screen.get_width() * 0.39, 
            screen.get_height() / 3 + screen.get_height() * 0.38, screen.get_width() * 0.80, screen.get_height() * 0.032, 
            kolor.BLACK, self.connection.getConnectionStatus() , gameController.getDefaultFont(), int(screen.get_height() * 0.025), kolor.WHITE, None, None, None, None, None, None)

        self.eventbus.subscribe("sessions_updated", self.refresh_sessions_view)
        self._prepareGraphics()


    def _prepareGraphics(self):
        self.graphics.add(self.choiceSbutton, self.choiceWbutton, self.createButton, 
                          self.joinButton, self.exitButton, self.loginLabel, 
                          self.loginText, self.sessionLabel, self.countSessionLabel, 
                          self.showSessionButton, self.stateLabel)


    def setAllDirty(self):
        for sprite in self.graphics:
            sprite.setDirty()


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
        self.sessionLabel.setSessions(sessions)
        self.countSessionLabel.changeText(f"Liczba dostępnych sesji: {len(sessions)}")
        self.countSessionLabel.setDirty()
        self.stateLabel.changeText(self.connection.getConnectionStatus())
        self.stateLabel.setDirty()


    def handleEvent(self, mousePosition, event):
        self.loginTextInactive()
        self.choiceSbutton.handle_event(mousePosition, event)
        self.choiceWbutton.handle_event(mousePosition, event)
        self.createButton.handle_event(mousePosition, event)
        self.joinButton.handle_event(mousePosition, event)
        self.exitButton.handle_event(mousePosition, event)
        self.loginText.handle_event(mousePosition, event)
        self.sessionLabel.handle_event(mousePosition, event)
        self.showSessionButton.handle_event(mousePosition, event)


    def handleKeyboardEvent(self, event):
        if self.loginText.getActive():
            if event.key == pygame.K_BACKSPACE:
                self.loginText.changeText(self.loginText.getText()[:-1])
                self.loginText.setDirty()
            else:
                newText = self.loginText.getText() + event.unicode
                self.loginText.changeText(support.Validation.validateText(newText))
                self.loginText.setDirty()
        

    def choiceSbuttonLC(self):
        self.gameController.setSite('C')
        self.choiceSbutton.changeColour(kolor.BLUE)
        self.choiceWbutton.changeColour(kolor.DGREY)
        self.choiceSbutton.setDirty()
        self.choiceWbutton.setDirty()
      

    def choiceWbuttonLC(self):
        self.gameController.setSite('Z')
        self.choiceWbutton.changeColour(kolor.BLUE)
        self.choiceSbutton.changeColour(kolor.DGREY)
        self.choiceWbutton.setDirty()
        self.choiceSbutton.setDirty()


    def createGame(self):
        if self.gameController.getSite() is not None and self.loginText.getText() != "":
            self.gameController.setLogin(self.loginText.getText())
            self.connection.setAction('create_game')
      

    def showSession(self):
        self.connection.setAction('list_sessions')
       

    def joinGame(self):
        self.gameController.setMarkedSessionID(self.sessionLabel.getSessionId())
        if self.gameController.getMarkedSessionID is not None and self.loginText.getText() != "":
            self.gameController.setLogin(self.loginText.getText())
            self.connection.setAction('join_game')
           

    def exitGame(self):
        self.connection.close_connection()
        pygame.quit()
        sys.exit()


    def loginTextActive(self):
        self.loginText.setActive(True)
        self.loginText.changeColour(self.loginText.getActiveColour())
        self.loginText.setDirty()
        
         
    def loginTextInactive(self):
        self.loginText.setActive(True)
        self.loginText.changeColour(kolor.GREY)
        self.loginText.setDirty()
         
    
    def setScrollOffsetUp(self):
        self.sessionLabel.setScrollOffset(self.sessionLabel.scrollOffset - 1)


    def setScrollOffsetDown(self):
        self.sessionLabel.setScrollOffset(self.sessionLabel.scrollOffset + 1)


    def chooseSession(self):
        selected_idx = self.sessionLabel.getSelectedIdx()
        if selected_idx is not None:
            self.gameController.setMarkedSessionID(selected_idx)

    