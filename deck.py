from py2neo.ogm import GraphObject, Property

class Deck(GraphObject):
    __primarykey__ = "name"

    name = Property()