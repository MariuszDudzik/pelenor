import pygame
import math
import collections
import kolor
from pygame.sprite import DirtySprite
from functools import partial
import play_handler

Point = collections.namedtuple("Point", ["x", "y"])
Hex = collections.namedtuple("Hex", ["q", "r", "s"])

class HexGraphic(DirtySprite):
    def __init__(self, position, logical_hex, base_center, base_size, fill_color, outline_colors, 
        thickness, on_click_left, visible = 0, map_area=None):
        super().__init__()
        self.position = position  # (q, r, s)
        self.logical_hex = logical_hex
        self.base_center = base_center
        self.base_size = base_size    
        self.current_center = base_center
        self.current_size = base_size
        self.fill_color = fill_color
        self.outline_colors = outline_colors
        self.thickness = thickness
        self.on_click_left = on_click_left
        self.on_click_right = None
        self.on_scroll_4 = None 
        self.on_scroll_5 = None
        self.dirty = 1
        self.visible = visible
        self.zoom_level = 1.0
        self.map_area = map_area
        
        self._update_image()
        
    def _update_image(self):
        diameter = int(2 * self.current_size + max(self.thickness) * 2)
        self.image = pygame.Surface((diameter, diameter ), pygame.SRCALPHA)
        
        center_on_surface = Point(diameter//2, diameter//2)
        corners = Hexagon.polygon_corners(center_on_surface, self.current_size)
        points = [(p.x, p.y) for p in corners]
        pygame.draw.polygon(self.image, self.fill_color, points)
        
        #scaled_thickness = [max(1, int(t * self.zoom_level)) for t in self.thickness]
        scaled_thickness = [max(1, t) for t in self.thickness]
        
        for i in range(6):
            start_pos = points[i]
            end_pos = points[(i + 1) % 6]
            pygame.draw.line(self.image, self.outline_colors[i], start_pos, end_pos, scaled_thickness[i])
        
        self.rect = self.image.get_rect(center=(self.current_center.x, self.current_center.y))

    
    def draw(self, surface):
        if not self.dirty:
            return
            
        if self.map_area is not None and not self.is_visible_in_map_area():
            return
            
        old_clip = surface.get_clip()
        
        if self.map_area is not None:
            surface.set_clip(self.map_area)
        
        surface.blit(self.image, self.rect)
        surface.set_clip(old_clip)
        
        self.dirty = 0

    
    def update(self, mouse_position=None):
        if self.dirty:
            self._update_image()


    def set_dirty(self):
        self.dirty = 1
    
    
    def is_visible_in_map_area(self, margin=20):
      
        if self.map_area is None:
            return True
            
        hex_radius = self.current_size + max(self.thickness)
        hex_rect = pygame.Rect(
            self.current_center.x - hex_radius - margin,
            self.current_center.y - hex_radius - margin,
            2 * hex_radius + 2 * margin,
            2 * hex_radius + 2 * margin
        )

        return self.map_area.get_rect().colliderect(hex_rect)

    def get_current_center(self):
        return self.current_center

    def get_current_size(self):
        return self.current_size

    def set_fill_colour(self, color):
        self.fill_color = color


    def apply_camera(self, camera, map_area, world_hex_size):
        scale = camera.get_camera_scale()
        ui_x = map_area.get_position_x()
        ui_y = map_area.get_position_y()

        sx = ui_x + (self.base_center.x - camera.get_camera_x()) * scale
        sy = ui_y + (self.base_center.y - camera.get_camera_y()) * scale

        self.current_center = Point(sx, sy)
        self.current_size   = world_hex_size * scale
        self.zoom_level     = scale
        self.set_dirty()


    def handle_event(self, mouse_position, event):
        if self.is_over_object(mouse_position):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.visible == 1:
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

    def is_over_object(self, mouse_position):
        return self.rect.collidepoint(mouse_position)


class Hexagon:

    @staticmethod
    def hex_to_pixel(hex, size, offset_x=0, offset_y=0):
        x = size * (3 / 2 * hex.q)
        y = size * (math.sqrt(3) / 2 * hex.q + math.sqrt(3) * hex.r)
        return Point(x + offset_x + size, y + offset_y + size)
    

    @staticmethod
    def polygon_corners(center, size):
        corners = []
        for i in range(6):
            angle = 2 * math.pi / 6 * (i + 0.5)
            x_i = center.x + size * math.sin(angle)
            y_i = center.y + size * math.cos(angle)
            corners.append(Point(x_i, y_i))
        return corners


    @staticmethod
    def draw_hexagon(surface, center, size, fill_color, outline_colors, thickness):
        corners = Hexagon.polygon_corners(center, size)
        points = [(p.x, p.y) for p in corners]
        pygame.draw.polygon(surface, fill_color, points)
        for i in range(6):
            start_pos = points[i]
            end_pos = points[(i + 1) % 6]
            pygame.draw.line(surface, outline_colors[i], start_pos, end_pos, thickness[i])


    @staticmethod
    def side_colours(pos, hexes):
        outline_colors = []
        
        obj = hexes.get(pos)
        for color in obj.get_rim_colour_list():
            outline_colors.append(kolor.color_side.get(color))
        return outline_colors


    @staticmethod
    def side_thickness(pos, hexes):
        thickness = []
        thickness_map = {
            'g': 2,
            'm': 5,
            's': 3,
            't': 6,
            'b': 4
        }

        obj = hexes.get(pos)
        for value in obj.get_rim_thickness_list():
            thickness.append(thickness_map.get(value))
        return thickness


    @staticmethod
    def field_colour(pos, hexes):
        obj = hexes.get(pos)
        if obj.get_colour_flag():
            x = obj.get_colour()
        else:
            x = obj.get_dark_colour()

        return kolor.colour_hex.get(x)

                
    @staticmethod
    def create_hex_graphics_dict(camera, visible_hexes_data, map_area, play_obj):
        
        hex_graphics = {}
        hexes_dict = {pos: data['hex_obj'] for pos, data in visible_hexes_data.items()}

        for pos, hex_data in visible_hexes_data.items():
            hex_obj   = hex_data['hex_obj']
            world_pos = hex_data.get('world_pos')
            clip_info = hex_data['clip_info']

            if world_pos is None:
                world_pos = hex_data['pixel_pos']

            hex_graphic = HexGraphic(
                position=pos,
                logical_hex=hex_obj,
                base_center=world_pos,
                base_size=play_obj.base_hex_size,
                fill_color=Hexagon.field_colour(pos, hexes_dict),
                outline_colors=Hexagon.side_colours(pos, hexes_dict),
                thickness=Hexagon.side_thickness(pos, hexes_dict),
                on_click_left=partial(play_handler.PlayHandler.hex_left_click,
                                    play_obj=play_obj, hex_obj=hex_obj),
                visible=(1 if clip_info['fully_visible'] else 0),
                map_area=map_area
            )

            hex_graphic.apply_camera(camera, map_area, play_obj.base_hex_size)

            if not clip_info['fully_visible']:
                hex_graphic = Hexagon.create_clipped_hex_sprite(hex_graphic, clip_info, map_area)

            hex_graphics[pos] = hex_graphic

        return hex_graphics


    @staticmethod
    def create_clipped_hex_sprite( hex_sprite, clip_info, map_area):

        original_surface = hex_sprite.image
        original_rect = hex_sprite.rect
        
        if 'clip_rect' in clip_info:
            clip_rect = clip_info['clip_rect']
            
            surface_clip_left = max(0, clip_rect['left'] - original_rect.left)
            surface_clip_top = max(0, clip_rect['top'] - original_rect.top)
            surface_clip_right = min(original_surface.get_width(), 
                                clip_rect['right'] - original_rect.left)
            surface_clip_bottom = min(original_surface.get_height(), 
                                    clip_rect['bottom'] - original_rect.top)
            
            clipped_width = int(surface_clip_right - surface_clip_left)
            clipped_height = int(surface_clip_bottom - surface_clip_top)
            
            if clipped_width > 0 and clipped_height > 0:
                clipped_surface = pygame.Surface((clipped_width, clipped_height), pygame.SRCALPHA)
                
                source_rect = pygame.Rect(surface_clip_left, surface_clip_top, 
                                        clipped_width, clipped_height)
                clipped_surface.blit(original_surface, (0, 0), source_rect)
                
                hex_sprite.image = clipped_surface
                hex_sprite.rect = pygame.Rect(clip_rect['left'], clip_rect['top'], 
                                            clipped_width, clipped_height)
        
        return hex_sprite

  
 