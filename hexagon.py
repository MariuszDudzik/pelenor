import pygame
import math
import collections
import kolor

Point = collections.namedtuple("Point", ["x", "y"])
Hex = collections.namedtuple("Hex", ["q", "r", "s"])

class Hexagon(object):

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
    def side_colours(QRS_key, hex):
        outline_colors = []
        obj = hex.get(QRS_key)
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
    def side_thickness(QRS_key, hex):
        thickness = []
        obj = hex.get(QRS_key)
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
    def field_colour(QRS_key, hex):
        obj = hex.get(QRS_key)
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
    def suport(QRS):
        hex_center = Hex(QRS[0], QRS[1], QRS[2])
        return hex_center

    @staticmethod
    def draw_map(surface, hex_size, offset_x, offset_y, hexes):
        q, r, s = 0, 0, 0
        for i in range(24):
            for j in range(20):
                hex_center = Hex(q, r, s)
                QRS_key = 'q' + str(q) + 'r' + str(r) + 's' + str(s)
                outline_colors = Hexagon.side_colours(QRS_key, hexes)
                pixel = Hexagon.hex_to_pixel(hex_center, hex_size, offset_x, offset_y)
                fill_color = Hexagon.field_colour(QRS_key, hexes)
                thickness = Hexagon.side_thickness(QRS_key, hexes)
                Hexagon.draw_hexagon(surface, pixel, hex_size, fill_color, outline_colors, thickness)
                q += 2
                r -= 1
                s -= 1    
            q = 0
            r = i + 1
            s = -r

        q, r, s = 1, 0, -1
        for i in range(23):
            for j in range(19):
                hex_center = Hex(q, r, s)
                QRS_key = 'q' + str(q) + 'r' + str(r) + 's' + str(s)
                outline_colors = Hexagon.side_colours(QRS_key, hexes)
                pixel = Hexagon.hex_to_pixel(hex_center, hex_size, offset_x, offset_y)
                fill_color = Hexagon.field_colour(QRS_key, hexes)
                thickness = Hexagon.side_thickness(QRS_key, hexes)
                Hexagon.draw_hexagon(surface, pixel, hex_size, fill_color, outline_colors, thickness)
                q += 2
                r -= 1
                s -= 1
            q = 1
            r = i + 1
            s = 0 - (q + r)

    @staticmethod
    def pixel_to_hex(x, y, size, offset_x=0, offset_y=0):
        x = x - offset_x - size
        y = y - offset_y - size
        q = x / size * 2 / 3
        r = (((y - size * math.sqrt(3)/2 * q) / math.sqrt(3))) / size 
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

    @staticmethod
    def get_clicked_hex(corrected_mouse_position, hex_size, offset_x, offset_y):
        mouse_x, mouse_y = corrected_mouse_position[0], corrected_mouse_position[1]
        hex_coords = Hexagon.pixel_to_hex(mouse_x, mouse_y, hex_size, offset_x, offset_y)
        QRS_key = 'q' + str(hex_coords.q) + 'r' + str(hex_coords.r) + 's' + str(hex_coords.s)
        return QRS_key, (hex_coords.q, hex_coords.r, hex_coords.s)

    