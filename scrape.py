from py2neo import Graph

from graphmodels import Clan, Player

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