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
    def s_deploy_palace_gward(board, players):
        for player in players:
            for unit in player.units.values():
                if unit.qrs != None:
                    qrs = unit.qrs
                    id = unit.id
                    unit.set_deploy()
                    board.hexes[qrs].pawn_list.append(id)


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
    def get_matching_coords(hex_dict, check_func):
        return [coords for coords in hex_dict if check_func(coords)]
    

    @staticmethod
    def check_right_player(site1, site2):
        return True if site1 == site2 else False
    

    @staticmethod
    def validate_deploy_hex(site, phaze, qrs):
        if site == 'C' and phaze == 0:
            return GameLogic.deploy0_right_hex_S(qrs)
        elif site == 'Z' and phaze == 0:
            return GameLogic.deploy0_right_hex_W(qrs) 
        

    @staticmethod
    def get_unit_type_for_player_c(player, unit_id, game):
        if player == 'C':
            return game.player_s.units[unit_id].get_unit_type()
        elif player == 'Z':
            return game.player_w.units[unit_id].get_unit_type()
        return None
    

    @staticmethod
    def get_unit_type_for_player_s(site, unit_id, players):
        for player in players:
            if site == player.get_site():
                return player.units[unit_id].get_unit_type()


    @staticmethod
    def base_deploy(unit_id, site, qrs, terrain, phaze, board, flag, find_type):
        check = False
        if unit_id is not None:
            if flag == 'c':
                unit_type = GameLogic.get_unit_type_for_player_c(site, unit_id, find_type)
            else:
                unit_type = GameLogic.get_unit_type_for_player_s(site, unit_id, find_type)
            if GameLogic.validate_deploy_hex(site, phaze, qrs) == True and terrain not in dictionary.terrain_restrictions[unit_type]:
                if len(board.hexes[qrs].pawn_list) > 0:
                    for i in board.hexes[qrs].pawn_list:
                        if unit_type == 'D' or unit_type == 'N':
                            if i not in dictionary.basic_quantity_limits['P']:
                                return
                            else:
                                check = True
                        if i in dictionary.basic_quantity_limits[unit_type]:
                            return
                        else:
                            check = True
                else:
                    if unit_type != 'D' and unit_type != 'N':
                        check = True
        return check
        
                

