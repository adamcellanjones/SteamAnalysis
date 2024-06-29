# Introduction

This WIP project uses data from Steam, the PC gaming marketplace, to analyse trends in gaming. I'm interested in how different types of games have become more or less popular over time, and whether the 'hits' of one year result in imitators in subsequent years.

# Data sources and code structure

Data was collected from the Steam Store API and the SteamSpy API in June 2024. The 'API exploration' notebook has references and shows how data is collected. The 'get_data.py' script is used to request and compile data on all games on Steam, a process which takes a few days because of rate limits, but can be run in batches.

The 'data exploration' notebook includes initial exploratory/descriptive analysis on the combined dataset.
