// Create indexes for nodes

CREATE INDEX ON :Battle(hash);
CREATE INDEX ON :Card(key);
CREATE INDEX ON :Card(name);
CREATE INDEX ON :Clan(name);
CREATE INDEX ON :Clan(tag);
CREATE INDEX ON :Deck(hash);
CREATE INDEX ON :Player(name);
CREATE INDEX ON :Player(tag);
CREATE INDEX ON :War(war_end_time);
CREATE INDEX ON :War_Participant(hash);
CREATE INDEX ON :War_Season(season_number);
CREATE INDEX ON :War_Standing(hash);