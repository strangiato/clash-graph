from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

class Card(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    elixer = Property()
    card_type = Property()
    rarity = Property()

class Player(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()

    member_of = RelatedTo("Clan")

class Clan(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()

    member = RelatedFrom("Player")

class Deck(GraphObject):
    __primarykey__ = "hash"

    hash = Property()

    used_in = RelatedFrom("Card")

class Battle(GraphObject):
    __primarykey__ = "name"

    name = Property()
    battle_type = Property()
    utcTime = Property()

    won = RelatedFrom("Player")
    lost = RelatedFrom("Player")