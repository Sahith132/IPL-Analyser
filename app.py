import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import load_raw_data, clean_matches, clean_deliveries
from analysis import (
    get_team_wins, get_team_win_percentage, get_toss_impact,
    get_top_batsmen, get_batsman_stats, get_top_six_hitters,
    get_top_wicket_takers, get_bowler_stats, get_top_economical_bowlers,
    get_top_venues, get_season_winners,
)
from visuals import (
    plot_team_wins, plot_top_batsmen, plot_top_wicket_takers,
    plot_toss_impact, plot_season_heatmap, plot_win_percentage,
)
from db_utils import create_database, run_query, load_queries

st.set_page_config(page_title="IPL Analyzer", layout="wide")


@st.cache_data
def load_data():
    matches, deliveries = load_raw_data('Data/Raw/matches.csv', 'Data/Raw/deliveries.csv')
    matches = clean_matches(matches)
    deliveries = clean_deliveries(deliveries)
    return matches, deliveries


matches, deliveries = load_data()
create_database(matches, deliveries)
queries = load_queries('sql/queries.sql')


st.sidebar.title("IPL Analyzer")
st.sidebar.divider()

PAGES = {
    "Overview": "Overview",
    "Team Analysis": "Team Analysis",
    "Batsman Analysis": "Batsman Analysis",
    "Bowler Analysis": "Bowler Analysis",
    "Season Analysis": "Season Analysis",
    "SQL Explorer": "SQL Explorer",
}

selected_label = st.sidebar.radio("Navigate", list(PAGES.keys()))
page = PAGES[selected_label]

st.sidebar.divider()
st.sidebar.caption(f"{matches.shape[0]} matches · {matches['season'].nunique()} seasons")

if page == "Overview":
    st.title("IPL Data Analyzer")
    st.subheader("2008 – 2024 · Complete Statistical Analysis")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", matches.shape[0])
    col2.metric("Seasons", matches['season'].nunique())
    col3.metric("Teams", matches['team1'].nunique())
    col4.metric("Venues", matches['venue'].nunique())

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Most Wins by Team")
        st.pyplot(plot_team_wins(get_team_wins(matches).head(10)))
    with col2:
        st.subheader("Toss Decision Win %")
        st.pyplot(plot_toss_impact(get_toss_impact(matches)))

    st.divider()
    st.subheader("Team Wins Per Season")
    st.pyplot(plot_season_heatmap(matches))

elif page == "Team Analysis":
    st.title("Team Analysis")
    st.divider()

    all_teams = sorted(matches['team1'].unique())
    selected_team = st.selectbox("Select Team", all_teams)

    team_matches = matches[(matches['team1'] == selected_team) | (matches['team2'] == selected_team)]
    team_wins = matches[matches['winner'] == selected_team].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Matches", len(team_matches))
    col2.metric("Total Wins", team_wins)
    win_pct = round(team_wins / len(team_matches) * 100, 2) if len(team_matches) else 0
    col3.metric("Win %", f"{win_pct}%")

    st.divider()
    st.subheader("Win % Across All Teams")
    st.pyplot(plot_win_percentage(get_team_win_percentage(matches).head(10)))

    st.subheader("Top Venues")
    st.dataframe(get_top_venues(matches), use_container_width=True)


elif page == "Batsman Analysis":
    st.title("Batsman Analysis")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Run Scorers")
        st.pyplot(plot_top_batsmen(get_top_batsmen(deliveries)))
    with col2:
        st.subheader("Top Six Hitters")
        st.dataframe(get_top_six_hitters(deliveries), use_container_width=True)

    st.divider()
    st.subheader("Search Batsman Stats")
    all_batsmen = sorted(deliveries['batter'].unique())
    selected = st.selectbox("Select Batsman", all_batsmen)
    if selected:
        stats = get_batsman_stats(deliveries, selected)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Runs", stats['Total Runs'])
        col1.metric("Matches", stats['Matches'])
        col2.metric("Balls Faced", stats['Balls Faced'])
        col2.metric("Strike Rate", stats['Strike Rate'])
        col3.metric("Fours", stats['Fours'])
        col3.metric("Sixes", stats['Sixes'])

elif page == "Bowler Analysis":
    st.title("Bowler Analysis")
    st.divider()

    st.subheader("Top 10 Wicket Takers")
    st.pyplot(plot_top_wicket_takers(get_top_wicket_takers(deliveries)))

    st.subheader("Most Economical Bowlers (min. 120 balls)")
    st.dataframe(get_top_economical_bowlers(deliveries), use_container_width=True)

    st.divider()
    st.subheader("Search Bowler Stats")
    all_bowlers = sorted(deliveries['bowler'].unique())
    selected = st.selectbox("Select Bowler", all_bowlers)
    if selected:
        stats = get_bowler_stats(deliveries, selected)
        col1, col2, col3 = st.columns(3)
        col1.metric("Wickets", stats['Wickets'])
        col1.metric("Matches", stats['Matches'])
        col2.metric("Runs Given", stats['Runs Given'])
        col2.metric("Balls Bowled", stats['Balls Bowled'])
        col3.metric("Economy", stats['Economy'])


elif page == "Season Analysis":
    st.title("Season Analysis")
    st.divider()

    st.subheader("IPL Champions by Season")
    st.dataframe(get_season_winners(matches), use_container_width=True)

    st.divider()
    selected_season = st.selectbox("Select Season", sorted(matches['season'].unique(), reverse=True))
    season_data = matches[matches['season'] == selected_season]

    col1, col2 = st.columns(2)
    col1.metric("Matches Played", len(season_data))
    col2.metric("Venues Used", season_data['venue'].nunique())


elif page == "SQL Explorer":
    st.title("🗄️ SQL Explorer")
    st.divider()

    st.subheader("Predefined Queries")
    selected_query = st.selectbox("Choose a Query", list(queries.keys()))
    if st.button("Run Query"):
        st.dataframe(run_query(queries[selected_query]), use_container_width=True)

    st.divider()
    st.subheader("Write Your Own SQL")
    st.code("SELECT winner, COUNT(*) as wins FROM matches GROUP BY winner ORDER BY wins DESC LIMIT 5")

    custom_query = st.text_area("Enter SQL Query", height=150)
    if st.button("Execute"):
        try:
            result = run_query(custom_query)
            st.success(f"Query returned {len(result)} rows")
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")