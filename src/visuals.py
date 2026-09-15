import matplotlib.pyplot as plt
import seaborn as sns

COLORS = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
          '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE']


def plot_team_wins(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(data['Team'], data['Wins'], color=COLORS[:len(data)])
    ax.set_title('Most Wins by Team', fontsize=16, fontweight='bold')
    ax.set_ylabel('Wins')
    plt.xticks(rotation=45, ha='right')
    for bar, val in zip(bars, data['Wins']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(val), ha='center', fontweight='bold')
    plt.tight_layout()
    return fig


def plot_top_batsmen(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(data['Batsman'], data['Total Runs'], color=COLORS[:len(data)])
    ax.set_title('Top 10 Run Scorers', fontsize=16, fontweight='bold')
    ax.invert_yaxis()
    plt.tight_layout()
    return fig


def plot_top_wicket_takers(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(data['Bowler'], data['Wickets'], color=COLORS[:len(data)])
    ax.set_title('Top 10 Wicket Takers', fontsize=16, fontweight='bold')
    ax.invert_yaxis()
    plt.tight_layout()
    return fig


def plot_toss_impact(data):
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = [f"{idx} ({val:.1f}%)" for idx, val in data.items()]
    ax.pie(data.values, labels=labels, autopct='%1.1f%%', startangle=90,
           colors=COLORS[:len(data)])
    ax.set_title('Toss Decision Win %', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig


def plot_season_heatmap(matches):
    season_team = matches[matches['winner'] != 'No Result'].groupby(
        ['season', 'winner']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(season_team, cmap='YlOrRd', annot=True, fmt='d', ax=ax, linewidths=0.5)
    ax.set_title('Team Wins Per Season', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def plot_win_percentage(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(data['Team'], data['Win %'], color=COLORS[:len(data)])
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    ax.set_title('Team Win Percentage', fontsize=16, fontweight='bold')
    ax.set_ylabel('Win %')
    plt.xticks(rotation=45, ha='right')
    for bar, val in zip(bars, data['Win %']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f'{val}%', ha='center', fontweight='bold', fontsize=8)
    plt.tight_layout()
    return fig