import requests
import json
import time
import pandas as pd
from datetime import datetime

def main():
    date = datetime.today().strftime('%Y%m%d')
    
    # Collect the full list of titles with owners data from SteamSpy API
    for i in range(74):
        print(f"Getting page {i}")
        data = get_steamspy_all(page=i)
        
        if i == 0:
            mode = "w"
            header = True
        else:
            mode = "a"
            header = False

        data.to_csv("../data/external/all_titles_{date}.csv", mode=mode, header=header)
        time.sleep(1)

    # TODO: Collect release dates from Steam API

    # TODO: Collect tags from SteamSpy API

def get_steamspy_all(page):
    url = f"https://steamspy.com/api.php?request=all&page={page}"
    response = requests.get(url).json()
    return pd.DataFrame(response).T

def get_game_date(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url).json()
    return response[str(appid)]['data']['release_date']['date']

main()