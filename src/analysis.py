import pandas as pd

WICKET_EXCLUDE = ['run out', 'retired hurt', 'obstructing the field']

def get_team_wins(matches):
    wins = matches[matches['winner'] != 'No Result']['winner'].value_counts().reset_index()
    wins.columns = ['Team','Wins']
    return wins

def get_team_win_percentage(matches):
    teams_played = pd.concat([matches['team1'], matches['team2']]).value_counts()
    wins = matches[matches['winner'] != 'No Result']['winner'].value_counts()
    win_pct = (wins / teams_played * 100).round(2).reset_index()
    win_pct.columns = ['Team', 'Win %']
    return win_pct.dropna().sort_values('Win %', ascending=False)

def get_toss_impact(matches):
    m = matches[matches['winner'] != 'No Result'].copy()
    m['toss_match_win'] = m['toss_winner'] == m['winner']
    return(m.groupby('toss_decision')['toss_match_win'].mean() * 100).round(2)

def get_top_venues(matches,n=10):
    venues = matches['venue'].value_counts().head(n).reset_index()
    venues.columns = ['Venue','matches_count']
    return venues

def get_season_winners(matches):
    finals = matches[matches['match_type'] == 'Final'][['season','winner']].copy()
    finals.columns = ['Season','Champions']
    return finals.sort_values('Season')

def get_top_batsmen(deliveries, n=10):
    runs = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(n).reset_index()
    runs.columns = ['Batsman', 'Total Runs']
    return runs

def get_batsman_stats(deliveries,batsman_name):
    bat = deliveries[deliveries['batter'] == batsman_name]
    balls_faced = len(bat)
    return{
        'Total Runs': int(bat['batsman_runs'].sum()),
        'Balls Faced':balls_faced,
        'Fours':int(len(bat[bat['batsman_runs'] == 4])),
        'Sixes':int(len(bat[bat['batsman_runs'] == 6])),
        'Strike Rate':round(bat['batsman_runs'].sum() / balls_faced * 100,2) if balls_faced else 0,
        'Matches':int(bat['match_id'].nunique()),
    }

def get_top_six_hitters(deliveries,n=10):
    sixes = deliveries[deliveries['batsman_runs'] == 6].groupby('batter').size().sort_values(ascending = False).head(n).reset_index()
    sixes.columns = ['Batsman','Sixes']
    return sixes

#bowler analysis

def get_top_wicket_takers(deliveries,n=10):
    wickets_df = deliveries[deliveries['dismissal_kind'].notna() & (~deliveries['dismissal_kind'].isin(WICKET_EXCLUDE))
    ]
    wickets = wickets_df.groupby('bowler').size().sort_values(ascending = False).head(n).reset_index()
    wickets.columns = ['Bowler','Wickets']
    return wickets

def get_bowler_stats(deliveries,bowler_name):
    bowl = deliveries[deliveries['bowler'] == bowler_name]
    wickets = bowl[
        bowl['dismissal_kind'].notna() &
        (~bowl['dismissal_kind'].isin(WICKET_EXCLUDE))
    ].shape[0]
    balls = len(bowl)
    return {
        'Wickets': int(wickets),
        'Runs Given': int(bowl['total_runs'].sum()),
        'Balls Bowled': balls,
        'Economy': round(bowl['total_runs'].sum() / balls * 6, 2) if balls else 0,
        'Matches': int(bowl['match_id'].nunique()),
    }

def get_top_economical_bowlers(deliveries, n=10, min_balls=120):
    stats = deliveries.groupby('bowler').agg(
        runs=('total_runs', 'sum'),
        balls=('total_runs', 'count')
    ).reset_index()
    stats['economy'] = (stats['runs'] / stats['balls'] * 6).round(2)
    return stats[stats['balls'] >= min_balls].sort_values('economy').head(n)

if __name__ == '__main__':
    import sys;sys.path.append('src')
    import pandas as pd
    deliveries = pd.read_csv('../data/processed/deliveries_clean.csv')
    print(get_bowler_stats(deliveries,'P Kumar'))