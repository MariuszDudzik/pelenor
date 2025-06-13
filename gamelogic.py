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
        """Funkcja pomocnicza do generowania stringa ze statystykami jednostki."""
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