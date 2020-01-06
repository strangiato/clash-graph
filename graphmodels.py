from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
import hashlib

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

    member_of = RelatedFrom("Player")

class Deck(GraphObject):
    __primarykey__ = "hash"

    hash = Property()

    contains = RelatedTo("Card")
    played = RelatedFrom("Player")

    def hashDeck(self, deck):
        """
        Calculate a hash of

        Keyword arguments:
        deck -- a list of eight card keys
        """

        assert len(deck) == 8

        hashSum = 0

        for card in deck:
            hashSum += int(hashlib.sha1(card.encode('utf-8')).hexdigest(), 16)

        self.hash = hex(hashSum)

class Battle(GraphObject):
    __primarykey__ = "name"

    name = Property()
    battle_type = Property()
    utcTime = Property()

    won = RelatedFrom("Player")
    lost = RelatedFrom("Player")