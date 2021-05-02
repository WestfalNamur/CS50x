# Simulate a sports tournament

import csv
import sys
import random
from typing import List, Dict, TypedDict

# Types
class Team(TypedDict):
    team: str
    rating: str


# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    # Read csv-file
    with open(sys.argv[1], newline="") as csvfile:
        csv_rows = csv.reader(csvfile, delimiter=",", quotechar="|")
        csv_data = [row for row in csv_rows]

    # Read in teams  # 1st row is column name
    teams: List[Team] = [{"team": i[0], "rating": int(i[1])} for i in csv_data[1:]]

    # Simulate N runs
    counts = {}
    for i in range(N):
        winner = simulate_tournament(teams)
        if winner in counts:
            counts[winner] = counts[winner] + 1
        else:
            counts[winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams: List[Team]) -> List[Team]:
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams: List[Team]):
    """Simulate a tournament. Return name of winning team."""

    winners_round_before: List[Team] = teams
    while len(winners_round_before) > 1:
        winners: List[Team] = simulate_round(winners_round_before)
        winners_round_before = winners

    return winners_round_before[0]["team"]


if __name__ == "__main__":
    main()
