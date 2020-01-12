from graphmodels import Clan, Player, Card, Deck, Battle, BattleTeam

def createCard(graph, key, name, elixir, card_type, rarity, description):
    card_node = Card.match(graph, key).first()

    if card_node is not None:
    
        card_node = Card()
        card_node.key = key
        card_node.name = name
        card_node.elixir = elixir
        card_node.card_type = card_type
        card_node.rarity = rarity
        card_node.description = description
        graph.push(card_node)

    return card_node

def createClan(graph, tag, name, description = None, clan_type = None, score = None, war_trophies = None, member_count = None, required_score = None, donations = None):
    clan_node = Clan.match(graph, tag).first()

    if clan_node is not None:
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

def createPlayer(graph, tag, name, trophies = None, clan_role = None, clan_node = None):

    player_node = Player.match(graph, tag).first()

    if player_node is not None:
        player_node = Player()
        player_node.tag = tag
        player_node.name = name
        player_node.trophies = trophies
        player_node.clan_role = clan_role

        if clan_node is not None:
            assert(isinstance(clan_node, Clan))
            player_node.member_of.add(clan_node)

        graph.push(player_node)

    return player_node

