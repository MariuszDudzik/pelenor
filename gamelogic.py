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