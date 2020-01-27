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

    def deck_hash(self, deck):
        
        """
        Set the hash property of the deck using the keys of the cards

        Keyword arguments:
        deck -- a list of eight card keys
        """
        self.deck_size_check(deck)

        hash_sum = 0
        for card in deck:
            card_hash = hashlib.sha1(card["key"].encode('utf-8')).hexdigest()
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


class WarSeason(GraphObject):
    __primarykey__ = "season_number"

    season_number = Property

    part_of_season = RelatedFrom("War")


class War(GraphObject):

    war_end_time = Property()

    battled_in = RelatedFrom("WarStanding")
    part_of_season = RelatedTo("WarSeason")
    

class WarStanding(GraphObject):

    participants = Property()
    battles_played = Property()
    wins = Property()
    crowns = Property()
    war_tophies = Property()
    war_trophies_change = Property()

    battled_in = RelatedFrom("WarParticipation")
    battled_in = RelatedTo("War")


class WarParticipation(GraphObject):
    
    cards_earched = Property()
    battle_count = Property()
    battles_played = Property()
    battles_missed = Property()
    wins = Property()
    collection_day_battles_played = Property()

    battled_in = RelatedFrom("Player")
    battled_in = RelatedTo("WarStanding")
