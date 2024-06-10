import requests
import json
import time
import pandas as pd

def main():
    # TODO: Collect the full list of titles from SteamSpy API
    for i in range(2):
        print(f"Getting page {i}")
        data = pull_steamspy_all(page=i)
        
        if i == 0:
            mode = "w"
            header = True
        else:
            mode = "a'"
            header = False
            
        data.to_csv("../data/external/all_titles.csv", mode=mode, header=header)
        time.sleep(61)

    # TODO: Collect release date from Steam API

    # TODO: Collect tags from SteamSpy API

def pull_steamspy_all(page):
    url = f"https://steamspy.com/api.php?request=all&page={page}"
    response = requests.get(url).json()
    return pd.DataFrame(response).T

main()