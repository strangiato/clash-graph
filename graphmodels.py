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
    donations_rceived = Property()
    donations_delta = Property()

    member_of = RelatedTo("Clan")

class Clan(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()
    description = Property()
    clan_type = Property()
    score = Property()
    war_trophies = Property()
    member_count = Property()
    required_score = Property()
    donations = Property()

    member_of = RelatedFrom("Player")

class Deck(GraphObject):
    __primarykey__ = "hash"

    hash = Property()
    average_elixir = Property()

    contains = RelatedTo("Card")
    played = RelatedFrom("Player")

    def deckHash(self, deck):
        
        """
        Set the hash property of the deck using the keys of the cards

        Keyword arguments:
        deck -- a list of eight card keys
        """
        self.deckSizeCheck(deck)

        hashSum = 0
        for card in deck:
            cardHash = hashlib.sha1(card["key"].encode('utf-8')).hexdigest()
            hashSum += int(cardHash, 16)

        hash = hex(hashSum)

        self.hash = hash
        
        return hash

    def calculateExilir(self, deck):
        """
        Calculate the average elixir of the deck

        Keyword arguments:
        deck -- a list of eight card elixirs
        """

        self.deckSizeCheck(deck)

        elixirTotal = 0

        for card in deck:
            elixirTotal += card["elixir"]

        average = round(elixirTotal / len(deck), 2)

        self.average_elixir = average

        return average

    def deckSizeCheck(self, deck):
        try:
            assert len(deck) == 8
        except AssertionError as err:
            print("Assert Error for deck: {}".format(deck))
            raise err

class Battle(GraphObject):

    battle_type = Property()
    utc_time = Property()
    is_ladder_tournament = Property()
    battle_mode = Property()

    battled_in = RelatedFrom("BattleTeam")
    won = RelatedFrom("Player")
    lost = RelatedFrom("Player")

class BattleTeam(GraphObject):

    team_size = Property()

    used_deck = RelatedTo("Deck")
    played_in = RelatedFrom("Player")
    battled_in = RelatedTo("Battle")
