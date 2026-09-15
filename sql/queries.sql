-- name: Top 10 Run Scorers
SELECT batter, SUM(batsman_runs) as Total_Runs, COUNT(DISTINCT match_id) as Matches
FROM deliveries
GROUP BY batter
ORDER BY Total_Runs DESC
LIMIT 10;

-- name: Top 10 Wicket Takers
SELECT bowler, COUNT(*) as Wickets, COUNT(DISTINCT match_id) as Matches
FROM deliveries
WHERE dismissal_kind NOT IN ('run out','retired hurt','obstructing the field')
  AND dismissal_kind IS NOT NULL
GROUP BY bowler
ORDER BY Wickets DESC
LIMIT 10;

-- name: Most Wins by Team
SELECT winner as Team, COUNT(*) as Wins
FROM matches
WHERE winner != 'No Result'
GROUP BY winner
ORDER BY Wins DESC;

-- name: Toss Impact on Match
SELECT toss_decision,
       COUNT(*) as Total_Matches,
       SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as Won_After_Toss,
       ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as Win_Percentage
FROM matches
WHERE winner != 'No Result'
GROUP BY toss_decision;

-- name: Season Champions
SELECT season as Season, winner as Champion
FROM matches
WHERE match_type = 'Final'
ORDER BY season;

-- name: Top Venues by Matches
SELECT venue as Venue, COUNT(*) as Matches_Played
FROM matches
GROUP BY venue
ORDER BY Matches_Played DESC
LIMIT 10;

-- name: Most Sixes by Batsman
SELECT batter as Batsman, COUNT(*) as Sixes
FROM deliveries
WHERE batsman_runs = 6
GROUP BY batter
ORDER BY Sixes DESC
LIMIT 10;

