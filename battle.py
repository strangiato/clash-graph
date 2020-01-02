from py2neo.ogm import GraphObject, Property

class Battle(GraphObject):
    __primarykey__ = "name"

    name = Property()
    battle_type = Property()
    utcTime = Property()