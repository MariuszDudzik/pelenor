import control_obj
import kolor
import sys
import pygame
import support

class Menu(object):

    def __init__(self, screenWidth, screenHeight, gameController, connection):

        self.gameController = gameController
        self.connection = connection
        self.scroll_offset = 0  
        self.selectedIdx = -1

         
        self.choiceSbutton = control_obj.Button(screenWidth / 2 - screenWidth * 0.14, 
            screenHeight / 3 - screenHeight * 0.09, screenWidth * 0.14, screenHeight * 0.065, 
            kolor.DGREY, "Sauron", None, int(screenHeight * 0.045), kolor.WHITE, 
            self.choiceSbuttonLC, None, None, None)    
        self.choiceWbutton = control_obj.Button(screenWidth / 2 + screenWidth * 0.014, 
            screenHeight / 3 - screenHeight * 0.09, screenWidth * 0.14, screenHeight * 0.065, 
            kolor.DGREY, "Westerneńczyk", None, int(screenHeight * 0.045), kolor.WHITE, 
            self.choiceWbuttonLC, None, None, None)
        self.createButton = control_obj.Button(screenWidth / 2 - screenWidth * 0.07, 
            screenHeight / 3, screenWidth * 0.14, screenHeight * 0.065, kolor.BLUE, "Stwórz Grę", 
            None, int(screenHeight * 0.045), kolor.WHITE, self.createGame, None, None, None)
        self.joinButton = control_obj.Button(screenWidth / 2 + screenWidth * 0.014, 
            screenHeight / 3 + screenHeight * 0.09, screenWidth * 0.14, screenHeight * 0.065, 
            kolor.GREEN, "Dołącz do Gry", None, int(screenHeight * 0.045), kolor.WHITE, self.joinGame,
            None, None, None)   
        self.exitButton = control_obj.Button(screenWidth / 2 - screenWidth * 0.07, 
            screenHeight / 3 + screenHeight * 0.45, screenWidth * 0.14, screenHeight * 0.065, 
            kolor.RED, "Zakończ", None, int(screenHeight * 0.045), kolor.WHITE, self.exitGame, None, 
            None, None)
        self.loginLabel = control_obj.Label(screenWidth / 2 - screenWidth * 0.14, 
            screenHeight / 3 - screenHeight * 0.15, screenWidth * 0.07, screenHeight * 0.032, 
            kolor.BLACK, "Wpisz login:", None, int(screenHeight * 0.035), kolor.WHITE, None, None, 
            None, None)
        self.loginText = control_obj.TextBox(screenWidth / 2 - screenWidth * 0.07, 
            screenHeight / 3 - screenHeight * 0.15, screenWidth * 0.14, screenHeight * 0.032, 
            kolor.GREY, "", None, int(screenHeight * 0.033), kolor.BLACK, self.loginTextActive, None, 
            None, None, kolor.WHITE,)
        self.sessionLabel = control_obj.LabelWithScroll(screenWidth / 2 - screenWidth * 0.175, 
            screenHeight / 3 + screenHeight * 0.18, screenWidth * 0.37, screenHeight * 0.16, 
            kolor.GREY, "", None, int(screenHeight * 0.033), kolor.BLACK, self.chooseSession, None, 
            self.setScrollOffsetUp, self.setScrollOffsetDown)
        self.countSessionLabel = control_obj.Label(screenWidth / 2 - screenWidth * 0.175, 
            screenHeight / 3 + screenHeight * 0.345, screenWidth * 0.37, screenHeight * 0.032, 
            kolor.GREY, f"Liczba dostępnych sesji: {self.gameController.getCountOpenSessions()}", 
            None, int(screenHeight * 0.033), kolor.BLACK, None, None, None, None)
        self.showSessionButton = control_obj.Button(screenWidth / 2 - screenWidth * 0.14, 
            screenHeight / 3 + screenHeight * 0.09, screenWidth * 0.14, screenHeight * 0.065, 
            kolor.GREEN, "Pokaż Sesje", None, int(screenHeight * 0.045), kolor.WHITE, self.showSession, 
            None, None, None)
        self.stateLabel = control_obj.Label(screenWidth / 2 - screenWidth * 0.175, 
            screenHeight / 3 + screenHeight * 0.38, screenWidth * 0.37, screenHeight * 0.032, 
            kolor.BLACK, self.connection.getConnectionStatus() , None, int(screenHeight * 0.033), 
            kolor.WHITE, None, None, None, None)
       

    def drawMenu(self, screen):
        self.choiceSbutton.draw(screen)
        self.choiceWbutton.draw(screen)
        self.createButton.draw(screen)
        self.joinButton.draw(screen)
        self.exitButton.draw(screen)
        self.loginLabel.draw(screen)
        self.loginText.draw(screen)
        self.sessionLabel.drawScrollList(screen, self.gameController.getOpenSessions(), 
                                    self.getScrollOffset(), self.getSelectedIdx())
        self.countSessionLabel.draw(screen)
        self.showSessionButton.draw(screen)
        self.stateLabel.draw(screen)


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
            else:
                newText = self.loginText.getText() + event.unicode
                self.loginText.changeText(support.Validation.validateText(newText))


    def choiceSbuttonLC(self):
        self.gameController.setSite('C')
        self.choiceSbutton.changeColour(kolor.BLUE)
        self.choiceWbutton.changeColour(kolor.DGREY)
      

    def choiceWbuttonLC(self):
        self.gameController.setSite('Z')
        self.choiceWbutton.changeColour(kolor.BLUE)
        self.choiceSbutton.changeColour(kolor.DGREY)

    def createGame(self):
        if self.gameController.getSite() is not None and self.loginText.getText() != "":
            self.gameController.setLogin(self.loginText.getText())
            self.connection.setAction('create_game')

    def showSession(self):
        self.connection.setAction('list_sessions')

    def joinGame(self):
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
         
    
    def loginTextInactive(self):
        self.loginText.setActive(True)
        self.loginText.changeColour(kolor.GREY)


    def getScrollOffset(self):
        return self.scroll_offset


    def changeScrollOffset(self, newOffset):
        self.scroll_offset = newOffset


    def setScrollOffsetUp(self):
                if self.getScrollOffset() > 0:
                    self.changeScrollOffset(self.getScrollOffset() - 1)


    def setScrollOffsetDown(self):
                if self.getScrollOffset() < len(self.gameController.getOpenSessions()) - 5:
                    self.changeScrollOffset(self.getScrollOffset() + 1)


    def getSelectedIdx(self):
        return self.selectedIdx


    def setSelectIdx(self, newIdx):
        self.selectedIdx = newIdx


    def chooseSession(self):                  
        sessions = self.gameController.getOpenSessions()
        scroll = self.getScrollOffset()
        selectedIdx = self.getSelectedIdx()
        x = self.sessionLabel.getPositionX()
        y = self.sessionLabel.getPositionY()
        height = self.sessionLabel.getFontSize() + 1
        width = self.sessionLabel.getWidth()
        mousePos = pygame.mouse.get_pos()
        for idx, session in enumerate(sessions[scroll:scroll + 5]):
            row_rect = pygame.Rect(x, y + idx * (height), width, height)
            if row_rect.collidepoint(mousePos):
                selectedIdx = idx + scroll 
                self.gameController.setMarkedSessionID(session['sesja'])
                self.setSelectIdx(selectedIdx)
