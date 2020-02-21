import royalerequest
import createnodes

from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_handler = logging.FileHandler('logs/scrape.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def update_cards(graph, base_url, headers):
    cards = royalerequest.get_cards(base_url, headers)

    for card in cards["items"]:
        createnodes.create_card(
            graph,
            card["name"],
            card["maxLevel"]
        )


def update_clan(graph, base_url, headers, tag):
    clan = royalerequest.get_clan(base_url, headers, tag)

    clan_node = createnodes.create_clan(
        graph,
        clan["tag"],
        clan["name"],
        clan["description"],
        clan["type"],
        clan["clanScore"],
        clan["clanWarTrophies"],
        clan["requiredTrophies"],
        clan["donationsPerWeek"]
    )

    clanMembers = []

    for player in clan["memberList"]:
        createnodes.create_player(
            graph,
            player["tag"],
            player["name"],
            player["trophies"],
            player["expLevel"],
            player["role"],
            clan_node
        )

        clanMembers.append(player["tag"])

    return clanMembers


def update_clan_warlog(graph, base_url, headers, tag, clans):
    warlog = royalerequest.get_warlog(base_url, headers, tag)

    primary_clan_node = createnodes.create_clan(
        graph,
        tag
    )

    primary_war_standing_node = None

    for war in warlog["items"]:

        logger.debug(war)

        war_season_node = createnodes.create_war_season(
            graph,
            war["seasonId"]
        )

        logger.debug(war_season_node)

        war_node = createnodes.create_war(
            graph,
            war["createdDate"],
            war_season_node
        )

        for standing, clan_results in enumerate(war["standings"], start=1):

            # add the clan to the list of clans to scrape
            if clan_results["clan"]["tag"] not in clans:
                clans.append(clan_results["clan"]["tag"])

            clan_node = createnodes.create_clan(
                graph,
                clan_results["clan"]["tag"],
                clan_results["clan"]["name"]
            )

            war_standing_node = createnodes.create_war_standing(
                graph,
                clan_results["clan"]["participants"],
                clan_results["clan"]["battlesPlayed"],
                clan_results["clan"]["wins"],
                clan_results["clan"]["crowns"],
                clan_results["trophyChange"],
                standing,
                clan_node,
                war_node
            )

            if clan_node == primary_clan_node:
                primary_war_standing_node = war_standing_node

        for participant in war["participants"]:
            player_node = createnodes.create_player(
                graph,
                participant["tag"],
                participant["name"]
            )

            createnodes.create_war_participant(
                graph,
                participant["cardsEarned"],
                participant["numberOfBattles"],
                participant["battlesPlayed"],
                participant["wins"],
                participant["collectionDayBattlesPlayed"],
                player_node,
                primary_war_standing_node
            )
    return clans


def update_battles(graph, base_url, headers, tag):
    battles = royalerequest.get_battles(base_url, headers, tag)

    MODES = [
        "Touchdown_MegaDeck_Challenge",
        "Touchdown_MegaDeck_Ladder",
        "DoubleDeck_Tournament",
        "DoubleDeck_Friendly"
    ]

    for battle in battles:
        # skip game modes because they use two decks for each player
        if battle["gameMode"]["name"] in MODES:
            continue

        team_node = update_team(graph, battle["team"])
        opponent_node = update_team(graph, battle["opponent"])

        createnodes.create_battle(
            graph,
            battle["type"],
            battle["battleTime"],
            battle["isLadderTournament"],
            battle["gameMode"]["name"],
            battle["team"][0]["crowns"],
            battle["opponent"][0]["crowns"],
            team_node,
            opponent_node
        )


def update_team(graph, team):
    team_list = []
    deck_list = []

    for player in team:

        clan_node = None
        # get the clan if they have one
        if "clan" in player:
            clan_node = createnodes.create_clan(
                graph,
                player["clan"]["tag"],
                player["clan"]["name"]
            )

        team_list.append(createnodes.create_player(
            graph,
            player["tag"],
            player["name"],
            clan_node=clan_node
        ))

        deck_list.append(createnodes.create_deck(
            graph,
            player["cards"]
        ))

    team_node = createnodes.create_team(
        graph,
        team_list,
        deck_list
    )

    return team_node


if __name__ == "__main__":

    start_time = datetime.now()

    graph = createnodes.get_graph()
    BASE_URL = royalerequest.get_base_url()
    HEADERS = royalerequest.get_headers()

    clans = ["#VV80RJY"]
    players = []

    update_cards(graph, BASE_URL, HEADERS)

    for depth, clan in enumerate(clans, start=1):
        clan_members = update_clan(graph, BASE_URL, HEADERS, clan)
        players.extend(clan_members)

        clans = update_clan_warlog(graph, BASE_URL, HEADERS, clan, clans)

        # this is not really a depth tracker
        # instead it just looks at the number of clans scanned
        # would like to eventually look at this for true depth tracking
        if depth == 50:
            break

    for player in players:
        update_battles(graph, BASE_URL, HEADERS, player)

    logger.info("run time - {}".format(datetime.now() - start_time))
