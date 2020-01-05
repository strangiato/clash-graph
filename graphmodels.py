from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom

class Card(GraphObject):
    __primarykey__ = "key"

    key = Property()
    name = Property()
    elixir = Property()
    card_type = Property()
    rarity = Property()
    description = Property()

class Player(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()
    clan_role = Property()
    trophies = Property()
    donations = Property()
    donationsReceived = Property()
    donationsDelta = Property()

    member_of = RelatedTo("Clan")

class Clan(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()
    description = Property()
    clan_type = Property()
    score = Property()
    warTrophies = Property()
    memberCount = Property()
    requiredScore = Property()
    donations = Property()

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