from py2neo import Graph

from graphmodels import Clan, Player, Card
import royalerequest

clash = Graph(host = "localhost", auth=("neo4j", "test123"))

def updateCards():
    cards = royalerequest.getCards(base_url, headers)

    for card in cards:
        node_card = Card()
        node_card.key = card["key"]
        node_card.name = card["name"]
        node_card.elixir = card["elixir"]
        node_card.card_type = card["type"]
        node_card.rarity = card["rarity"]
        node_card.description = card["description"]
        clash.push(node_card)

def updateClan(tag):
    clan = royalerequest.getClan(base_url, headers, tag)

    node_clan = Clan()
    node_clan.tag = clan["tag"]
    node_clan.name = clan["name"]
    node_clan.description = clan["description"]
    node_clan.clan_type = clan["type"]
    node_clan.score = clan["score"]
    node_clan.warTrophies = clan["warTrophies"]
    node_clan.memberCount = clan["memberCount"]
    node_clan.requiredScore = clan["requiredScore"]
    node_clan.donations = clan["donations"]

    clash.push(node_clan)

    for player in clan["members"]:
        updatePlayer(player["tag"], node_clan)

def updatePlayer(tag, clan = None):
    player = royalerequest.getPlayer(base_url, headers, tag)

    node_player = Player()
    node_player.tag = player["tag"]
    node_player.name = player["name"]
    node_player.clan_role = player["clan"]["role"]
    node_player.trophies = player["trophies"]
    # node_player.donations = player["clan"]["donations"]
    # node_player.donationsReceived = player["clan"]["donationsReceived"]
    # node_player.donationsDelta = player["clan"]["donationsDelta"]

    if clan != None:
        print(type(clan))
        node_player.member_of.add(clan)

    clash.push(node_player)

if __name__ == "__main__":
    base_url = royalerequest.getBaseURL()
    headers = royalerequest.getHeaders()

    updateCards()
    updateClan("VV80RJY")
