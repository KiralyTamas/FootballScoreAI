-- pr_diff+winner+league_id

drop function if exists retrieve_fixtures_without_first_n_matches
go

CREATE FUNCTION retrieve_fixtures_without_first_n_matches (@n int)
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

	return
END
go

select * from retrieve_fixtures_without_first_n_matches(5)
go


-- pr_diff+odds+winner

drop function if exists retrieve_fixtures_with_odds_without_first_n_matches
go

CREATE FUNCTION retrieve_fixtures_with_odds_without_first_n_matches (@n int)
RETURNS @result TABLE(
	fixture_id int, event_timestamp int, goalsHomeTeam int, goalsAwayTeam int, [homeTeam.PowerRating] real, [awayTeam.PowerRating] real,
	[Match_Winner.Home] real, [Match_Winner.Draw] real, [Match_Winner.Away] real
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
	select fixtures.fixture_id, fixtures.event_timestamp, fixtures.goalsHomeTeam, fixtures.goalsAwayTeam,
			fixture_pr.[homeTeam.PowerRating], fixture_pr.[awayTeam.PowerRating],
			odds.[Match_Winner.Home], odds.[Match_Winner.Draw], odds.[Match_Winner.Away]
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
	join retrieve_formatted_label1_odds() as odds on odds.fixture_id=fixtures.fixture_id

	return
END
go
