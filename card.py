from py2neo.ogm import GraphObject, Property

class Card(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    elixer = Property()
    card_type = Property()
    rarity = Property()