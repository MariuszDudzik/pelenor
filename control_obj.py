import pygame
import kolor
import support
import pygame
import kolor
import support
import pygame
import kolor
import support

class ControlObj(pygame.sprite.DirtySprite):
    def __init__(self, positionX, positionY, width, height, colour, text, 
                 fontStyle, fontSize, fontColour, onClickLeft, onClickRight, 
                 onScroll4, onScroll5, onHover=None, onUnhover=None):
        super().__init__()
        self.positionX = positionX
        self.positionY = positionY
        self.width = int(width)
        self.height = int(height)
        self.colour = colour
        self.boardColour = kolor.BLACK
        self.boardThickness = 1
        self.text = text
        self.wrapped_lines = []
        self.tiptext = None
        self.fontStyle = fontStyle
        self.fontSize = fontSize
        self.fontColour = fontColour
        self.onClickLeft = onClickLeft  
        self.onClickRight = onClickRight
        self.onScroll4 = onScroll4 
        self.onScroll5 = onScroll5
        self.onHover = onHover
        self.onUnhover = onUnhover
        self.hovered = False
        self.active = True
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.positionX, self.positionY))
        self.dirty = 1
        self.visible = 1
 
        self._updateImage()

    
    def _updateImage(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        if self.colour != (0, 0, 0, 0):
            self.image.fill(self.colour)

        if self.fontStyle and self.fontSize:
            font = pygame.font.SysFont(self.fontStyle, self.fontSize)

            
            if self.wrapped_lines:
                if isinstance(self, UnitGraph):
                    lineHeight = int(self.height * 0.95 / 3)
                    align_key = "centerx"
                    align_value = self.width // 2
                elif isinstance(self, Label):
                    lineHeight = int(self.height / 5)
                    align_key = "left"
                    align_value = 1
                for i, line in enumerate(self.wrapped_lines):
                    label = font.render(line, True, self.fontColour)
                    rect = label.get_rect(**{align_key: align_value, "top": 1 + i * lineHeight})
                    self.image.blit(label, rect)

            elif self.text:
                label = font.render(str(self.text), True, self.fontColour)
                label_rect = label.get_rect(center=(self.width // 2, self.height // 2))
                self.image.blit(label, label_rect)

        if isinstance(self, UnitGraph):
            pygame.draw.rect(self.image, self.boardColour, pygame.Rect(0, 0, self.width, self.height),
            self.boardThickness)
    

    def update(self, mousePosition=None):
        
        if mousePosition is not None:
            is_hovering = self.isOverObject(mousePosition)
            if is_hovering and not self.hovered:
                    self.hovered = True
                    if callable(self.onHover):
                        self.onHover(self)
                        if self.visible == 1:
                            self.setDirty()
            elif not is_hovering and self.hovered:
                    self.hovered = False
                    if callable(self.onUnhover):
                        self.onUnhover(self)
                        if self.visible == 1:
                            self.setDirty()
        
        if self.dirty == 1:
            self._updateImage()


    #stosowane tylko w przypadku recznego rysowania
    def draw(self, surface):
        if self.dirty == 0:
            return

        surface.blit(self.image, self.rect)
        self.dirty = 0


    def getSurface(self):
        return self.surface

    def setDirty(self):
        self.dirty = 1
       
    def changeText(self, text):
        if self.text != text:
            self.text = text
            self.wrapped_lines = None
            self.setDirty()

    def changeColour(self, colour):
        if self.colour != colour:
            self.colour = colour
            self.setDirty()

    def isOverObject(self, mousePosition):
        return self.rect.collidepoint(mousePosition)

    def getText(self):
        return self.text
    
    def setActive(self, active):
        self.active = active
        self.visible = 1 if active else 0

    def getActive(self):
        return self.active

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

    def getDirty(self):
        return self.dirty
    
    def getRect(self):
        return self.rect
    
    def getTipText(self):
        return self.tiptext
    
    def setTipText(self, text):
        self.tiptext = text
    
    def setPositionX(self, positionX):
        self.positionX = positionX
        self.rect.topleft = (self.positionX, self.positionY)
    
    def setPositionY(self, positionY):
        self.positionY = positionY
        self.rect.topleft = (self.positionX, self.positionY)

    def setColour(self, colour):
            self.colour = colour

    def setText(self, text):
        self.text = text

    def setVisible(self, visible):
        self.visible = visible
    
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
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover=None, onUnhover=None):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover, onUnhover)
        

class LabelWithScroll(Label):
    def __init__(self, positionX, positionY, width, height, colour, text,
                    fontStyle, fontSize, fontColour, onClickLeft, onClickRight,
                    onScroll4, onScroll5, onHover=None, onUnhover=None):
            
        self.sessions = []
        self.scrollOffset = 0
        self.selectedIdx = None

        super().__init__(positionX, positionY, width, height, colour, text,
                        fontStyle, fontSize, fontColour, onClickLeft, onClickRight,
                        onScroll4, onScroll5, onHover, onUnhover)

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
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover=None, onUnhover=None,
                 activeColor=None):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover, onUnhover)
        self.activeColor = activeColor
        self.active = False


    def getActiveColour(self):
        return self.activeColor

    
class Button(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover=None, onUnhover=None):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover, onUnhover)
        
        
class StageGraph(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover=None, onUnhover=None,
                 stageObj=None):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover, onUnhover)
        self.stageObj = stageObj


class PhazeGraph(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover=None, onUnhover=None,
                 phazeObj=None):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover, onUnhover)
        self.phazeObj = phazeObj


class UnitGraph(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover=None, onUnhover=None,
                map_area=None, unit=None):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle, 
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5, onHover, onUnhover)
        self.unit = unit
        self.map_area = map_area


    def is_visible_in_map_area(self, margin=10):
        if self.map_area is None:
            return True

        unit_rect = pygame.Rect(
            self.positionX - margin,
            self.positionY - margin,
            self.width + 2 * margin,
            self.height + 2 * margin
        )

        return self.map_area.getRect().colliderect(unit_rect)


    def draw(self, surface):
        if not self.dirty:
            return
        
        if self.map_area is not None and not self.is_visible_in_map_area():
            return
        
        old_clip = surface.get_clip()
   
        if self.map_area is not None:
            surface.set_clip(self.map_area.getRect())
        
        surface.blit(self.image, self.rect)
        
        surface.set_clip(old_clip)
        
        self.dirty = 0


class Tooltip(ControlObj):
    def __init__(self, positionX, positionY, width, height, colour, text, fontStyle, 
                 fontSize, fontColour, onClickLeft=None, onClickRight=None, 
                 onScroll4=None, onScroll5=None, onHover=None, onUnhover=None):
        super().__init__(positionX, positionY, width, height, colour, text, fontStyle,
                fontSize, fontColour, onClickLeft, onClickRight, onScroll4, onScroll5,
                onHover, onUnhover)
        self.wrapped_lines = [] 
     

    def _updateImage(self):
        if hasattr(self, 'wrapped_lines') and self.wrapped_lines:
            return
        else:
            super()._updateImage()

    
    def setTextWrapped(self, text, max_line_width):
        self.text = text
        if not self.fontStyle or not self.fontSize:
            return
            
        font = pygame.font.SysFont(self.fontStyle, self.fontSize)
        lines = support.Wrap.wrap_text(text, font, max_line_width)
        self.wrapped_lines = lines

        width = max_line_width + 10
        height = len(lines) * (font.get_height() + 5) + 10

        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.positionX, self.positionY))

        self._renderWrappedLines(lines, font)
        self.setDirty()


    def _renderWrappedLines(self, lines, font):
        self.image.fill(kolor.WHITE)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, kolor.BLACK)
            self.image.blit(text_surface, (5, 5 + i * (font.get_height() + 5)))
    






        
        

        
