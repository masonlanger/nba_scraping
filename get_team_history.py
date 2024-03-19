import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
from shared import abrevs

def get_team_history(team):
    team_history = {}
    abr = abrevs[team]
    url = f"https://www.basketball-reference.com/teams/{abr}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = soup.find('table', id=abr).find_all('tr')
    for year in range(1, len(html)):
        stat_objs = []
        stat_objs = html[year].find_all('th') + html[year].find_all('td')
        if len(stat_objs) > 1:
            season = stat_objs[0].text
            team_history[season] = {}
            for i in range(1, len(stat_objs)):
                stat = stat_objs[i]['data-stat']
                if stat == 'DUMMY':
                    continue
                if stat == 'team_name':
                    if '*' in stat_objs[i].text:
                        team_history[season][stat] = stat_objs[i].text[:-1]
                        team_history[season]['playoffs'] = 1 
                        continue
                    else:
                        team_history[season]['playoffs'] = 0 
                team_history[season][stat] = stat_objs[i].text
    return team_history