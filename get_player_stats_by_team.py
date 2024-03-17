import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np

abrevs = {
          "Atlanta Hawks": 'ATL',
          "Baltimore Bullets": 'BAL',
          "Boston Celtics": 'BOS',
          "Brooklyn Nets": 'BRK',
          "Buffalo Braves": 'BUF',
          "Carolina Cougars": 'CAR',
          "Charlotte Hornets": 'CHO',
          "Charlotte Bobcats": 'CHA',
          "Chicago Bulls": 'CHI',
          "Cleveland Cavaliers": 'CLE',
          "Dallas Chaparrals": 'DLC',
          "Dallas Mavericks": 'DAL',
          "Detroit Pistons": 'DET',
          "Denver Nuggets": {
              'ABA': 'DNR',
              'NBA': 'DEN'
          },
          "Denver Rockets": 'DNR',
          "Golden State Warriors": 'GSW',
          "Houston Rockets": 'HOU',
          "Indiana Pacers": {
              'ABA': 'INA',
              'NBA': 'IND'
          },
          "Kansas City Kings": 'KCK',
          "Kansas City-Omaha Kings": 'KCO',
          "Kentucky Colonels": 'KEN',
          "Los Angeles Lakers": 'LAL',
          "Los Angeles Clippers": 'LAC',
          "Miami Heat": 'MIA',
          "Milwaukee Bucks": 'MIL',
          "Minnesota Timberwolves": 'MIN',
          "Memphis Tams": 'MMT',
          "Memphis Sounds": "MMS",
          "Memphis Grizzlies": 'MEM',
          "New Orleans Jazz": "NOJ",
          "New Orleans Hornets": "NOH",
          "New Orleans Pelicans": "NOP",
          "New Orleans/Oklahoma City Hornets": "NOK",
          "New York Knicks": "NYK",
          "New York Nets": {
              'ABA': 'NYA',
              'NBA': 'NYN'
          },
          "New Jersey Nets": 'NJN',
          "Orlando Magic": 'ORL',
          "Oklahoma City Thunder": 'OKC',
          "Philadelphia 76ers": 'PHI',
          "Phoenix Suns": 'PHO',
          "Portland Trail Blazers": 'POR',
          "Sacramento Kings": 'SAC',
          "San Antonio Spurs": 'SAS',
          "San Diego Conquistadors": 'SDA',
          "Seattle SuperSonics": 'SEA',
          "Toronto Raptors": 'TOR',
          "Utah Jazz": 'UTA',
          "Utah Stars": 'UTS',
          "Vancouver Grizzlies": 'VAN',
          "Virginia Squires": 'VIR',
          "Washington Bullets": 'WSB',
          "Washington Wizards": 'WAS'
}

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
