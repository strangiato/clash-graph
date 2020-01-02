from py2neo.ogm import GraphObject, Property, RelatedFrom

class Battle(GraphObject):
    __primarykey__ = "name"

    name = Property()
    battle_type = Property()
    utcTime = Property()

    won = RelatedFrom("Player")
    lost = RelatedFrom("Player")