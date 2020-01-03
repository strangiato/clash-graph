from py2neo import Graph

from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

class Clan(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()

    member = RelatedFrom("Player", "Member_In")

class Player(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()

    member_of = RelatedTo("Clan")

clash = Graph(host = "localhost", auth=("neo4j", "test123"))

rares = Clan()
rares.tag = "tag123"
rares.name = "The Blunt Rares"

test = Player()
test.tag = "tag234"
test.name = "Strangiato"
test.member_of.add(rares)

clash.push(rares)
clash.push(test)