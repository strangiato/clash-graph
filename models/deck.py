from py2neo.ogm import GraphObject, Property, RelatedFrom

class Deck(GraphObject):
    __primarykey__ = "hash"

    hash = Property()

    used_in = RelatedFrom("Card")