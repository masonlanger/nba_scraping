import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
from shared import abrevs

def get_player_stats_team(team, year, mode, league='NBA'):
    season = str(year[-4:])
    abr = abrevs[team][league] if type(abrevs[team]) == dict else abrevs[team]
    url = 'https://www.basketball-reference.com/teams/' + abr + '/' + str(season) + '.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    totals = soup.find('table', id=str(mode))
    roster = {}
    for td in totals.findAll('td'):
        if td["data-stat"] == 'player' and td.getText() == '':
            break
        elif td["data-stat"] == 'player':
            curr_player = td.getText()
            roster[td.getText()] = {}
        elif td.getText() != '':
            roster[curr_player][td['data-stat']] = td.getText()
    keys = list(roster.get(list(roster)[0]).keys())
    df = pd.DataFrame(columns=keys)
    df = df.from_dict(roster, orient='index', dtype='float')
    return df
