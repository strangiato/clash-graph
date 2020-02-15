from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
import hashlib
from statistics import mean


class Card(GraphObject):
    __primarykey__ = "name"

    # key = Property() # not available in clash api
    name = Property()
    elixir = Property()  # not available in clash api
    card_type = Property()  # not available in clash api
    rarity = Property()  # not available in clash api
    description = Property()  # not available in clash api

    def __init__(self, name, max_level):
        self.name = name
        self.rarity = self.get_rarity(max_level)

    def get_rarity(self, max_level):
        if max_level == 13:
            rarity = 'Common'
        elif max_level == 11:
            rarity = 'Rare'
        elif max_level == 8:
            rarity = 'Epic'
        elif max_level == 5:
            rarity = 'Legendary'

        return rarity


class Player(GraphObject):
    __primarykey__ = "tag"

    tag = Property()
    name = Property()
    clan_role = Property()
    trophies = Property()
    level = Property()
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

    def deck_hash(self, deck):
        """
        Set the hash property of the deck using the keys of the cards

        Keyword arguments:
        deck -- a list of eight card keys
        """
        self.deck_size_check(deck)

        hash_sum = 0
        for card in deck:
            card_hash = hashlib.sha1(card["name"].encode('utf-8')).hexdigest()
            hash_sum += int(card_hash, 16)

        hash = hex(hash_sum)

        self.hash = hash

        return hash

    def calculate_exilir(self, deck):
        """
        Calculate the average elixir of the deck

        Keyword arguments:
        deck -- a list of eight card elixirs
        """

        self.deck_size_check(deck)

        elixir_total = 0

        for card in deck:
            elixir_total += card["elixir"]

        average = round(elixir_total / len(deck), 2)

        self.average_elixir = average

        return average

    def deck_size_check(self, deck):
        try:
            assert len(deck) == 8
        except AssertionError as err:
            print("Assert Error for deck: {}".format(deck))
            raise err


class Battle(GraphObject):
    __primarykey__ = "hash"

    hash = Property()
    battle_type = Property()
    utc_time = Property()
    is_ladder_tournament = Property()
    battle_mode = Property()

    battled_in = RelatedFrom("Team")
    won = RelatedFrom("Player")
    lost = RelatedFrom("Player")

    def setHash(self, utc_time, team, opponent):

        hashValues = [utc_time, str(team), str(opponent)]

        hashSum = 0
        for item in hashValues:
            itemHash = hashlib.sha1(item.encode('utf-8')).hexdigest()
            hashSum += int(itemHash, 16)

        hash = hex(hashSum)

        self.hash = hash

        return hash


class Team(GraphObject):

    team_size = Property()

    used_deck = RelatedTo("Deck")
    played_in = RelatedFrom("Player")
    battled_in = RelatedTo("Battle")


class War_Season(GraphObject):
    __primarykey__ = "season_number"

    season_number = Property()

    part_of_season = RelatedFrom("War")


class War(GraphObject):
    __primarykey__ = "war_datetime"

    war_datetime = Property()

    battled_in = RelatedFrom("War_Standing")
    part_of_season = RelatedTo("War_Season")


class War_Standing(GraphObject):
    __primarykey__ = "hash"

    hash = Property()
    participants = Property()
    battles_played = Property()
    wins = Property()
    crowns = Property()
    war_tophies = Property()
    war_trophies_change = Property()

    battled_in = RelatedFrom("War_Participant")
    warred_in = RelatedFrom("Clan")
    results_from = RelatedTo("War")


class Hash_Graph_Object(GraphObject):
    __primarykey__ = "hash"

    hash = Property()

    def get_hash(self, hash_array):

        hashSum = 0
        for item in hash_array:
            itemHash = hashlib.sha1(str(item).encode('utf-8')).hexdigest()
            hashSum += int(itemHash, 16)

        hash = hex(hashSum)

        return hash


class War_Participant(GraphObject):

    # properties set directly
    cards_earned = Property()
    war_battles_count = Property()
    war_battles_played = Property()
    war_battles_wins = Property()
    collection_battles_played = Property()

    # properties calculated
    # not being used today
    war_battles_missed = Property()
    collection_battles_missed = Property()

    # relationships
    battled_in = RelatedFrom("Player")
    resulted_in = RelatedTo("War_Standing")


def get_hash(hash_array):

    hashSum = 0
    for item in hash_array:
        itemHash = hashlib.sha1(str(item).encode('utf-8')).hexdigest()
        hashSum += int(itemHash, 16)

    hash = hex(hashSum)

    return hash
