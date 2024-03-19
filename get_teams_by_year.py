import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
from shared import abrevs

def get_teams_by_year(year, league_id='NBA'):
    url = f"https://www.basketball-reference.com/leagues/{league_id}_{year}.html"
    print(url)
    page = requests.get(url)
    if str(page) == '<Response [429]>':
        print("Rate Limited Request: triggered rate limiting by cloud service provider (429)")
        return None
    soup = BeautifulSoup(page.content, 'html.parser')
    league = {}
    if int(year) > 1971 and league_id == 'NBA':
        confs = ['E', 'W']
    else:
        confs = []
        
    if len(confs) > 1:
        for letter in confs:
            if letter == 'E':
                curr_conf = 'Eastern'
            else:
                curr_conf = 'Western'
            conf = soup.find('table', id=f'divs_standings_{letter}').find('tbody')
            extract_div = lambda x: x.text.split(" ")[0]
            divisions = conf.find_all('tr', attrs={'class': 'thead'})
            standings = {}
            divisions = conf.find_all('tr', attrs={'class': 'thead'})
            for div in divisions:
                standings[extract_div(div)] = {}
            curr_div = ""
            all_rows = conf.find_all('tr')
            for row in all_rows:
                if row['class'][0] == 'thead':
                    curr_div = extract_div(row)
                    continue  
                team = row.find('th').text
                playoffs = 0
                if team[-1] == '*':
                    team = team[:-1]
                    playoffs = 1
                standings[curr_div][team] = {}
                standings[curr_div][team]['playoffs'] = playoffs
                stats = row.find_all('td')
                for stat in stats:
                    stat_type = stat['data-stat']
                    standings[curr_div][team][stat_type] = stat.text
            league[curr_conf] = standings
    else:
            conf = soup.find('table', id=f'divs_standings_').find('tbody')
            extract_div = lambda x: x.text.split(" ")[0]
            divisions = conf.find_all('tr', attrs={'class': 'thead'})
            standings = {}
            divisions = conf.find_all('tr', attrs={'class': 'thead'})
            for div in divisions:
                standings[extract_div(div)] = {}
            curr_div = ""
            all_rows = conf.find_all('tr')
            for row in all_rows:
                if row['class'][0] == 'thead':
                    curr_div = extract_div(row)
                    continue
                playoffs = 0
                team = row.find('th').text
                if team[-1] == '*':
                    team = team[:-1]
                    playoffs = 1
                standings[curr_div][team] = {}
                standings[curr_div][team]['playoffs'] = playoffs
                stats = row.find_all('td')
                for stat in stats:
                    stat_type = stat['data-stat']
                    standings[curr_div][team][stat_type] = stat.text
            return standings
    return league