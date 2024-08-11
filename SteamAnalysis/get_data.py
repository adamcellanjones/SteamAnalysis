import requests
import json
import time
import pandas as pd
from datetime import datetime
import os
import math

def main():
    date = datetime.today().strftime('%Y%m%d')
    list_datapath = f"../data/external/all_titles_{date}.csv"
    dates_datapath = "../data/external/game_dates.csv"
    tags_datapath = "../data/external/game_tags.csv"
    
    # Collect the full list of titles with owners data from SteamSpy API
    if not os.path.isfile(list_datapath):
        for i in range(74):
            print(f"Getting page {i}")
            data = get_steamspy_all(page=i)
            
            # Start new file with header row for first page, append data without header afterwards
            if i == 0:
                mode = "w"
                header = True
            else:
                mode = "a"
                header = False

            data.to_csv(list_datapath, mode=mode, header=header)
            time.sleep(1)

    # Collect release dates from Steam API and genres and tags from SteamSpy API
    games_list = pd.read_csv(list_datapath).set_index("appid").index

    # Check if we already have some data - if yes, exclude games from list and append data, if not start new file
    if os.path.isfile(dates_datapath):
        games_with_dates = pd.read_csv(dates_datapath).set_index("appid").index
        dates_mode = "a"
        dates_header = False
    else:
        games_with_dates = []
        dates_mode = "w"
        dates_header = True
    if os.path.isfile(tags_datapath):
        games_with_tags = pd.read_csv(tags_datapath).set_index("appid").index
        tags_mode = "a"
        tags_header = False
    else:
        games_with_tags = []
        tags_mode = "w"
        tags_header = True

    games_list_to_pull = [id for id in games_list if 
                          id not in set(games_with_dates) or 
                          id not in set(games_with_tags)]

    # Work in batches of 50
    start_point = 0
    batch_size = 50
    batches = math.ceil(len(games_list_to_pull)/batch_size)
    i = 0
    while start_point < len(games_list_to_pull):
        end_point = start_point + batch_size
        batch = games_list_to_pull[start_point:end_point]
        
        batch_dates = get_game_dates(batch)
        batch_dates.to_csv("../data/external/game_dates.csv", header=dates_header, mode = dates_mode)

        batch_tags = get_game_tags(batch)
        batch_tags.to_csv("../data/external/game_tags.csv", header=tags_header, mode = tags_mode)

        start_point = end_point
        i+=1

        print(f"Batch {i}/{batches} complete.")


def get_steamspy_all(page):
    """
    This function calls the SteamSpy API and returns a given page of the "all games" list as a Pandas dataframe
    """
    url = f"https://steamspy.com/api.php?request=all&page={page}"
    response = requests.get(url).json()
    return pd.DataFrame(response).T

def get_game_dates(appid_list):
    """
    This function returns a Pandas dataframe of release dates for a given list of app IDs 
    """
    n_games = len(appid_list)
    dates = []
    
    for i, appid in enumerate(appid_list):     
        print(f"Getting date for game {appid} ({i+1}/{n_games})")
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=uk"
        
        # try 3 times in case of request issues
        for j in range(3):
            try:
                response = requests.get(url).json()
                date = response[str(appid)]['data']['release_date']['date']
                dates.append(date)
                str_error = None
            except Exception as e:
                str_error = str(e)
            
            if str_error:
                time.sleep(2)
                if j == 2: dates.append(None)
            else:
                break

        # Rate limit of 200 calls per 5 minutes = 1 call per 1.5 seconds
        time.sleep(0.9)
    
    return pd.DataFrame(zip(appid_list, dates), columns=["appid", "date"])


def get_game_tags(appid_list, tag_limit=5):
    """
    This function returns a Pandas dataframe of genres and tags for a given list of app IDs.

    Parameters:
    appid_list (list): a list of Steam app IDs
    tag_limit (int): the number of tags to include for each game
    """
    n_games = len(appid_list)
    tags_data = []

    for i, appid in enumerate(appid_list):     
        print(f"Getting genre/tags for game {appid} ({i+1}/{n_games})")
        url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
        
        # try 3 times in case of request issues
        for j in range(3):
            try:
                response = requests.get(url).json()
                
                game_tags = {"appid": appid, "genre": response['genre']}
                for k, tag in enumerate(response['tags']):
                    if k == tag_limit:
                        break
                    game_tags.update({f"tag{k+1}": tag})
                
                tags_data.append(game_tags)
                str_error = None
            except Exception as e:
                str_error = str(e)

            if str_error:
                print("Error raised:", str_error)
                time.sleep(2)
            else:
                break

        # Rate limit of 1 call per second
        time.sleep(0.95)
    
    return pd.DataFrame(tags_data)


main()