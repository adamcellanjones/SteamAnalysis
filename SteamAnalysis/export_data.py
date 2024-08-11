import pandas as pd
import sys
import os

sys.path.insert(1, os.path.abspath('..'))
from SteamAnalysis.load_data import load_steam_data

games = load_steam_data()

games.to_csv('../data/clean/steam_games.csv', header=True)