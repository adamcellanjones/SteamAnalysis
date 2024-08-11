import pandas as pd

def load_steam_data():
    all_games = pd.read_csv("../data/external/all_titles_20240617.csv", index_col="appid")
    game_dates = pd.read_csv("../data/external/game_dates.csv", index_col="appid").drop_duplicates()
    game_tags = pd.read_csv("../data/external/game_tags.csv", index_col="appid").drop_duplicates()

    # Clear up unnecessary columns formed from indexes in data pulling
    for df in [all_games, game_dates, game_tags]:
        df.drop(columns="Unnamed: 0", inplace=True)

    # Combine data into single dataset
    games = all_games.merge(game_dates, left_index=True, right_index=True)
    games = games.merge(game_tags, left_index=True, right_index=True)

    # Convert date to datetime data type
    games['date'] = pd.to_datetime(games['date'], errors="coerce")

    # Add a year variable
    games['year'] = games['date'].dt.year

    #Convert owners to ordered category data type
    from pandas.api.types import CategoricalDtype

    labels = games['owners'].unique()
    categories = sorted(labels, key=lambda x: int(x.split(" .. ")[0].replace(",","")))

    cat_type = CategoricalDtype(categories=categories, ordered=True)
    games['owners'] = games['owners'].astype(cat_type)

    return games