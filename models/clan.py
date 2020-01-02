from py2neo.ogm import GraphObject, Property, RelatedFrom

class Clan(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()

    member = RelatedFrom("Player")