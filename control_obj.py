import pygame
import kolor
import support

class ControlObj(pygame.sprite.DirtySprite):
    def __init__(self, positionX, positionY, width, height, colour, text, 
                 fontStyle, fontSize, fontColour, onClickLeft, onClickRight, 
                 onScroll4, onScroll5):
        super().__init__()
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
        self.active = True
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.positionX, self.positionY))
        self.dirty = 1
        self._updateImage()


    def _updateImage(self):
        self.image.fill(self.colour)
        if self.text:
            font = pygame.font.SysFont(self.fontStyle, self.fontSize)
            label = font.render(self.text, True, self.fontColour)
            label_rect = label.get_rect(center=(self.width // 2, self.height // 2))
            self.image.blit(label, label_rect)


    def update(self):
        if self.dirty == 1:
            self._updateImage()


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

    def setDirty(self):
        self.dirty = 1

    def getDirty(self):
        return self.dirty
    

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
    def __init__(self, positionX, positionY, width, height, colour, text,
                    fontStyle, fontSize, fontColour, onClickLeft, onClickRight,
                    onScroll4, onScroll5):
            
        self.sessions = []
        self.scrollOffset = 0
        self.selectedIdx = None

        super().__init__(positionX, positionY, width, height, colour, text,
                        fontStyle, fontSize, fontColour, onClickLeft, onClickRight,
                        onScroll4, onScroll5)

    def setSessions(self, sessions):
        self.sessions = sessions
        self.dirty = 1

    def setScrollOffset(self, offset):
        old_offset = self.scrollOffset
        self.scrollOffset = max(0, min(offset, max(0, len(self.sessions) - 5)))
        if old_offset != self.scrollOffset:
            self.dirty = 1

    def setSelectedIdx(self, idx):
        old_idx = self.selectedIdx
        self.selectedIdx = idx
        if old_idx != self.selectedIdx:
            self.dirty = 1

    def getSessionId(self):
        sessionData = self.sessions[self.selectedIdx]
        session_id = sessionData['sesja']
        return session_id

    def getSelectedIdx(self):
        return self.selectedIdx

    def getSelectedSession(self):
        if self.selectedIdx is not None and 0 <= self.selectedIdx < len(self.sessions):
            return self.sessions[self.selectedIdx]
        return None

    def _updateImage(self):
        self.image.fill(self.colour)

        font = pygame.font.SysFont(self.fontStyle or 'Arial', self.fontSize)
        
        max_visible = min(5, len(self.sessions))
        end_index = min(self.scrollOffset + max_visible, len(self.sessions))
        visibleSessions = self.sessions[self.scrollOffset:end_index]
        

        for idx, sesja in enumerate(visibleSessions):
            try:
                session_id = sesja.get('sesja', 'N/A') if isinstance(sesja, dict) else str(sesja)
                player = sesja.get('gracz', 'N/A') if isinstance(sesja, dict) else 'N/A'
                side = sesja.get('jako', 'N/A') if isinstance(sesja, dict) else 'N/A'
                
                text = f"SESJA {session_id}:  LOGIN: {player}  STRONA: {side}"
                
                isSelected = (self.selectedIdx == idx + self.scrollOffset)
                kolorTekstu = kolor.RED if isSelected else self.fontColour
                
                label = font.render(text, True, kolorTekstu)
                
                y = idx * (self.fontSize + 2)
                
                if y + self.fontSize <= self.height:
                    self.image.blit(label, (5, y))
                    
            except Exception as e:
                error_text = f"Błąd danych sesji {idx + self.scrollOffset}"
                label = font.render(error_text, True, kolor.RED)
                y = idx * (self.fontSize + 2)
                if y + self.fontSize <= self.height:
                    self.image.blit(label, (5, y))

        if len(self.sessions) > 5:
            if self.scrollOffset > 0:
                up_arrow = font.render("▲", True, kolor.BLUE)
                self.image.blit(up_arrow, (self.width - 20, 2))
            
            if self.scrollOffset + 5 < len(self.sessions):
                down_arrow = font.render("▼", True, kolor.BLUE)
                self.image.blit(down_arrow, (self.width - 20, self.height - self.fontSize - 2))

    def update(self):
        if self.dirty == 1:
            self._updateImage()
        return None
    
    def handle_event(self, mousePosition, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.isOverObject(mousePosition):
            rel_x = mousePosition[0] - self.positionX
            rel_y = mousePosition[1] - self.positionY
            
            if len(self.sessions) > 5:
                if (self.scrollOffset > 0 and 
                    self.width - 20 <= rel_x <= self.width and 
                    2 <= rel_y <= 2 + self.fontSize):
                    if self.onScroll4:  
                        self.onScroll4()
                    return 
                
                if (self.scrollOffset + 5 < len(self.sessions) and 
                    self.width - 20 <= rel_x <= self.width and 
                    self.height - self.fontSize - 2 <= rel_y <= self.height):
                    if self.onScroll5: 
                        self.onScroll5()
                    return 
            
            for idx in range(min(5, len(self.sessions) - self.scrollOffset)):
                y_pos = idx * (self.fontSize + 2)
                if y_pos <= rel_y <= y_pos + self.fontSize:
                    self.setSelectedIdx(idx + self.scrollOffset)
                    if self.onClickLeft: 
                        self.onClickLeft()
                    return 
            
            super().handle_event(mousePosition, event)


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





        
        

        
