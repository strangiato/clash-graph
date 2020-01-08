from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
import hashlib
from statistics import mean 

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
    average_elixir = Property()

    contains = RelatedTo("Card")
    played = RelatedFrom("Player")

    def hashDeck(self, deck):
        """
        Calculate a hash of the keys of the cards in the deck

        Keyword arguments:
        deck -- a list of eight card keys
        """

        assert len(deck) == 8

        hashSum = 0

        for card in deck:
            hashSum += int(hashlib.sha1(card.encode('utf-8')).hexdigest(), 16)

        self.hash = hex(hashSum)

    def calculateExilir(self, deck):
        """
        Calculate the average elixir of the deck

        Keyword arguments:
        deck -- a list of eight card elixirs
        """

        assert len(deck) == 8

        average = round(mean(deck), 2)

        self.average_elixir = average


class Battle(GraphObject):
    __primarykey__ = "name"

    name = Property()
    battle_type = Property()
    utcTime = Property()

    won = RelatedFrom("Player")
    lost = RelatedFrom("Player")