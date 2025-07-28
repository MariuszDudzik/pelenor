import dictionary

class GameLogic(object):

    @staticmethod
    def describe_name(site):
        if site == 'C':
            return 'Sauron'
        elif site == 'Z':
            return 'Westerneńczyk'

    @staticmethod
    def describe_spell_power(site):
        if site == 'C':
            return 8
        elif site == 'Z':
            return 10
        
    @staticmethod
    def unit_stats(unit):
        if unit.unit_type in ['P', 'J', 'S']:
            if unit.rewers == False:
                force = str(unit.force_hand or '')
                shot = str(unit.force_shot or '')
                return force + shot + str(unit.defence) + str(unit.morale)
            else:
                force = str(unit.force_hand_r or '')
                shot = str(unit.force_shot_r or '')
                return force + shot + str(unit.defence_r) + str(unit.morale_r)
        elif unit.unit_type == 'D':
            return str(unit.authority if unit.rewers == False else unit.authority_r)
        elif unit.unit_type == 'N':
            return f"{unit.authority}-{unit.spell_power}" if unit.rewers == False else f"{unit.authority_r}-{unit.spell_power}"
        elif unit.unit_type == 'M':
            return ''
        return ''
    

    @staticmethod
    def unit_full_string(unit, site):
        line1 = ""
        line2 = ""
        line3 = GameLogic.unit_stats(unit)

        if unit.unit_type in ['M']:
            line1 = ""
        else:
            line1 = unit.nationality
        if unit.unit_type in ['P', 'J', 'S']:
            line2 = unit.unit_type
        else:
            if unit.name == "Kocioł makieta" and site == 'C':
                line2 = "Kocioł"
            else:
                line2 = unit.name
        lines = [line1, line2, line3]
        return lines
    

    @staticmethod
    def change_pot_name(unit, site):
        name = unit.name
        if site == 'C':
            if name == "Kocioł makieta":
                name = "Kocioł"
        return name
    

    @staticmethod
    def deploy0_right_hex_S(hex):
        if hex[2] < -19 and hex[1] > 0 and hex[1] - hex[2] > 38:
            return True
        return False
    

    @staticmethod
    def deploy0_right_hex_W(hex):
        if (hex[0] > 3 and hex[0] < 19 and hex[1] < 8) or (hex[0] > 18 and hex[0] < 33 and hex[2] > -26):
            return True
        return False
    

    @staticmethod
    def minas_tirith(hex):
        if (hex[0] > 5 and hex[0] < 19 and hex[1] < 6) or (hex[0] > 18 and hex[0] < 31 and hex[2] > -24):
            return True
        return False
    

    @staticmethod
    def mn_level_1(hex):
        if (hex[0] > 5 and hex[0] < 8 and hex[1] < 6) or (hex[0] > 7 and hex[0] < 19 and hex[1] < 6 and hex[1] > 3) or (hex[0] > 28 and hex[0] < 31 and hex[2] > -24) or (hex[0] > 18 and hex[0] < 29 and hex[2] < -21 and hex[2] > -24):
            return True
        return False
    

    @staticmethod
    def mn_level_2(hex):
        if (hex[0] > 7 and hex[0] < 10 and hex[1] < 4) or (hex[0] > 9 and hex[0] < 19 and hex[1] < 4 and hex[1] > 1) or (hex[0] > 26 and hex[0] < 29 and hex[2] > -22) or (hex[0] > 18 and hex[0] < 27 and hex[2] < -19 and hex[2] > -22):
            return True
        return False
    

    @staticmethod
    def mn_level_3(hex):
        if (hex[0] > 9 and hex[0] < 12 and hex[1] < 2) or (hex[0] > 11 and hex[0] < 19 and hex[1] < 2 and hex[1] > -1) or (hex[0] > 24 and hex[0] < 27 and hex[2] > -20) or (hex[0] > 18 and hex[0] < 27 and hex[2] < -17 and hex[2] > -20):
            return True
        return False
    

    @staticmethod
    def mn_level_4(hex):
        if (hex[0] > 11 and hex[0] < 14 and hex[1] < 0) or (hex[0] > 13 and hex[0] < 19 and hex[1] < 0 and hex[1] > -3) or (hex[0] > 22 and hex[0] < 25 and hex[2] > -18) or (hex[0] > 18 and hex[0] < 23 and hex[2] < -15 and hex[2] > -18):
            return True
        return False
    

    @staticmethod
    def mn_level_5(hex):
        if (hex[0] > 13 and hex[0] < 16 and hex[1] < -2) or (hex[0] > 15 and hex[0] < 19 and hex[1] < -2 and hex[1] > -5) or (hex[0] > 20 and hex[0] < 23 and hex[2] > -16) or (hex[0] > 18 and hex[0] < 21 and hex[2] < -13 and hex[2] > -16):
            return True
        return False
    

    @staticmethod
    def mn_level_6(hex):
        if (hex[0] > 15 and hex[0] < 18 and hex[1] < -4) or (hex[0] > 17 and hex[0] < 19 and hex[1] < -4 and hex[1] > -7) or (hex[0] > 18 and hex[0] < 21 and hex[2] > -14) or (hex[0] > 16 and hex[0] < 19 and hex[2] < -11 and hex[2] > -14) or hex == (18, -7, -11):
            return True
        return False
    

    def create_mn_level_dict(hexes):
        minas_tirith = {}
        mn_level_1 = {}
        mn_level_2 = {}
        mn_level_3 = {}
        mn_level_4 = {}
        mn_level_5 = {}
        mn_level_6 = {}

        for coord, hex_obj in hexes.items():
            if GameLogic.minas_tirith(coord):
                minas_tirith[coord] = hex_obj
            if GameLogic.mn_level_1(coord):
                mn_level_1[coord] = hex_obj
            if GameLogic.mn_level_2(coord):
                mn_level_2[coord] = hex_obj
            if GameLogic.mn_level_3(coord):
                mn_level_3[coord] = hex_obj
            if GameLogic.mn_level_4(coord):
                mn_level_4[coord] = hex_obj
            if GameLogic.mn_level_5(coord):
                mn_level_5[coord] = hex_obj
            if GameLogic.mn_level_6(coord):
                mn_level_6[coord] = hex_obj

        return {
            "minas_tirith": minas_tirith,
            "mn_level_1": mn_level_1,
            "mn_level_2": mn_level_2,
            "mn_level_3": mn_level_3,
            "mn_level_4": mn_level_4,
            "mn_level_5": mn_level_5,
            "mn_level_6": mn_level_6,
        }
    
    
    @staticmethod
    def get_matching_coords(hex_dict, check_func):
        return [coords for coords in hex_dict if check_func(coords)]
    

    @staticmethod
    def check_right_player(site1, site2):
        return True if site1 == site2 else False
    

    @staticmethod
    def validate_deploy_hex(site, phaze, qrs):
        if site == 'C' and phaze == 0:
            return GameLogic.deploy0_right_hex_S(qrs)
     #   elif site == 'Z' and phaze == 0:
       #     return GameLogic.deploy0_right_hex_W(qrs) 
        elif site == 'Z' and phaze == 0:
            return GameLogic.minas_tirith(qrs)

    @staticmethod
    def get_unit_by_id(unit_id, player_1, player_2):
        for player in [player_1, player_2]:
            if unit_id in player.get_units():
                return player.get_units()[unit_id]
        return None


    @staticmethod
    def get_player_by_unit_id(unit_id, player_1, player_2):
        for player in [player_1, player_2]:
            if unit_id in player.get_units():
                return player
        return None


    @staticmethod
    def get_unit_type_for_player(unit_id, player_1, player_2):
        unit = GameLogic.get_unit_by_id(unit_id, player_1, player_2)
        return unit.get_unit_type() if unit else None


    @staticmethod
    def get_unit_nationality_for_player(unit_id, player_1, player_2):
        unit = GameLogic.get_unit_by_id(unit_id, player_1, player_2)
        return unit.get_nationality() if unit else None

          
    @staticmethod
    def get_unit_site(unit_id, player_1, player_2):
        unit = GameLogic.get_unit_by_id(unit_id, player_1, player_2)
        return unit.get_site() if unit else None
      
            
    @staticmethod
    def get_unit_distracted(unit_id, player_1, player_2):
        unit = GameLogic.get_unit_by_id(unit_id, player_1, player_2)
        return unit.get_distracted() if unit else None


    @staticmethod
    def get_units_for_player(site, player_1, player_2):
        for player in [player_1, player_2]:
            if player.get_site() == site:
                return player.get_units()


    @staticmethod
    def get_unit_qrs(unit_id, player_1, player_2):
        unit = GameLogic.get_unit_by_id(unit_id, player_1, player_2)
        return unit.get_qrs() if unit else None


    @staticmethod
    def get_unit_name(unit_id, player_1, player_2):
        unit = GameLogic.get_unit_by_id(unit_id, player_1, player_2)
        return unit.get_name() if unit else None
            

    @staticmethod
    def is_friendly_hex(hex_unit_id, site, player_1, player_2):
        return GameLogic.get_unit_site(hex_unit_id, player_1, player_2) == site
    

    @staticmethod
    def check_friends_for_n(pawns, player_1, player_2):
        for pawn_id in pawns:
            hex_unit_type = GameLogic.get_unit_type_for_player(pawn_id, player_1, player_2)
            if hex_unit_type in ['P', 'J', 'S', 'K', 'B']:
                return True, 12
        return False, 15
    

    @staticmethod
    def check_friends_for_d(pawns, nationality, player_1, player_2):
        for pawn_id in pawns:
            hex_unit_type = GameLogic.get_unit_type_for_player(pawn_id, player_1, player_2)
            hex_unit_nationality = GameLogic.get_unit_nationality_for_player(pawn_id, player_1, player_2)
            if hex_unit_type in ['P', 'J', 'S', 'K', 'B'] and hex_unit_nationality == nationality:
                return True, 12
        return False, 18
    

    @staticmethod
    def has_duplicate_unit_type(unit_type, pawns, player_1, player_2):
        for pawn_id in pawns:
            hex_unit_type = GameLogic.get_unit_type_for_player(pawn_id, player_1, player_2)
            if hex_unit_type in dictionary.basic_quantity_limits[unit_type]:
                return True
        return False


    @staticmethod
    def base_deploy(unit_id, site, qrs, phaze, board, player_1, player_2):
        if unit_id is None or qrs is None:
            return False, 11

        hex_ = board.hexes[qrs]
        terrain = hex_.get_terrain_sign()
        pawns = hex_.get_pawn_list()
        unit_type = GameLogic.get_unit_type_for_player(unit_id, player_1, player_2)
        unit_nationality = GameLogic.get_unit_nationality_for_player(unit_id, player_1, player_2)

        if not GameLogic.validate_deploy_hex(site, phaze, qrs):
            return False, 13

        if terrain in dictionary.terrain_restrictions[unit_type]:
            return False, 14

        if not pawns:
            return (False, 15) if unit_type in ('D', 'N') else (True, 12)

        if not GameLogic.is_friendly_hex(pawns[0], site, player_1, player_2):
            return False, 16

        if unit_type == 'N':
            return GameLogic.check_friends_for_n(pawns, player_1, player_2)

        if unit_type == 'D':
            return GameLogic.check_friends_for_d(pawns, unit_nationality, player_1, player_2)

        if GameLogic.has_duplicate_unit_type(unit_type, pawns, player_1, player_2):
            return False, 17

        return True, 12

    
    @staticmethod
    def check_commander_not_alone(unit_id, qrs, board, player_1, player_2, message):
        hex_ = board.hexes[qrs]
        pawns = hex_.get_pawn_list()[:]
        if len(pawns) > 1:
            pawns.remove(unit_id)
            l = []
            for pawn_id in pawns:
                hex_unit_type = GameLogic.get_unit_type_for_player(pawn_id, player_1, player_2)
                l.append(hex_unit_type)
            if 'D' in l or 'N' in l:
                if not any(x in l for x in ['P', 'J', 'S', 'K', 'B']):
                    return False, 19
        return True, message
    
    
    @staticmethod
    def check_palace_gward(unit_id, board, player_1, player_2, message):
        unit_name = GameLogic.get_unit_name(unit_id, player_1, player_2)
        if unit_name == "Gwardia pałacowa":
            return False, 22
        return True, message
    

    @staticmethod
    def set_akt_movement_after_deploy(unit_id, units, stage, board, qrs, site):
        if stage == 0:
            if site == 'C' or units[unit_id].get_unit_type() in ['N', 'D', 'M']:
                akt_movement = units[unit_id].get_movement()
            else:
                akt_movement = 5
        else:
            hex_movement_point = board.hexes[qrs].get_movement_point_to_spend()
            akt_movement = units[unit_id].get_movement() - hex_movement_point

        return akt_movement


    @staticmethod
    def chceck_if_deployed(site, stage, player_1, player_2):
        deployed = True
        units = GameLogic.get_units_for_player(site, player_1, player_2)
        for unit in units.values():
            if unit.get_stage_deploy() <= stage and not unit.get_deploy():
                deployed = False
                break
        return deployed


    @staticmethod
    def move_range(qrs, hexes, ran):
        range_hexes = set()

        q_base, r_base, s_base = qrs

        for dq in range(-ran, ran + 1):
            for dr in range(max(-ran, -dq - ran), min(ran, -dq + ran) + 1):
                ds = -dq - dr
                q = q_base + dq
                r = r_base + dr
                s = s_base + ds
                if (q, r, s) in hexes:
                    range_hexes.add((q, r, s))

        return range_hexes
    

