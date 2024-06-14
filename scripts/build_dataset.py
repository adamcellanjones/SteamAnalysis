import requests
import json
import time
import pandas as pd
from datetime import datetime
import os

def main():
    date = datetime.today().strftime('%Y%m%d')
    datapath = f"../data/external/all_titles_{date}.csv"
    
    # Collect the full list of titles with owners data from SteamSpy API
    if not os.path.isfile(datapath):
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

            data.to_csv(datapath, mode=mode, header=header)
            time.sleep(1)

    # TODO: Collect release dates from Steam API
    games_list_data = pd.read_csv(datapath).set_index("appid")
    games_list = games_list_data.index
    
    batch = games_list[:100]
    batch_dates = get_game_dates(batch)

    batch_dates.to_csv("../data/external/game_dates.csv", header=True)


    # TODO: Collect tags from SteamSpy API

def get_steamspy_all(page):
    url = f"https://steamspy.com/api.php?request=all&page={page}"
    response = requests.get(url).json()
    return pd.DataFrame(response).T

def get_game_dates(appid_list):
    n_games = len(appid_list)
    dates = []
    
    for i, appid in enumerate(appid_list):     
        print(f"Getting date for game {appid} ({i+1}/{n_games})")
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=uk"
        response = requests.get(url).json()
        date = response[str(appid)]['data']['release_date']['date']
        dates.append(date)

        # Rate limit of 200 calls per 5 minutes = 1 call per 1.5 seconds
        time.sleep(1.5)
    
    return pd.DataFrame(zip(appid_list, dates), columns=["appid", "date"])
main()