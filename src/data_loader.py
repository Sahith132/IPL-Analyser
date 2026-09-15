import pandas as pd

TEAM_NAME_FIXES = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Rising Pune Supergiant': 'Rising Pune Supergiants',
    'Kings XI Punjab': 'Punjab Kings',
    'Pune Warriors': 'Rising Pune Supergiants',
    'Gujarat Lions': 'Gujarat Titans',
}

def load_raw_data(matches_path='../Data/Raw/matches.csv',
                  deliveries_path='../Data/Raw/deliveries.csv'):
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)
    return matches, deliveries

def clean_matches(matches):
    matches['winner'] = matches['winner'].fillna('No Result')
    matches['player_of_match'] = matches['player_of_match'].fillna('N/A')
    matches['city'] = matches['city'].fillna('Unknown')
    matches['method'] = matches['method'].fillna('Normal')
    matches['result_margin'] = matches['result_margin'].fillna(0)
    matches['target_runs'] = matches['target_runs'].fillna(0)
    matches['target_overs'] = matches['target_overs'].fillna(0)

    for col in('team1', 'team2','toss_winner','winner'):
        matches[col] = matches[col].replace(TEAM_NAME_FIXES)

    matches['date'] = pd.to_datetime(matches['date'],errors='coerce')
    return matches

def clean_deliveries(deliveries):

    wickets = deliveries[deliveries['player_dismissed'].notna()]
    print("Total wickets:", len(wickets))

    return deliveries

def save_clean_data(matches,deliveries,matches_out='../Data/Processed/matches_clean.csv',
                     deliveries_out='../Data/Processed/deliveries_clean.csv'):
    matches.to_csv(matches_out, index=False)
    deliveries.to_csv(deliveries_out, index=False)

if __name__ == "__main__":
    matches, deliveries = load_raw_data()
    matches = clean_matches(matches)
    deliveries = clean_deliveries(deliveries)
    save_clean_data(matches, deliveries)
    print("Data cleaned and saved to Data/processed/")
    print(f"Matches shape: {matches.shape}")
    print(f"Deliveries shape: {deliveries.shape}")