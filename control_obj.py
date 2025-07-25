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
    def __init__(self, position_x, position_y, width, height, colour, text, 
                 font_style, font_size, font_colour, on_click_left, on_click_right, 
                 on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK):
        super().__init__()
        self.position_x = position_x
        self.position_y = position_y
        self.width = int(width)
        self.height = int(height)
        self.colour = colour
        self.board_thickness = 1
        self.text = text
        self.wrapped_lines = []
        self.tiptext = None
        self.font_style = font_style
        self.font_size = font_size
        self.font_colour = font_colour
        self.on_click_left = on_click_left
        self.on_click_right = on_click_right
        self.on_scroll_4 = on_scroll_4
        self.on_scroll_5 = on_scroll_5
        self.on_hover = on_hover
        self.on_unhover = on_unhover
        self.board_colour = board_colour
        self.hovered = False
        self.active = True
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.position_x, self.position_y))
        self.dirty = 1
        self.visible = 1
 
        self._update_image()


    def _update_image(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        if self.colour != (0, 0, 0, 0):
            self.image.fill(self.colour)

        if self.font_style and self.font_size:
            font = pygame.font.SysFont(self.font_style, self.font_size)

            if self.wrapped_lines:
                if isinstance(self, UnitGraph):
                    line_height = int(self.height * 0.95 / 3)
                    align_key = "centerx"
                    align_value = self.width // 2
                elif isinstance(self, Label):
                    line_height = int(self.height / 5)
                    align_key = "left"
                    align_value = 1
                for i, line in enumerate(self.wrapped_lines):
                    label = font.render(line, True, self.font_colour)
                    rect = label.get_rect(**{align_key: align_value, "top": 1 + i * line_height})
                    self.image.blit(label, rect)

            elif self.text:
                label = font.render(str(self.text), True, self.font_colour)
                label_rect = label.get_rect(center=(self.width // 2, self.height // 2))
                self.image.blit(label, label_rect)

        if isinstance(self, UnitGraph):
            pygame.draw.rect(self.image, self.board_colour, pygame.Rect(0, 0, self.width, self.height),
            self.board_thickness)


    def update(self, mouse_position=None):

        if mouse_position is not None:
            is_hovering = self.is_over_object(mouse_position)
            if is_hovering and not self.hovered:
                    self.hovered = True
                    if callable(self.on_hover):
                        self.on_hover(self)
                        if self.visible == 1:
                            self.set_dirty()
            elif not is_hovering and self.hovered:
                    self.hovered = False
                    if callable(self.on_unhover):
                        self.on_unhover(self)
                        if self.visible == 1:
                            self.set_dirty()

        if self.dirty == 1:
            self._update_image()


    #stosowane tylko w przypadku recznego rysowania
    def draw(self, surface):
        if self.dirty == 0:
            return

        surface.blit(self.image, self.rect)
        self.dirty = 0


    def get_surface(self):
        return self.surface

    def set_dirty(self):
        self.dirty = 1

    def change_text(self, text):
        if self.text != text:
            self.text = text
            self.wrapped_lines = None
            self.set_dirty()

    def change_colour(self, colour):
        if self.colour != colour:
            self.colour = colour
            self.set_dirty()

    def is_over_object(self, mouse_position):
        return self.rect.collidepoint(mouse_position)

    def get_text(self):
        return self.text

    def set_active(self, active):
        self.active = active

    def get_active(self):
        return self.active

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_position_x(self):
        return self.position_x

    def get_position_y(self):
        return self.position_y

    def get_font_size(self):
        return self.font_size

    def get_font_style(self):
        return self.font_style

    def get_dirty(self):
        return self.dirty

    def get_rect(self):
        return self.rect

    def get_tip_text(self):
        return self.tiptext

    def set_tip_text(self, text):
        self.tiptext = text

    def set_position_x(self, position_x):
        self.position_x = position_x
        self.rect.topleft = (self.position_x, self.position_y)

    def set_position_y(self, position_y):
        self.position_y = position_y
        self.rect.topleft = (self.position_x, self.position_y)

    def set_colour(self, colour):
            self.colour = colour

    def set_text(self, text):
        self.text = text

    def set_visible(self, visible):
        self.visible = visible

    def set_board_colour(self, colour):
        self.board_colour = colour

    def handle_event(self, mouse_position, event):
        if self.is_over_object(mouse_position):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.on_click_left:
                    self.on_click_left(mouse_position=mouse_position)
            elif event.button == 3:
                if self.on_click_right:
                    self.on_click_right(mouse_position=mouse_position)
            elif event.button == 4:
                if self.on_scroll_4:
                    self.on_scroll_4()
            elif event.button == 5:   
                if self.on_scroll_5:
                    self.on_scroll_5()

class Label(ControlObj):
    def __init__(self, position_x, position_y, width, height, colour, text, font_style, 
                 font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK):
        super().__init__(position_x, position_y, width, height, colour, text, font_style, 
                font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover, on_unhover,
                board_colour)


class LabelWithScroll(Label):
    def __init__(self, position_x, position_y, width, height, colour, text,
                    font_style, font_size, font_colour, on_click_left, on_click_right,
                    on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK):

        self.sessions = []
        self.scroll_offset = 0
        self.selected_idx = None

        super().__init__(position_x, position_y, width, height, colour, text,
                        font_style, font_size, font_colour, on_click_left, on_click_right,
                        on_scroll_4, on_scroll_5, on_hover, on_unhover, board_colour)

    def set_sessions(self, sessions):
        self.sessions = sessions
        self.dirty = 1

    def set_scroll_offset(self, offset):
        old_offset = self.scroll_offset
        self.scroll_offset = max(0, min(offset, max(0, len(self.sessions) - 5)))
        if old_offset != self.scroll_offset:
            self.dirty = 1

    def set_selected_idx(self, idx):
        old_idx = self.selected_idx
        self.selected_idx = idx
        if old_idx != self.selected_idx:
            self.dirty = 1

    def get_session_id(self):
        session_data = self.sessions[self.selected_idx]
        if session_data is None:
            return
        session_id = session_data['sesja']
        return session_id

    def get_selected_idx(self):
        return self.selected_idx

    def get_selected_session(self):
        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.sessions):
            return self.sessions[self.selected_idx]
        return None

    def _update_image(self):
        self.image.fill(self.colour)

        font = pygame.font.SysFont(self.font_style or 'Arial', self.font_size)

        max_visible = min(5, len(self.sessions))
        end_index = min(self.scroll_offset + max_visible, len(self.sessions))
        visible_sessions = self.sessions[self.scroll_offset:end_index]

        for idx, sesja in enumerate(visible_sessions):
            try:
                session_id = sesja.get('sesja', 'N/A') if isinstance(sesja, dict) else str(sesja)
                player = sesja.get('gracz', 'N/A') if isinstance(sesja, dict) else 'N/A'
                side = sesja.get('jako', 'N/A') if isinstance(sesja, dict) else 'N/A'
                
                text = f"SESJA {session_id}:  LOGIN: {player}  STRONA: {side}"

                is_selected = (self.selected_idx == idx + self.scroll_offset)
                kolorTekstu = kolor.RED if is_selected else self.font_colour

                label = font.render(text, True, kolorTekstu)

                y = idx * (self.font_size + 2)

                if y + self.font_size <= self.height:
                    self.image.blit(label, (5, y))
                    
            except Exception as e:
                error_text = f"Błąd danych sesji {idx + self.scroll_offset}"
                label = font.render(error_text, True, kolor.RED)
                y = idx * (self.font_size + 2)
                if y + self.font_size <= self.height:
                    self.image.blit(label, (5, y))

        if len(self.sessions) > 5:
            if self.scroll_offset > 0:
                up_arrow = font.render("▲", True, kolor.BLUE)
                self.image.blit(up_arrow, (self.width - 20, 2))

            if self.scroll_offset + 5 < len(self.sessions):
                down_arrow = font.render("▼", True, kolor.BLUE)
                self.image.blit(down_arrow, (self.width - 20, self.height - self.font_size - 2))

    def update(self):
        if self.dirty == 1:
            self._update_image()
        return None

    def handle_event(self, mouse_position, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over_object(mouse_position):
            rel_x = mouse_position[0] - self.position_x
            rel_y = mouse_position[1] - self.position_y

            if len(self.sessions) > 5:
                if (self.scroll_offset > 0 and
                    self.width - 20 <= rel_x <= self.width and
                    2 <= rel_y <= 2 + self.font_size):
                    if self.on_scroll_4:  
                        self.on_scroll_4()
                    return

                if (self.scroll_offset + 5 < len(self.sessions) and
                    self.width - 20 <= rel_x <= self.width and
                    self.height - self.font_size - 2 <= rel_y <= self.height):
                    if self.on_scroll_5:
                        self.on_scroll_5()
                    return

            for idx in range(min(5, len(self.sessions) - self.scroll_offset)):
                y_pos = idx * (self.font_size + 2)
                if y_pos <= rel_y <= y_pos + self.font_size:
                    self.set_selected_idx(idx + self.scroll_offset)
                    if self.on_click_left: 
                        self.on_click_left()
                    return 
            
            super().handle_event(mouse_position, event)


class TextBox(ControlObj):
    def __init__(self, position_x, position_y, width, height, colour, text, font_style,
                 font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK,
                 active_color=None):
        super().__init__(position_x, position_y, width, height, colour, text, font_style,
                font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover, on_unhover, board_colour)
        self.active_color = active_color
        self.active = False


    def get_active_colour(self):
        return self.active_color

    
class Button(ControlObj):
    def __init__(self, position_x, position_y, width, height, colour, text, font_style,
                 font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK):
        super().__init__(position_x, position_y, width, height, colour, text, font_style,
                font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover, on_unhover, board_colour)


class StageGraph(ControlObj):
    def __init__(self, position_x, position_y, width, height, colour, text, font_style,
                 font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK, stage_obj=None):
        super().__init__(position_x, position_y, width, height, colour, text, font_style,
                font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover, on_unhover, board_colour)
        self.stage_obj = stage_obj


class PhazeGraph(ControlObj):
    def __init__(self, position_x, position_y, width, height, colour, text, font_style,
                 font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK, phaze_obj=None):
        super().__init__(position_x, position_y, width, height, colour, text, font_style,
                font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover, on_unhover, board_colour)
        self.phaze_obj = phaze_obj


class UnitGraph(ControlObj):
    def __init__(self, position_x, position_y, width, height, colour, text, font_style,
                 font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover=None, on_unhover=None, board_colour=kolor.BLACK, map_area=None, unit=None):
        super().__init__(position_x, position_y, width, height, colour, text, font_style,
                font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5, on_hover, on_unhover, board_colour)
        self.unit = unit
        self.map_area = map_area


    def is_visible_in_map_area(self, margin=10):
        if self.map_area is None:
            return True

        unit_rect = pygame.Rect(
            self.position_x - margin,
            self.position_y - margin,
            self.width + 2 * margin,
            self.height + 2 * margin
        )

        return self.map_area.get_rect().colliderect(unit_rect)


    def draw(self, surface):
        if not self.dirty:
            return
        
        if self.map_area is not None and not self.is_visible_in_map_area():
            return
        
        old_clip = surface.get_clip()
   
        if self.map_area is not None:
            surface.set_clip(self.map_area.get_rect())

        surface.blit(self.image, self.rect)
        
        surface.set_clip(old_clip)
        
        self.dirty = 0


class Tooltip(ControlObj):
    def __init__(self, position_x, position_y, width, height, colour, text, font_style,
                 font_size, font_colour, on_click_left=None, on_click_right=None,
                 on_scroll_4=None, on_scroll_5=None, on_hover=None, on_unhover=None, board_colour=kolor.BLACK):
        super().__init__(position_x, position_y, width, height, colour, text, font_style,
                font_size, font_colour, on_click_left, on_click_right, on_scroll_4, on_scroll_5,
                on_hover, on_unhover, board_colour)
        self.wrapped_lines = []


    def _update_image(self):
        if hasattr(self, 'wrapped_lines') and self.wrapped_lines:
            return
        else:
            super()._update_image()


    def set_text_wrapped(self, text, max_line_width):
        self.text = text
        if not self.font_style or not self.font_size:
            return

        font = pygame.font.SysFont(self.font_style, self.font_size)
        lines = support.Wrap.wrap_text(text, font, max_line_width)
        self.wrapped_lines = lines

        width = max_line_width + 10
        height = len(lines) * (font.get_height() + 5) + 10

        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.position_x, self.position_y))

        self._render_wrapped_lines(lines, font)
        self.set_dirty()


    def _render_wrapped_lines(self, lines, font):
        self.image.fill(kolor.WHITE)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, kolor.BLACK)
            self.image.blit(text_surface, (5, 5 + i * (font.get_height() + 5)))
    






        
        

        
