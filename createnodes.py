from py2neo import Graph
from graphmodels import Clan, Player, Card, Deck, Battle, Team, WarSeason, War, WarStanding, WarParticipation


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


def create_clan(graph, tag, name, description = None, clan_type = None, score = None, war_trophies = None, member_count = None, required_score = None, donations = None):
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
    deck_hash = deck_node.deckHash(deck)

    deck_node_search = Deck.match(graph, deck_hash).first()

    if deck_node_search is None:
    
        for card in deck:
            node_card = Card.match(graph, card["key"]).first()
            deck_node.contains.add(node_card)

        deck_node.calculateExilir(deck)

        graph.merge(deck_node)
    else:
        deck_node = deck_node_search

    return deck_node


def create_battle(graph, battle_type, utc_time, is_ladder_tournament, battle_mode, team_node, opponent_node):
    
    # validate objects are the correct types
    assert(isinstance(team_node, Team))
    assert(isinstance(opponent_node, Team))

    # todo:
    # add hashing function to identify when a battle has already been recorded

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

    Team_node = Team()

    for player, deck in zip(team, decks):
        # validate the objects are the correct types
        assert(isinstance(player, Player))
        assert(isinstance(deck, Deck))

        Team_node.played_in.add(player)
        Team_node.used_deck.add(deck)

    graph.push(Team_node)

    return Team_node
    