class GameLogic(object):

    @staticmethod
    def describeName(site):
        if site == 'C':
            return 'Sauron'
        elif site == 'Z':
            return 'Westerneńczyk' 
        
    @staticmethod    
    def describeSpellPower(site):
        if site == 'C':
            return 8
        elif site == 'Z':
            return 10
        
    @staticmethod
    def unitStats(unit):
        if unit.unitType in ['P', 'J', 'S']:
            if unit.rewers == False:
                force = str(unit.forceHand or '')
                shot = str(unit.forceShot or '')
                return force + shot + str(unit.defence) + str(unit.morale)
            else:
                force = str(unit.forceHandR or '')
                shot = str(unit.forceShotR or '')
                return force + shot + str(unit.defenceR) + str(unit.moraleR)
        elif unit.unitType == 'D':
            return str(unit.authority if unit.rewers == False else unit.authorityR)
        elif unit.unitType == 'N':
            return f"{unit.authority}-{unit.spellPower}" if unit.rewers == False else f"{unit.authorityR}-{unit.spellPower}"
        elif unit.unitType == 'M':
            return ''
        return ''
    

    @staticmethod
    def unitFullString(unit, site):
        line1 = ""
        line2 = ""
        line3 = GameLogic.unitStats(unit)

        if unit.unitType in ['M']:
            line1 = ""
        else:
            line1 = unit.nationality
        if unit.unitType in ['P', 'J', 'S']:
            line2 = unit.unitType
        else:
            if unit.name == "Kocioł makieta" and site == 'C':
                line2 = "Kocioł"
            else:
                line2 = unit.name
        lines = [line1, line2, line3]
        return lines
    

    @staticmethod
    def changePotName(unit, site):
        name = unit.name
        if site == 'C':
            if name == "Kocioł makieta":
                name = "Kocioł"
        return name
    

    @staticmethod
    def S_deploy_palace_gward(board, players):
        for player in players:
            for unit in player.units.values():
                if unit.QRS != None:
                    qrs = unit.QRS
                    id = unit.id
                    unit.setDeploy()
                    board.hexes[qrs].pawnList.append(id)


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
                

