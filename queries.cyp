// Game Type Counts
Match (c:Clan)--(p:Player)--(t:Team)--(b:Battle)
Where c.tag="VV80RJY"
Return b.battle_mode, count(b)
Order By count(b) DESC

// Unique Decks Count
Match (c:Clan)--(p:Player)--(t:Team)--(d:Deck)
Where c.tag="VV80RJY"
Return p.name, count(distinct d) as DecksPlayed
Order by DecksPlayed DESC

// War Participation
MATCH (c:Clan)--(p:Player)--(wp:War_Participant)
WHERE c.name = "the blunt rares"
RETURN 
p.name as Player, 
p.clan_role as Role,
Sum(wp.collection_day_battles_played) as Collections_Played, 
(count(wp) * 3) as Collections,
Sum(wp.battles_played) as Battles_Played,
Sum(wp.battle_count) as Battles,
100.0 * ((Sum(wp.collection_day_battles_played) + Sum(wp.battles_played)) / ((count(wp) * 3.0) + Sum(wp.battle_count))) as Participation_Score
ORDER BY Participation_Score DESC