import pygame
import math
import collections
import kolor
from pygame.sprite import DirtySprite

Point = collections.namedtuple("Point", ["x", "y"])
Hex = collections.namedtuple("Hex", ["q", "r", "s"])

class HexGraphic(DirtySprite):
    def __init__(self, position, logical_hex, base_center, base_size, fill_color, outline_colors, 
        thickness, map_area=None):
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
        self.dirty = 1
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
        
        scaled_thickness = [max(1, int(t * self.zoom_level)) for t in self.thickness]
        
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

    
    def update(self, mouse_pos=None):
        if self.dirty:
            self._update_image()

    
    def update_from_logical(self):
        self.fill_color = Hexagon.field_colour(self.position, {self.position: self.logical_hex})
        self.outline_colors = Hexagon.side_colours(self.position, {self.position: self.logical_hex})
        self.thickness = Hexagon.side_thickness(self.position, {self.position: self.logical_hex})
        self.dirty = 1
    
   
    def setDirty(self):
        self.dirty = 1
        self.update_from_logical()
    
    
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
        
        return self.map_area.getRect().colliderect(hex_rect)
    
    
    def update_graphics(self, fill_color=None, outline_colors=None, thickness=None):
        if fill_color is not None:
            self.fill_color = fill_color
        if outline_colors is not None:
            self.outline_colors = outline_colors
        if thickness is not None:
            self.thickness = thickness
        self.dirty = 1

    
    def getCurrentCenter(self):
        return self.current_center
    
    def getCurrentSize(self):
        return self.current_size


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
        for color in obj.getRimColourList():
            match color:
                case 'W':
                    outline_colors.append(kolor.WHITE)
                case 'B':
                    outline_colors.append(kolor.BLACK)
                case 'R':
                    outline_colors.append(kolor.CHOCOLATE)
        return outline_colors


    @staticmethod
    def side_thickness(pos, hexes):
        thickness = []
        obj = hexes.get(pos)
        for value in obj.getRimThicknessList():
            match value:
                case 'g':
                    thickness.append(2)
                case 'm':
                    thickness.append(5)
                case 's':
                    thickness.append(3)
                case 't':
                    thickness.append(6)
                case 'b':
                    thickness.append(4)
        return thickness


    @staticmethod
    def field_colour(pos, hexes):
        obj = hexes.get(pos)
        match obj.getColour():
            case 'W':
                return kolor.BEIGE
            case 'Y':
                return kolor.YELLOW
            case 'G':
                return kolor.GREEN
            case 'Z':
                return kolor.BROWN
            case 'B':
                return kolor.BLACK
            case 'T':
                return kolor.GREY
            case 'K':
                return kolor.DGREY
            case 'S':
                return kolor.PERU
            case 'O':
                return kolor.DARKKHAKI
            case 'PG':
                return kolor.PGREEN
            case 'PY':
                return kolor.PYELLOW
            case 'PZ':
                return kolor.PBROWN
            case 'PW':
                return kolor.PBEIGE
            case 'PT':
                return kolor.PGREY
            case 'PK':
                return kolor.PDGREY
            case 'PS':
                return kolor.PPERU
            case 'PO':
                return kolor.PDARKKHAKI

    
    @staticmethod
    def create_hex_graphics_dict(hex_size, camera, visible_hexes_data, map_area):
        
        hex_graphics = {}

        hexes_dict = {pos: data['hex_obj'] for pos, data in visible_hexes_data.items()}

        for pos, hex_data in visible_hexes_data.items():
            hex_obj = hex_data['hex_obj']
            pixel_pos = hex_data['pixel_pos']
            clip_info = hex_data['clip_info']

            fill_color = Hexagon.field_colour(pos, hexes_dict)
            outline_colors = Hexagon.side_colours(pos, hexes_dict)
            thickness = Hexagon.side_thickness(pos, hexes_dict)

            hex_graphic = HexGraphic(
                position=pos,
                logical_hex=hex_obj,
                base_center=pixel_pos,
                base_size=hex_size,
                fill_color=fill_color,
                outline_colors=outline_colors,
                thickness=thickness,
                map_area=map_area
            )

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


    @staticmethod
    def pixel_to_hex(x, y, base_size, zoom_level, offset_x=0, offset_y=0, zoom_center_x=None, zoom_center_y=None):
        if zoom_center_x is not None and zoom_center_y is not None:
            scaled_x = zoom_center_x + (x - zoom_center_x) / zoom_level
            scaled_y = zoom_center_y + (y - zoom_center_y) / zoom_level
        else:
            scaled_x = x / zoom_level
            scaled_y = y / zoom_level
        
        scaled_x = scaled_x - offset_x - base_size
        scaled_y = scaled_y - offset_y - base_size
        
        q = scaled_x / base_size * 2 / 3
        r = (((scaled_y - base_size * math.sqrt(3)/2 * q) / math.sqrt(3))) / base_size 
        return Hexagon.hex_round(q, r)


    @staticmethod    
    def hex_round(q, r):
        s = -q - r
        q_round = round(q)
        r_round = round(r)
        s_round = round(s)

        q_diff = abs(q_round - q)
        r_diff = abs(r_round - r)
        s_diff = abs(s_round - s)

        if q_diff > r_diff and q_diff > s_diff:
            q_round = -r_round - s_round
        elif r_diff > s_diff:
            r_round = -q_round - s_round
        return Hex(q_round, r_round, s_round)
   