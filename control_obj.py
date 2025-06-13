import pygame
import kolor
import support

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
    
    def getFontStyle(self): 
        return self.fontStyle
    
    def setColour(self, colour):
        self.colour = colour

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


class UnitGraph(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5,
                 unit):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5)
        self.unit = unit


    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.positionX, self.positionY, 
                                            self.width, self.height))

        unit_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        unit_surface.fill(self.colour)

        font = pygame.font.SysFont(self.fontStyle, self.fontSize)

        line = self.text
        lineHeight = int(self.height * 0.95 / 3)

        for i, tekst in enumerate(line):
            text_surface = font.render(tekst, True, self.fontColour)
            rect = text_surface.get_rect(centerx=self.width // 2, top=1 + i * lineHeight)
            unit_surface.blit(text_surface, rect)

        screen.blit(unit_surface, (self.positionX, self.positionY))


class Description(object):

    @staticmethod
    def draw(screen, text, max_line_width, positionX, positionY, fontStyle, fontSize):
        font = pygame.font.SysFont(fontStyle, fontSize)
        line = support.Wrap.wrap_text(text, font, max_line_width)
        width = max_line_width + 10
        height = len(line) * (font.get_height() + 5) + 10
        rect = pygame.Rect(positionX, positionY, width, height)
        menu_surface = pygame.Surface((width, height))
        menu_surface.fill((kolor.WHITE))
        for i, row in enumerate(line):
            tekst_surface = font.render(row, True, kolor.BLACK)
            menu_surface.blit(tekst_surface, (5, 5 + i * (font.get_height() + 5)))
        screen.blit(menu_surface, (positionX, positionY))





        
        

        
