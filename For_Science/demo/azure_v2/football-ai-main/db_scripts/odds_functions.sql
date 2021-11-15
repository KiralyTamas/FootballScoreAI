-- odds retriever functions


drop function if exists retrieve_formatted_label1_odds
go
CREATE FUNCTION retrieve_formatted_label1_odds ()
RETURNS TABLE AS RETURN   
(
	select * from (
		select [fixture.fixture_id] as fixture_id, odd,  CAST(concat(replace(replace(CONVERT(VARCHAR(MAX), label_name), ' ', '_'), '/', '_'), '.', replace(replace(CONVERT(VARCHAR(MAX), "value"), ' ', '_'), '/', '_'))AS VARCHAR(MAX)) as odd_name
		from odds where label_id in (1)
	) t
	pivot (max(odd) for odd_name in ([Match_Winner.Home], [Match_Winner.Draw], [Match_Winner.Away])) 
	as pivoted
)
go

drop function if exists retrieve_formatted_odds
go
CREATE FUNCTION retrieve_formatted_odds ()
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
go



