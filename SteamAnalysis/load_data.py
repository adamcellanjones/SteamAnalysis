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

    # Add columns for upper and lower bounds of owners
    def get_bounds(bin_label):
        tmp = bin_label.split(" .. ")
        lb = int(tmp[0].replace(",",""))
        ub = int(tmp[-1].replace(",",""))
        return [lb, ub]

    games[['owners_lb', 'owners_ub']] = games['owners'].apply(get_bounds).tolist()
    
    #Convert owners to ordered category data type
    from pandas.api.types import CategoricalDtype

    labels = games['owners'].unique()
    categories = sorted(labels, key=lambda x: get_bounds(x)[0])

    cat_type = CategoricalDtype(categories=categories, ordered=True)
    games['owners'] = games['owners'].astype(cat_type)

    return games