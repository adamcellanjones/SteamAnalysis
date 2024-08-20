import pandas as pd
import sys
import os

sys.path.insert(1, os.path.abspath('..'))

# load Steam game data and export as CSV
from SteamAnalysis.load_data import load_steam_data

games = load_steam_data()

games.to_csv('../data/clean/steam_games.csv', header=True)

# Make a table of tag rank by year and export as CSV
all_tags = pd.concat([games['year'], games.filter(like="tag")], axis=1)
all_tags = all_tags.melt(id_vars='year', ignore_index=False, value_name='tag').drop(columns='variable')

tags_per_year = all_tags.groupby('year').value_counts()
tag_ranks_per_year = tags_per_year.groupby(level='year').rank(ascending=False, method='min')
tag_ranks_per_year.name = 'rank'

tag_ranks_per_year = pd.DataFrame(tag_ranks_per_year).reset_index()
tag_ranks_per_year.to_csv('../data/clean/steam_tag_history.csv', header=True)