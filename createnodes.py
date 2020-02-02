from py2neo import Graph
from graphmodels import Clan, Player, Card, Deck, Battle, Team, War_Season, War, War_Standing, War_Participant
from graphmodels import get_hash


def get_graph():
    return Graph(host = "localhost", auth=("neo4j", "test123"))


def create_card(graph, key, name, elixir, card_type, rarity, description):
    card_node = Card.match(graph, key).first()

    if card_node is None:
        card_node = Card()
        card_node.key = key
        card_node.name = name
        card_node.elixir = elixir
        card_node.card_type = card_type
        card_node.rarity = rarity
        card_node.description = description
        graph.push(card_node)

    return card_node


def create_clan(graph, tag, name = None, description = None, clan_type = None, score = None, war_trophies = None, member_count = None, required_score = None, donations = None):
    clan_node = Clan.match(graph, tag).first()

    if clan_node is None:
        clan_node = Clan()
        clan_node.tag = tag
        clan_node.name = name
        clan_node.description = description
        clan_node.clan_type = clan_type
        clan_node.score = score
        clan_node.war_trophies = war_trophies
        clan_node.member_count = member_count
        clan_node.required_score = required_score
        clan_node.donations = donations

        graph.push(clan_node)

    return clan_node

def create_player(graph, tag, name, trophies = None, clan_role = None, clan_node = None):
    player_node = Player.match(graph, tag).first()

    if player_node is None:
        player_node = Player()
        player_node.tag = tag
        player_node.name = name
        player_node.trophies = trophies
        player_node.clan_role = clan_role

        # does this need to be outside of the if block
        # possible issue when player is created then joins clan
        if clan_node is not None:
            assert(isinstance(clan_node, Clan))
            player_node.member_of.add(clan_node)

        graph.push(player_node)

    return player_node


def create_deck(graph, deck):

    deck_node = Deck()
    deck_hash = deck_node.deck_hash(deck)

    deck_node_search = Deck.match(graph, deck_hash).first()

    if deck_node_search is None:
    
        for card in deck:
            node_card = Card.match(graph, card["key"]).first()
            deck_node.contains.add(node_card)

        deck_node.calculate_exilir(deck)

        graph.merge(deck_node)
    else:
        deck_node = deck_node_search

    return deck_node


def create_battle(graph, battle_type, utc_time, is_ladder_tournament, battle_mode, team_node, opponent_node):
    
    # validate objects are the correct types
    assert(isinstance(team_node, Team))
    assert(isinstance(opponent_node, Team))

    battle_node = Battle()
    battle_hash = battle_node.setHash(utc_time, team_node, opponent_node)

    battle_node_search = Battle.match(graph, battle_hash).first()

    if battle_node_search is None:

        battle_node = Battle()

        battle_node.setHash(utc_time, team_node, opponent_node)

        battle_node.battle_type = battle_type
        battle_node.utc_time = utc_time
        battle_node.is_ladder_tournament = is_ladder_tournament
        battle_node.battle_mode = battle_mode

        # todo:
        # add won/lost properties to relationship
        battle_node.battled_in.add(team_node)
        battle_node.battled_in.add(opponent_node)
        
        graph.push(battle_node)
    else:
        battle_node = battle_node_search

    return battle_node


def create_team(graph, team, decks):
    
    # validate that the same number of teammembers and decks were provided
    assert(len(team) == len(decks))

    team_node = Team()

    for player, deck in zip(team, decks):
        # validate the objects are the correct types
        assert(isinstance(player, Player))
        assert(isinstance(deck, Deck))

        team_node.played_in.add(player)
        team_node.used_deck.add(deck)

    graph.push(team_node)

    return team_node


def create_war_season(graph, war_season):
    season_node = War_Season.match(graph, war_season).first()

    if season_node is None:
        season_node = War_Season()

        season_node.season_number = war_season

        graph.push(season_node)
    
    return season_node


def create_war(graph, war_end_time, war_season_node):
    assert(isinstance(war_season_node, War_Season))

    war_node = War.match(graph, war_end_time).first()

    if war_node is None:
        war_node = War()

        war_node.war_end_time = war_end_time

        war_node.part_of_season.add(war_season_node)

        graph.push(war_node)

    return war_node


def get_war_standing(graph, clan_node, war_node):
    assert(isinstance(clan_node, Clan))
    assert(isinstance(war_node, War))

    war_standing_hash = get_hash([clan_node, war_node])
    war_standing_node = War_Standing.match(graph, war_standing_hash).first()

    return war_standing_node, war_standing_hash


def create_war_standing(graph, participants, battles_played, wins, crowns, war_tophies, war_trophies_change, clan_node, war_node):

    war_standing_node, war_standing_hash = get_war_standing(graph, clan_node, war_node)

    if war_standing_node is None:
        war_standing_node = War_Standing()

        war_standing_node.hash = war_standing_hash
        war_standing_node.participants = participants
        war_standing_node.battles_played = battles_played
        war_standing_node.wins = wins
        war_standing_node.crowns = crowns
        war_standing_node.war_tophies = war_tophies
        war_standing_node.war_trophies_change = war_trophies_change

        war_standing_node.warred_in.add(clan_node)
        war_standing_node.results_from.add(war_node)

        graph.push(war_standing_node)

    return war_standing_node


def get_war_participant(graph, player_node, war_standing_node):
    assert(isinstance(player_node, Player))
    assert(isinstance(war_standing_node, War_Standing))

    war_participant_hash = get_hash([player_node, war_standing_node])
    war_participant_node = War_Participant.match(graph, war_participant_hash).first()

    return war_participant_node, war_participant_hash


def create_war_participant(graph, cards_earned, battle_count, battles_played, battles_missed, wins, collection_day_battles_played, player_node, war_standing_node):

    war_participant_node, war_participant_hash = get_war_participant(graph, player_node, war_standing_node)

    if war_participant_node is None:
        war_participant_node = War_Participant()

        war_participant_node.hash = war_participant_hash
        war_participant_node.cards_earned = cards_earned
        war_participant_node.battle_count = battle_count
        war_participant_node.battles_played = battles_played
        war_participant_node.battles_missed = battles_missed
        war_participant_node.wins = wins
        war_participant_node.collection_day_battles_played = collection_day_battles_played

        war_participant_node.battled_in.add(player_node)
        war_participant_node.resulted_in.add(war_standing_node)

        graph.push(war_participant_node)

    return war_participant_node

if __name__ == "__main__":

    graph = get_graph()
    war_season = create_war_season(graph, 1)
    print(war_season)