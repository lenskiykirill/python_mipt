class Spell:
    def __init__(self, name, formula, \
                 recharge = None, cast = None):

        self.name     = name
        self.formula  = formula
        self.recharge = recharge
        self.cast     = cast

        self.last_casted = None

class Object:
    def __init__(self, name, description):
        self.name        = name
        self.description = description

class Player:
    
    occultist = 10
    cultist   = 20
    enlighted = 40

    def __init__(self, health = 100):

        self.health = health
        self.spells = dict()
        self.magica = 0

        self.title  = "occultist"

        self.inventory = list()
        self.spells    = list()

    def set_title(self):

        if (self.magica < self.occultist):
            self.title = "occultist"
            return

        if (self.magica < self.cultist):
            self.title = "cultist"
            return

        if (self.magica < self.enlighted):
            self.title = "enlightened"
            return

        self.title = "Bill Cypher"

class Option:
    def __init__(self, text="", node=""):
        self.text = text
        self.node = node

class Action:
    add             = 0
    remove          = 1
    increase_health = 2
    reduce_health   = 3

    # Action.object_name
    # Action.amount

    def __init__(self):
        self.action_type = None

class Node:
    def __init__(self):
        self.text          = ""
        self.options       = list() # contains user-shown options
        self.actions       = list()
        self.spell_options = dict()
        self.duration      = 1

