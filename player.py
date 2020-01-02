from py2neo.ogm import GraphObject, Property, RelatedTo

class Player(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()

    member_of = RelatedTo("Clan")