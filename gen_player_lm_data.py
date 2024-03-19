import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
from shared import abrevs

def gen_player_lm_dataset(year, league_id='NBA'):
    league = get_teams_by_year(year,league_id=league_id)
    if league is None:
        return
    print("Sleeping for 20 seconds...")
    time.sleep(20)
    league_df = pd.DataFrame(columns=['ts_pct', 'trb_pct', 'ast_pct', 'ows', 'dws', 'ws_per_48', 'mp_per_g', 'fg_per_g', 'fga_per_g', 'fg_pct', 'efg_pct', 'ast_per_g', 'pts_per_g'])
    confs = list(league.keys())
    time_ela = 20
    for conf in confs:
        divs = list(league[conf].keys())
        for div in divs:
            teams = list(league[conf][div].keys())
            for team in teams:
                print(team + ": sleeping for 30 seconds...")
                time.sleep(30)
                time_ela += 30
                team_df = get_player_lm_data(team, year, league_id=league_id)
                print(team_df)
                league_df = pd.concat([league_df, team_df])
                print(team + " done, time elapsed: " + str(time_ela/60) + " minutes")
    return league_df