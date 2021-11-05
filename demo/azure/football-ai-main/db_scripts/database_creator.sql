-- ****************** SqlDBM: Microsoft SQL Server ******************
-- ******************************************************************

-- ************************************** [fixtures]

CREATE TABLE [fixtures]
(
 [fixture_id]                 integer NOT NULL ,
 [league_id]                  integer NULL ,
 [event_date]                 datetime NULL ,
 [event_timestamp]            integer NULL ,
 [firstHalfStart]             integer NULL ,
 [secondHalfStart]            integer NULL ,
 [round]                      text NULL ,
 [status]                     text NULL ,
 [statusShort]                text NULL ,
 [elapsed]                    integer NULL ,
 [venue]                      text NULL ,
 [referee]                    text NULL ,
 [goalsHomeTeam]              integer NULL ,
 [goalsAwayTeam]              integer NULL ,
 [league.name]                text NULL ,
 [league.country]             text NULL ,
 [league.logo]                text NULL ,
 [league.flag]                text NULL ,
 [homeTeam.team_id]           integer NULL ,
 [homeTeam.team_name]         text NULL ,
 [homeTeam.logo]              text NULL ,
 [awayTeam.team_id]           integer NULL ,
 [awayTeam.team_name]         text NULL ,
 [awayTeam.logo]              text NULL ,
 [score.halftime]             text NULL ,
 [score.fulltime]             text NULL ,
 [score.extratime]            text NULL ,
 [score.penalty]              text NULL ,
 [lineups.homeTeam.coach]     text NULL ,
 [lineups.homeTeam.coach_id]  integer NULL ,
 [lineups.homeTeam.formation] text NULL ,
 [lineups.awayTeam.coach]     text NULL ,
 [lineups.awayTeam.coach_id]  integer NULL ,
 [lineups.awayTeam.formation] text NULL ,


 CONSTRAINT [PK_fixtures] PRIMARY KEY CLUSTERED ([fixture_id] ASC)
);
GO








-- ****************** SqlDBM: Microsoft SQL Server ******************
-- ******************************************************************

-- ************************************** [events]

CREATE TABLE [events]
(
 [fixture_id]   integer NOT NULL ,
 [id]           integer IDENTITY (1, 1) NOT NULL ,
 [elapsed]      integer NOT NULL ,
 [elapsed_plus] text NULL ,
 [team_id]      integer NULL ,
 [teamName]     text NULL ,
 [player_id]    integer NULL ,
 [player]       text NULL ,
 [assist_id]    real NULL ,
 [assist]       text NULL ,
 [type]         text NULL ,
 [detail]       text NULL ,
 [comments]     text NULL ,


 CONSTRAINT [PK_events] PRIMARY KEY CLUSTERED ([id] ASC),
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_436] ON [events] 
 (
  [fixture_id] ASC
 )

GO







-- ****************** SqlDBM: Microsoft SQL Server ******************
-- ******************************************************************

-- ************************************** [lineups]

CREATE TABLE [lineups]
(
 [fixture_id]  integer NOT NULL ,
 [player_id]   integer NOT NULL ,
 [team_id]     integer NULL ,
 [player]      text NULL ,
 [number]      integer NULL ,
 [pos]         text NULL ,
 [is_homeTeam] bit NOT NULL ,
 [is_startXI]  bit NOT NULL ,


 CONSTRAINT [PK_lineups] PRIMARY KEY CLUSTERED ([fixture_id] ASC, [player_id] ASC, [is_startXI] ASC),
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_449] ON [lineups] 
 (
  [fixture_id] ASC
 )

GO







-- ****************** SqlDBM: Microsoft SQL Server ******************
-- ******************************************************************

-- ************************************** [players]
drop table players
CREATE TABLE [players]
(
 [id]           integer IDENTITY (1, 1) NOT NULL ,
 [fixture_id]            integer NOT NULL ,
 [player_id]             integer NOT NULL ,
 [updateAt]              integer NULL ,
 [player_name]           text NULL ,
 [team_id]               integer NULL ,
 [team_name]             text NULL ,
 [number]                integer NULL ,
 [position]              text NULL ,
 [rating]                real NULL ,
 [minutes_played]        real NULL ,
 [captain]               integer NULL ,
 [substitute]            integer NULL ,
 [offsides]              real NULL ,
 [shots.total]           integer NULL ,
 [shots.on]              integer NULL ,
 [goals.total]           integer NULL ,
 [goals.conceded]        integer NULL ,
 [goals.assists]         integer NULL ,
 [goals.saves]           integer NULL ,
 [passes.total]          integer NULL ,
 [passes.key]            integer NULL ,
 [passes.accuracy]       integer NULL ,
 [tackles.total]         integer NULL ,
 [tackles.blocks]        integer NULL ,
 [tackles.interceptions] integer NULL ,
 [duels.total]           integer NULL ,
 [duels.won]             integer NULL ,
 [dribbles.attempts]     integer NULL ,
 [dribbles.success]      integer NULL ,
 [dribbles.past]         integer NULL ,
 [fouls.drawn]           integer NULL ,
 [fouls.committed]       integer NULL ,
 [cards.yellow]          integer NULL ,
 [cards.red]             integer NULL ,
 [penalty.won]           integer NULL ,
 [penalty.commited]      integer NULL ,
 [penalty.success]       integer NULL ,
 [penalty.missed]        integer NULL ,
 [penalty.saved]         integer NULL ,


 CONSTRAINT [PK_players] PRIMARY KEY CLUSTERED ([id] ASC),
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_445] ON [players] 
 (
  [id] ASC
 )

GO







-- ****************** SqlDBM: Microsoft SQL Server ******************
-- ******************************************************************

-- ************************************** [predictions]

CREATE TABLE [predictions]
(
 [fixture_id]                                              integer NOT NULL ,
 [match_winner]                                            text NULL ,
 [under_over]                                              real NULL ,
 [goals_home]                                              real NULL ,
 [goals_away]                                              real NULL ,
 [advice]                                                  text NULL ,
 [winning_percent.home]                                    real NULL ,
 [winning_percent.draws]                                   real NULL ,
 [winning_percent.away]                                    real NULL ,
 [teams.home.team_id]                                      integer NULL ,
 [teams.home.team_name]                                    text NULL ,
 [teams.home.last_5_matches.forme]                         real NULL ,
 [teams.home.last_5_matches.att]                           real NULL ,
 [teams.home.last_5_matches.def]                           real NULL ,
 [teams.home.last_5_matches.goals]                         integer NULL ,
 [teams.home.last_5_matches.goals_avg]                     real NULL ,
 [teams.home.last_5_matches.goals_against]                 integer NULL ,
 [teams.home.last_5_matches.goals_against_avg]             real NULL ,
 [teams.home.all_last_matches.matchs.matchsPlayed.home]    integer NULL ,
 [teams.home.all_last_matches.matchs.matchsPlayed.away]    integer NULL ,
 [teams.home.all_last_matches.matchs.matchsPlayed.total]   integer NULL ,
 [teams.home.all_last_matches.matchs.wins.home]            integer NULL ,
 [teams.home.all_last_matches.matchs.wins.away]            integer NULL ,
 [teams.home.all_last_matches.matchs.wins.total]           integer NULL ,
 [teams.home.all_last_matches.matchs.draws.home]           integer NULL ,
 [teams.home.all_last_matches.matchs.draws.away]           integer NULL ,
 [teams.home.all_last_matches.matchs.draws.total]          integer NULL ,
 [teams.home.all_last_matches.matchs.loses.home]           integer NULL ,
 [teams.home.all_last_matches.matchs.loses.away]           integer NULL ,
 [teams.home.all_last_matches.matchs.loses.total]          integer NULL ,
 [teams.home.all_last_matches.goals.goalsFor.home]         integer NULL ,
 [teams.home.all_last_matches.goals.goalsFor.away]         integer NULL ,
 [teams.home.all_last_matches.goals.goalsFor.total]        integer NULL ,
 [teams.home.all_last_matches.goals.goalsAgainst.home]     integer NULL ,
 [teams.home.all_last_matches.goals.goalsAgainst.away]     integer NULL ,
 [teams.home.all_last_matches.goals.goalsAgainst.total]    integer NULL ,
 [teams.home.all_last_matches.goalsAvg.goalsFor.home]      real NULL ,
 [teams.home.all_last_matches.goalsAvg.goalsFor.away]      real NULL ,
 [teams.home.all_last_matches.goalsAvg.goalsFor.total]     real NULL ,
 [teams.home.all_last_matches.goalsAvg.goalsAgainst.home]  real NULL ,
 [teams.home.all_last_matches.goalsAvg.goalsAgainst.away]  real NULL ,
 [teams.home.all_last_matches.goalsAvg.goalsAgainst.total] real NULL ,
 [teams.home.last_h2h.played.home]                         integer NULL ,
 [teams.home.last_h2h.played.away]                         integer NULL ,
 [teams.home.last_h2h.played.total]                        integer NULL ,
 [teams.home.last_h2h.wins.home]                           integer NULL ,
 [teams.home.last_h2h.wins.away]                           integer NULL ,
 [teams.home.last_h2h.wins.total]                          integer NULL ,
 [teams.home.last_h2h.draws.home]                          integer NULL ,
 [teams.home.last_h2h.draws.away]                          integer NULL ,
 [teams.home.last_h2h.draws.total]                         integer NULL ,
 [teams.home.last_h2h.loses.home]                          integer NULL ,
 [teams.home.last_h2h.loses.away]                          integer NULL ,
 [teams.home.last_h2h.loses.total]                         integer NULL ,
 [teams.away.team_id]                                      integer NULL ,
 [teams.away.team_name]                                    text NULL ,
 [teams.away.last_5_matches.forme]                         real NULL ,
 [teams.away.last_5_matches.att]                           real NULL ,
 [teams.away.last_5_matches.def]                           real NULL ,
 [teams.away.last_5_matches.goals]                         integer NULL ,
 [teams.away.last_5_matches.goals_avg]                     real NULL ,
 [teams.away.last_5_matches.goals_against]                 integer NULL ,
 [teams.away.last_5_matches.goals_against_avg]             real NULL ,
 [teams.away.all_last_matches.matchs.matchsPlayed.home]    integer NULL ,
 [teams.away.all_last_matches.matchs.matchsPlayed.away]    integer NULL ,
 [teams.away.all_last_matches.matchs.matchsPlayed.total]   integer NULL ,
 [teams.away.all_last_matches.matchs.wins.home]            integer NULL ,
 [teams.away.all_last_matches.matchs.wins.away]            integer NULL ,
 [teams.away.all_last_matches.matchs.wins.total]           integer NULL ,
 [teams.away.all_last_matches.matchs.draws.home]           integer NULL ,
 [teams.away.all_last_matches.matchs.draws.away]           integer NULL ,
 [teams.away.all_last_matches.matchs.draws.total]          integer NULL ,
 [teams.away.all_last_matches.matchs.loses.home]           integer NULL ,
 [teams.away.all_last_matches.matchs.loses.away]           integer NULL ,
 [teams.away.all_last_matches.matchs.loses.total]          integer NULL ,
 [teams.away.all_last_matches.goals.goalsFor.home]         integer NULL ,
 [teams.away.all_last_matches.goals.goalsFor.away]         integer NULL ,
 [teams.away.all_last_matches.goals.goalsFor.total]        integer NULL ,
 [teams.away.all_last_matches.goals.goalsAgainst.home]     integer NULL ,
 [teams.away.all_last_matches.goals.goalsAgainst.away]     integer NULL ,
 [teams.away.all_last_matches.goals.goalsAgainst.total]    integer NULL ,
 [teams.away.all_last_matches.goalsAvg.goalsFor.home]      real NULL ,
 [teams.away.all_last_matches.goalsAvg.goalsFor.away]      real NULL ,
 [teams.away.all_last_matches.goalsAvg.goalsFor.total]     real NULL ,
 [teams.away.all_last_matches.goalsAvg.goalsAgainst.home]  real NULL ,
 [teams.away.all_last_matches.goalsAvg.goalsAgainst.away]  real NULL ,
 [teams.away.all_last_matches.goalsAvg.goalsAgainst.total] real NULL ,
 [teams.away.last_h2h.played.home]                         integer NULL ,
 [teams.away.last_h2h.played.away]                         integer NULL ,
 [teams.away.last_h2h.played.total]                        integer NULL ,
 [teams.away.last_h2h.wins.home]                           integer NULL ,
 [teams.away.last_h2h.wins.away]                           integer NULL ,
 [teams.away.last_h2h.wins.total]                          integer NULL ,
 [teams.away.last_h2h.draws.home]                          integer NULL ,
 [teams.away.last_h2h.draws.away]                          integer NULL ,
 [teams.away.last_h2h.draws.total]                         integer NULL ,
 [teams.away.last_h2h.loses.home]                          integer NULL ,
 [teams.away.last_h2h.loses.away]                          integer NULL ,
 [teams.away.last_h2h.loses.total]                         integer NULL ,
 [comparison.forme.home]                                   real NULL ,
 [comparison.forme.away]                                   real NULL ,
 [comparison.att.home]                                     real NULL ,
 [comparison.att.away]                                     real NULL ,
 [comparison.def.home]                                     real NULL ,
 [comparison.def.away]                                     real NULL ,
 [comparison.fish_law.home]                                real NULL ,
 [comparison.fish_law.away]                                real NULL ,
 [comparison.h2h.home]                                     real NULL ,
 [comparison.h2h.away]                                     real NULL ,
 [comparison.goals_h2h.home]                               real NULL ,
 [comparison.goals_h2h.away]                               real NULL ,


 CONSTRAINT [PK_predictions] PRIMARY KEY CLUSTERED ([fixture_id] ASC),
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_453] ON [predictions] 
 (
  [fixture_id] ASC
 )

GO







-- ****************** SqlDBM: Microsoft SQL Server ******************
-- ******************************************************************

-- ************************************** [statistics]

CREATE TABLE [fixture_statistics]
(
 [fixture_id]           integer NOT NULL ,
 [ShotsonGoal.home]     integer NULL ,
 [ShotsonGoal.away]     integer NULL ,
 [ShotsoffGoal.home]    integer NULL ,
 [ShotsoffGoal.away]    integer NULL ,
 [TotalShots.home]      integer NULL ,
 [TotalShots.away]      integer NULL ,
 [BlockedShots.home]    integer NULL ,
 [BlockedShots.away]    integer NULL ,
 [Shotsinsidebox.home]  integer NULL ,
 [Shotsinsidebox.away]  integer NULL ,
 [Shotsoutsidebox.home] integer NULL ,
 [Shotsoutsidebox.away] integer NULL ,
 [Fouls.home]           integer NULL ,
 [Fouls.away]           integer NULL ,
 [CornerKicks.home]     integer NULL ,
 [CornerKicks.away]     integer NULL ,
 [Offsides.home]        integer NULL ,
 [Offsides.away]        integer NULL ,
 [BallPossession.home]  real NULL ,
 [BallPossession.away]  real NULL ,
 [YellowCards.home]     integer NULL ,
 [YellowCards.away]     integer NULL ,
 [RedCards.home]        integer NULL ,
 [RedCards.away]        integer NULL ,
 [GoalkeeperSaves.home] integer NULL ,
 [GoalkeeperSaves.away] integer NULL ,
 [Totalpasses.home]     integer NULL ,
 [Totalpasses.away]     integer NULL ,
 [Passesaccurate.home]  integer NULL ,
 [Passesaccurate.away]  integer NULL ,
 [Passes%.home]         real NULL ,
 [Passes%.away]         real NULL ,


 CONSTRAINT [PK_statistics] PRIMARY KEY CLUSTERED ([fixture_id] ASC),
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_441] ON [statistics] 
 (
  [fixture_id] ASC
 )

GO







-- ****************** SqlDBM: Microsoft SQL Server ******************
-- ******************************************************************

-- ************************************** [odds]

CREATE TABLE [odds]
(
 [id]                 integer IDENTITY (1, 1) NOT NULL ,
 [value]              text NULL ,
 [odd]                real NULL ,
 [label_id]           integer NOT NULL ,
 [label_name]         text NULL ,
 [bookmaker_id]       integer NOT NULL ,
 [bookmaker_name]     text NULL ,
 [fixture.fixture_id] integer NOT NULL ,
 [fixture.league_id]  integer NULL ,
 [fixture.updateAt]   integer NOT NULL ,


 CONSTRAINT [PK_odds] PRIMARY KEY CLUSTERED ([id] ASC),
);
GO


CREATE NONCLUSTERED INDEX [fkIdx_467] ON [odds] 
 (
  [fixture.fixture_id] ASC
 )

GO






-- ******************************************************************

-- ************************************** [odds_mappings]

CREATE TABLE [odds_mappings]
(
 [fixture_id]   integer NOT NULL ,
 [updateAt]     integer NOT NULL ,
 [lastUpdateAt] integer NULL ,


 CONSTRAINT [PK_odds_mappings] PRIMARY KEY CLUSTERED ([fixture_id] ASC)
);
GO



