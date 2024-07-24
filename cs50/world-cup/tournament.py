# Simulate a sports tournament
import time
from math import sqrt
import csv
import sys
import random

# Number of simluations to run
N = 1000

s_time = time.time()


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # TODO: Read teams into memory from file
    with open(sys.argv[1]) as file:

        n_file = csv.DictReader(file)

        for row in n_file:
            row["rating"] = int(row["rating"])
            teams.append(row)

        counts = {}
        for row in teams:
            counts[row["team"]] = 0

        # TODO: Simulate N tournaments and keep track of win counts
        for i in range(N):
            winner = simulate_tournament(teams)
            counts[winner] += 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    t = [teams]
    teams_squared = sqrt(len(teams))
    teams_squared2 = int(teams_squared)
    for i in range(teams_squared2):
        current_round = simulate_round(t[i])
        t.append(current_round)

    stuff = t[-1]
    stuff2 = stuff[0]
    return stuff2["team"]

if __name__ == "__main__":
    main()

e_time = time.time()
print("total time: ", e_time - s_time)