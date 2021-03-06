/****** Object:  UserDefinedFunction [dbo].[retrieve_fixtures_without_first_n_matches]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION [dbo].[retrieve_fixtures_without_first_n_matches] (@n int)
RETURNS @result TABLE(
	league_id int, fixture_id int, event_timestamp int, goalsHomeTeam int, goalsAwayTeam int, [homeTeam.PowerRating] real, [awayTeam.PowerRating] real
) AS 
BEGIN
	declare @tmp TABLE(league_id int, fixture_id int, event_timestamp int, teams int, ishome int, rownums int)

	insert into @tmp
	select *, ROW_NUMBER() over (partition by league_id, teams order by event_timestamp) as rownums 
	from (
		(select league_id, fixture_id, event_timestamp, [homeTeam.team_id] as teams, 1 as ishome from fixtures) 
		union all 
		(select league_id, fixture_id, event_timestamp, [awayTeam.team_id] as teams, 0 as ishome from fixtures)
	) a
	order by event_timestamp, fixture_id

	insert into @result
	select fixtures.league_id, fixtures.fixture_id, fixtures.event_timestamp, fixtures.goalsHomeTeam, fixtures.goalsAwayTeam,
			fixture_pr.[homeTeam.PowerRating], fixture_pr.[awayTeam.PowerRating]
	from fixtures
	join (
		select tmp.fixture_id, tmp.event_timestamp, rownums as [homeTeam.matchnum], [awayTeam.matchnum] from @tmp as tmp
		join (
			select fixture_id, event_timestamp, teams as [awayTeam.team_id], rownums as [awayTeam.matchnum] from @tmp
			where ishome=0
		) a on a.fixture_id=tmp.fixture_id and a.event_timestamp=tmp.event_timestamp
		where ishome=1 and rownums > @n and [awayTeam.matchnum] > @n
	) a on a.fixture_id=fixtures.fixture_id and a.event_timestamp=fixtures.event_timestamp
	join fixture_pr on fixture_pr.fixture_id=fixtures.fixture_id
	where fixtures.goalsHomeTeam is not null and fixtures.goalsAwayTeam is not null

	return
END
GO
/****** Object:  Table [dbo].[odds]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[odds](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[value] [text] NULL,
	[odd] [real] NULL,
	[label_id] [int] NOT NULL,
	[label_name] [text] NULL,
	[bookmaker_id] [int] NOT NULL,
	[bookmaker_name] [text] NULL,
	[fixture.fixture_id] [int] NOT NULL,
	[fixture.league_id] [int] NULL,
	[fixture.updateAt] [int] NOT NULL,
 CONSTRAINT [PK_odds] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  UserDefinedFunction [dbo].[retrieve_formatted_odds]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[retrieve_formatted_odds] ()
RETURNS TABLE AS RETURN   
(
	select * from (
		select [fixture.fixture_id], odd,  CAST(concat(replace(replace(CONVERT(VARCHAR(MAX), label_name), ' ', '_'), '/', '_'), '.', replace(replace(CONVERT(VARCHAR(MAX), "value"), ' ', '_'), '/', '_'))AS VARCHAR(MAX)) as odd_name
		from odds where label_id in (1, 2, 12)
	) t
	pivot (max(odd) for odd_name in ([Match_Winner.Home], [Match_Winner.Draw], [Match_Winner.Away], 
									[Home_Away.Home], [Home_Away.Away], 
									[Double_Chance.Home_Draw], [Double_Chance.Home_Away], [Double_Chance.Draw_Away])) 
	as pivoted
)
GO
/****** Object:  Table [dbo].[fixtures]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[fixtures](
	[fixture_id] [int] NOT NULL,
	[league_id] [int] NULL,
	[event_date] [datetime] NULL,
	[event_timestamp] [int] NULL,
	[firstHalfStart] [int] NULL,
	[secondHalfStart] [int] NULL,
	[round] [text] NULL,
	[status] [text] NULL,
	[statusShort] [text] NULL,
	[elapsed] [int] NULL,
	[venue] [text] NULL,
	[referee] [text] NULL,
	[goalsHomeTeam] [int] NULL,
	[goalsAwayTeam] [int] NULL,
	[league.name] [text] NULL,
	[league.country] [text] NULL,
	[league.logo] [text] NULL,
	[league.flag] [text] NULL,
	[homeTeam.team_id] [int] NULL,
	[homeTeam.team_name] [text] NULL,
	[homeTeam.logo] [text] NULL,
	[awayTeam.team_id] [int] NULL,
	[awayTeam.team_name] [text] NULL,
	[awayTeam.logo] [text] NULL,
	[score.halftime] [text] NULL,
	[score.fulltime] [text] NULL,
	[score.extratime] [text] NULL,
	[score.penalty] [text] NULL,
	[lineups.homeTeam.coach] [text] NULL,
	[lineups.homeTeam.coach_id] [int] NULL,
	[lineups.homeTeam.formation] [text] NULL,
	[lineups.awayTeam.coach] [text] NULL,
	[lineups.awayTeam.coach_id] [int] NULL,
	[lineups.awayTeam.formation] [text] NULL,
	[insert_date] [datetime] NOT NULL,
 CONSTRAINT [PK_fixtures] PRIMARY KEY CLUSTERED 
(
	[fixture_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  View [dbo].[bi_firs]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

create   view [dbo].[bi_firs]
AS
select 
fx.event_date  as event_date
,fx.[league.flag] as legue_flag
,fx.[league.country] as legue_country
,fx.[league.logo] as legue_logo
,fx.[league.name] as league_name
,fx.[round] as round
,fx.[homeTeam.team_name] as home_team_name
,fx.[homeTeam.logo] as home_team_logo
,fx.[awayTeam.team_name] as away_team_name
,fx.[awayTeam.logo] as away_team_logo
, 0 as home_rating
, 0 as away_rating
, 0 as home_pr
, 0 as away_pr
, 0 as pr_diff
, 0 as rating_diff
, 0 as att_def_diff
, 0 as home_odds
, 0 as home_pr_odds
, 0 as home_rating_diff_odds
, 0 as home_att_def_diff_ods
, 0 as drawn_odds
, 0 as drawn_pr_odds
, 0 as drawn_rating_diff_odds
, 0 as drawn_att_deff_diff_odds
, 0 as away_odds
, 0 as away_pr_odds
, 0 as away_rating_diff_odds
, 0 as away_att_deff_diff_odds
, 0 as match_winner
, 0 as away_win_profit_bet
, 0 as goals_home
, 0 as goals_away
, 0 as advice
, 0 as winning_percent_home
, 0 as winning_percent_draws
, 0 as winning_percent_away
, 0 as all_tip
, 0 as all_odds
, 0 as all_value_odds_diff
, 0 as all_ods

from dbo.fixtures as fx

GO
/****** Object:  UserDefinedFunction [dbo].[retrieve_formatted_label1_odds]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[retrieve_formatted_label1_odds] ()
RETURNS TABLE AS RETURN   
(
	select * from (
		select [fixture.fixture_id] as fixture_id, odd,  CAST(concat(replace(replace(CONVERT(VARCHAR(MAX), label_name), ' ', '_'), '/', '_'), '.', replace(replace(CONVERT(VARCHAR(MAX), "value"), ' ', '_'), '/', '_'))AS VARCHAR(MAX)) as odd_name
		from odds where label_id in (1)
	) t
	pivot (max(odd) for odd_name in ([Match_Winner.Home], [Match_Winner.Draw], [Match_Winner.Away])) 
	as pivoted
)
GO
/****** Object:  Table [dbo].[events]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[events](
	[fixture_id] [int] NOT NULL,
	[id] [int] IDENTITY(1,1) NOT NULL,
	[elapsed] [int] NOT NULL,
	[elapsed_plus] [text] NULL,
	[team_id] [int] NULL,
	[teamName] [text] NULL,
	[player_id] [int] NULL,
	[player] [text] NULL,
	[assist_id] [real] NULL,
	[assist] [text] NULL,
	[type] [text] NULL,
	[detail] [text] NULL,
	[comments] [text] NULL,
 CONSTRAINT [PK_events] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[first_odds]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[first_odds](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[value] [text] NULL,
	[odd] [real] NULL,
	[label_id] [int] NOT NULL,
	[label_name] [text] NULL,
	[bookmaker_id] [int] NOT NULL,
	[bookmaker_name] [text] NULL,
	[fixture.fixture_id] [int] NOT NULL,
	[fixture.league_id] [int] NULL,
	[fixture.updateAt] [int] NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[fixture_pr]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[fixture_pr](
	[fixture_id] [bigint] NULL,
	[homeTeam.PowerRating] [float] NULL,
	[awayTeam.PowerRating] [float] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[fixture_pr_odds_stats]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[fixture_pr_odds_stats](
	[fixture_id] [bigint] NULL,
	[Match_Winner.Home.winCount] [float] NULL,
	[Match_Winner.Draw.winCount] [float] NULL,
	[Match_Winner.Away.winCount] [float] NULL,
	[Match_Winner.Home.loseCount] [float] NULL,
	[Match_Winner.Draw.loseCount] [float] NULL,
	[Match_Winner.Away.loseCount] [float] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[fixture_pr_stats]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[fixture_pr_stats](
	[fixture_id] [bigint] NULL,
	[prHomeWinPercent] [float] NULL,
	[prDrawWinPercent] [float] NULL,
	[prAwayWinPercent] [float] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[fixture_statistics]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[fixture_statistics](
	[fixture_id] [int] NOT NULL,
	[ShotsonGoal.home] [int] NULL,
	[ShotsonGoal.away] [int] NULL,
	[ShotsoffGoal.home] [int] NULL,
	[ShotsoffGoal.away] [int] NULL,
	[TotalShots.home] [int] NULL,
	[TotalShots.away] [int] NULL,
	[BlockedShots.home] [int] NULL,
	[BlockedShots.away] [int] NULL,
	[Shotsinsidebox.home] [int] NULL,
	[Shotsinsidebox.away] [int] NULL,
	[Shotsoutsidebox.home] [int] NULL,
	[Shotsoutsidebox.away] [int] NULL,
	[Fouls.home] [int] NULL,
	[Fouls.away] [int] NULL,
	[CornerKicks.home] [int] NULL,
	[CornerKicks.away] [int] NULL,
	[Offsides.home] [int] NULL,
	[Offsides.away] [int] NULL,
	[BallPossession.home] [real] NULL,
	[BallPossession.away] [real] NULL,
	[YellowCards.home] [int] NULL,
	[YellowCards.away] [int] NULL,
	[RedCards.home] [int] NULL,
	[RedCards.away] [int] NULL,
	[GoalkeeperSaves.home] [int] NULL,
	[GoalkeeperSaves.away] [int] NULL,
	[Totalpasses.home] [int] NULL,
	[Totalpasses.away] [int] NULL,
	[Passesaccurate.home] [int] NULL,
	[Passesaccurate.away] [int] NULL,
	[Passes%.home] [real] NULL,
	[Passes%.away] [real] NULL,
 CONSTRAINT [PK_statistics] PRIMARY KEY CLUSTERED 
(
	[fixture_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[leagues]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[leagues](
	[league_id] [bigint] NULL,
	[name] [varchar](max) NULL,
	[type] [varchar](max) NULL,
	[country] [varchar](max) NULL,
	[country_code] [varchar](max) NULL,
	[season] [bigint] NULL,
	[season_start] [varchar](max) NULL,
	[season_end] [varchar](max) NULL,
	[logo] [varchar](max) NULL,
	[flag] [varchar](max) NULL,
	[standings] [bigint] NULL,
	[is_current] [bigint] NULL,
	[coverage.standings] [bit] NULL,
	[coverage.fixtures.events] [bit] NULL,
	[coverage.fixtures.lineups] [bit] NULL,
	[coverage.fixtures.statistics] [bit] NULL,
	[coverage.fixtures.players_statistics] [bit] NULL,
	[coverage.players] [bit] NULL,
	[coverage.topScorers] [bit] NULL,
	[coverage.predictions] [bit] NULL,
	[coverage.odds] [bit] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[lineups]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[lineups](
	[fixture_id] [int] NOT NULL,
	[player_id] [int] NOT NULL,
	[team_id] [int] NULL,
	[player] [text] NULL,
	[number] [int] NULL,
	[pos] [text] NULL,
	[is_homeTeam] [bit] NOT NULL,
	[is_startXI] [bit] NOT NULL,
 CONSTRAINT [PK_lineups] PRIMARY KEY CLUSTERED 
(
	[fixture_id] ASC,
	[player_id] ASC,
	[is_startXI] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[odds_mappings]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[odds_mappings](
	[fixture_id] [bigint] NULL,
	[updateAt] [bigint] NULL,
	[lastUpdateAt] [float] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[players]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[players](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[fixture_id] [int] NOT NULL,
	[player_id] [int] NOT NULL,
	[updateAt] [int] NULL,
	[player_name] [text] NULL,
	[team_id] [int] NULL,
	[team_name] [text] NULL,
	[number] [int] NULL,
	[position] [text] NULL,
	[rating] [real] NULL,
	[minutes_played] [real] NULL,
	[captain] [int] NULL,
	[substitute] [int] NULL,
	[offsides] [real] NULL,
	[shots.total] [int] NULL,
	[shots.on] [int] NULL,
	[goals.total] [int] NULL,
	[goals.conceded] [int] NULL,
	[goals.assists] [int] NULL,
	[goals.saves] [int] NULL,
	[passes.total] [int] NULL,
	[passes.key] [int] NULL,
	[passes.accuracy] [int] NULL,
	[tackles.total] [int] NULL,
	[tackles.blocks] [int] NULL,
	[tackles.interceptions] [int] NULL,
	[duels.total] [int] NULL,
	[duels.won] [int] NULL,
	[dribbles.attempts] [int] NULL,
	[dribbles.success] [int] NULL,
	[dribbles.past] [int] NULL,
	[fouls.drawn] [int] NULL,
	[fouls.committed] [int] NULL,
	[cards.yellow] [int] NULL,
	[cards.red] [int] NULL,
	[penalty.won] [int] NULL,
	[penalty.commited] [int] NULL,
	[penalty.success] [int] NULL,
	[penalty.missed] [int] NULL,
	[penalty.saved] [int] NULL,
 CONSTRAINT [PK_players] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[predictions]    Script Date: 2021. 02. 01. 15:04:24 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[predictions](
	[fixture_id] [int] NOT NULL,
	[match_winner] [text] NULL,
	[under_over] [real] NULL,
	[goals_home] [real] NULL,
	[goals_away] [real] NULL,
	[advice] [text] NULL,
	[winning_percent.home] [real] NULL,
	[winning_percent.draws] [real] NULL,
	[winning_percent.away] [real] NULL,
	[teams.home.team_id] [int] NULL,
	[teams.home.team_name] [text] NULL,
	[teams.home.last_5_matches.forme] [real] NULL,
	[teams.home.last_5_matches.att] [real] NULL,
	[teams.home.last_5_matches.def] [real] NULL,
	[teams.home.last_5_matches.goals] [int] NULL,
	[teams.home.last_5_matches.goals_avg] [real] NULL,
	[teams.home.last_5_matches.goals_against] [int] NULL,
	[teams.home.last_5_matches.goals_against_avg] [real] NULL,
	[teams.home.all_last_matches.matchs.matchsPlayed.home] [int] NULL,
	[teams.home.all_last_matches.matchs.matchsPlayed.away] [int] NULL,
	[teams.home.all_last_matches.matchs.matchsPlayed.total] [int] NULL,
	[teams.home.all_last_matches.matchs.wins.home] [int] NULL,
	[teams.home.all_last_matches.matchs.wins.away] [int] NULL,
	[teams.home.all_last_matches.matchs.wins.total] [int] NULL,
	[teams.home.all_last_matches.matchs.draws.home] [int] NULL,
	[teams.home.all_last_matches.matchs.draws.away] [int] NULL,
	[teams.home.all_last_matches.matchs.draws.total] [int] NULL,
	[teams.home.all_last_matches.matchs.loses.home] [int] NULL,
	[teams.home.all_last_matches.matchs.loses.away] [int] NULL,
	[teams.home.all_last_matches.matchs.loses.total] [int] NULL,
	[teams.home.all_last_matches.goals.goalsFor.home] [int] NULL,
	[teams.home.all_last_matches.goals.goalsFor.away] [int] NULL,
	[teams.home.all_last_matches.goals.goalsFor.total] [int] NULL,
	[teams.home.all_last_matches.goals.goalsAgainst.home] [int] NULL,
	[teams.home.all_last_matches.goals.goalsAgainst.away] [int] NULL,
	[teams.home.all_last_matches.goals.goalsAgainst.total] [int] NULL,
	[teams.home.all_last_matches.goalsAvg.goalsFor.home] [real] NULL,
	[teams.home.all_last_matches.goalsAvg.goalsFor.away] [real] NULL,
	[teams.home.all_last_matches.goalsAvg.goalsFor.total] [real] NULL,
	[teams.home.all_last_matches.goalsAvg.goalsAgainst.home] [real] NULL,
	[teams.home.all_last_matches.goalsAvg.goalsAgainst.away] [real] NULL,
	[teams.home.all_last_matches.goalsAvg.goalsAgainst.total] [real] NULL,
	[teams.home.last_h2h.played.home] [int] NULL,
	[teams.home.last_h2h.played.away] [int] NULL,
	[teams.home.last_h2h.played.total] [int] NULL,
	[teams.home.last_h2h.wins.home] [int] NULL,
	[teams.home.last_h2h.wins.away] [int] NULL,
	[teams.home.last_h2h.wins.total] [int] NULL,
	[teams.home.last_h2h.draws.home] [int] NULL,
	[teams.home.last_h2h.draws.away] [int] NULL,
	[teams.home.last_h2h.draws.total] [int] NULL,
	[teams.home.last_h2h.loses.home] [int] NULL,
	[teams.home.last_h2h.loses.away] [int] NULL,
	[teams.home.last_h2h.loses.total] [int] NULL,
	[teams.away.team_id] [int] NULL,
	[teams.away.team_name] [text] NULL,
	[teams.away.last_5_matches.forme] [real] NULL,
	[teams.away.last_5_matches.att] [real] NULL,
	[teams.away.last_5_matches.def] [real] NULL,
	[teams.away.last_5_matches.goals] [int] NULL,
	[teams.away.last_5_matches.goals_avg] [real] NULL,
	[teams.away.last_5_matches.goals_against] [int] NULL,
	[teams.away.last_5_matches.goals_against_avg] [real] NULL,
	[teams.away.all_last_matches.matchs.matchsPlayed.home] [int] NULL,
	[teams.away.all_last_matches.matchs.matchsPlayed.away] [int] NULL,
	[teams.away.all_last_matches.matchs.matchsPlayed.total] [int] NULL,
	[teams.away.all_last_matches.matchs.wins.home] [int] NULL,
	[teams.away.all_last_matches.matchs.wins.away] [int] NULL,
	[teams.away.all_last_matches.matchs.wins.total] [int] NULL,
	[teams.away.all_last_matches.matchs.draws.home] [int] NULL,
	[teams.away.all_last_matches.matchs.draws.away] [int] NULL,
	[teams.away.all_last_matches.matchs.draws.total] [int] NULL,
	[teams.away.all_last_matches.matchs.loses.home] [int] NULL,
	[teams.away.all_last_matches.matchs.loses.away] [int] NULL,
	[teams.away.all_last_matches.matchs.loses.total] [int] NULL,
	[teams.away.all_last_matches.goals.goalsFor.home] [int] NULL,
	[teams.away.all_last_matches.goals.goalsFor.away] [int] NULL,
	[teams.away.all_last_matches.goals.goalsFor.total] [int] NULL,
	[teams.away.all_last_matches.goals.goalsAgainst.home] [int] NULL,
	[teams.away.all_last_matches.goals.goalsAgainst.away] [int] NULL,
	[teams.away.all_last_matches.goals.goalsAgainst.total] [int] NULL,
	[teams.away.all_last_matches.goalsAvg.goalsFor.home] [real] NULL,
	[teams.away.all_last_matches.goalsAvg.goalsFor.away] [real] NULL,
	[teams.away.all_last_matches.goalsAvg.goalsFor.total] [real] NULL,
	[teams.away.all_last_matches.goalsAvg.goalsAgainst.home] [real] NULL,
	[teams.away.all_last_matches.goalsAvg.goalsAgainst.away] [real] NULL,
	[teams.away.all_last_matches.goalsAvg.goalsAgainst.total] [real] NULL,
	[teams.away.last_h2h.played.home] [int] NULL,
	[teams.away.last_h2h.played.away] [int] NULL,
	[teams.away.last_h2h.played.total] [int] NULL,
	[teams.away.last_h2h.wins.home] [int] NULL,
	[teams.away.last_h2h.wins.away] [int] NULL,
	[teams.away.last_h2h.wins.total] [int] NULL,
	[teams.away.last_h2h.draws.home] [int] NULL,
	[teams.away.last_h2h.draws.away] [int] NULL,
	[teams.away.last_h2h.draws.total] [int] NULL,
	[teams.away.last_h2h.loses.home] [int] NULL,
	[teams.away.last_h2h.loses.away] [int] NULL,
	[teams.away.last_h2h.loses.total] [int] NULL,
	[comparison.forme.home] [real] NULL,
	[comparison.forme.away] [real] NULL,
	[comparison.att.home] [real] NULL,
	[comparison.att.away] [real] NULL,
	[comparison.def.home] [real] NULL,
	[comparison.def.away] [real] NULL,
	[comparison.fish_law.home] [real] NULL,
	[comparison.fish_law.away] [real] NULL,
	[comparison.h2h.home] [real] NULL,
	[comparison.h2h.away] [real] NULL,
	[comparison.goals_h2h.home] [real] NULL,
	[comparison.goals_h2h.away] [real] NULL,
 CONSTRAINT [PK_predictions] PRIMARY KEY CLUSTERED 
(
	[fixture_id] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[fixtures] ADD  DEFAULT (getdate()) FOR [insert_date]
GO
