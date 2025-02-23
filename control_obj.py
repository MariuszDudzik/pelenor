import pygame
import kolor

class ControlObj(object):
    def __init__(self, positionX, positionY, width, height, colour, text, 
                 fontStyle, fontSize, fontColour, onClickLeft, onClickRight, 
                 onScroll4, onScroll5):
        self.positionX = positionX
        self.positionY = positionY
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.fontStyle = fontStyle
        self.fontSize = fontSize
        self.fontColour = fontColour
        self.onClickLeft = onClickLeft  
        self.onClickRight = onClickRight
        self.onScroll4 = onScroll4 
        self.onScroll5 = onScroll5
        self.rect = pygame.Rect(positionX, positionY, width, height)
        self.active = True
        

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.positionX, self.positionY, 
                                               self.width, self.height))
        font = pygame.font.SysFont(self.fontStyle, self.fontSize)
        label = font.render(self.text, True, self.fontColour)
        screen.blit(label, (self.positionX + (self.width - label.get_width()) // 2, 
                            self.positionY + (self.height - label.get_height()) // 2))
        

    def isOverObject(self, mousePosition):
        return self.rect.collidepoint(mousePosition)
    

    def changeText(self, text):
        self.text = text


    def getText(self):
        return self.text
    
    def setActive(self, active):
        self.active = active

    def getActive(self):
        return self.active
    

    def changeColour(self, colour):
        self.colour = colour

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getPositionX(self):
        return self.positionX
    
    def getPositionY(self):
        return self.positionY
    
    def getFontSize(self):
        return self.fontSize


    def handle_event(self, mousePosition, event):
        if self.isOverObject(mousePosition):
            if event.button == 1: 
                if self.onClickLeft:
                    self.onClickLeft()
            elif event.button == 3:
                if self.onClickRight:
                    self.onClickRight()
            elif event.button == 4:
                if self.onScroll4:
                    self.onScroll4()
            elif event.button == 5:   
                if self.onScroll5:
                    self.onScroll5()
                    

class Label(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5)


class LabelWithScroll(Label):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5)
        

    def drawScrollList(self, screen, sessions, scrollOffSet, selectedIdx):
        pygame.draw.rect(screen, self.colour, (self.positionX, self.positionY, self.width, self.height))
        font = pygame.font.Font(self.fontStyle, self.fontSize)
   
        visibleSessions = sessions[scrollOffSet:scrollOffSet + 5]

        for idx, sesion in enumerate(visibleSessions):
            text = f"SESJA {sesion['sesja']}:  LOGIN: {sesion['gracz']}  STRONA: {sesion['jako']}"  
            if selectedIdx == idx + scrollOffSet:
                label = font.render(text, True, kolor.RED)  
            else:
                label = font.render(text, True, self.fontColour) 
            
            screen.blit(label, (self.positionX, self.positionY + idx * (self.fontSize + 1)))  

        
class TextBox(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5,
                 activeColor):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5)
        self.activeColor = activeColor
        self.active = False


    def getActiveColour(self):
        return self.activeColor

    
class Button(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5)
        
        
class StageGraph(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5,
                 season, nrStage):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5)
        self.season = season
        self.nrStage = nrStage


class PhazeGraph(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5,
                 nrstage, nrphaze):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5)
        self.nrStage = nrstage
        self.nrPhaze = nrphaze
        
        

        
