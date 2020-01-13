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