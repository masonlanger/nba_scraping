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


def get_team_img(team, year, league='NBA'):
    season = str(year[-4:])
    abr = abrevs[team][league] if type(abrevs[team]) == dict else abrevs[team]
    url = 'https://www.basketball-reference.com/teams/' + abr + '/' + str(season) + '.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    img = soup.find('img', {'class': 'teamlogo'})
    return img['src']

def get_team_sum_by_year(team, year, league='NBA'):
    season = str(year[-4:])
    abr = abrevs[team][league] if type(abrevs[team]) == dict else abrevs[team]
    url = 'https://www.basketball-reference.com/teams/' + abr + '/' + str(season) + '.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = soup.find('div', {'data-template': "Partials/Teams/Summary"}).find_all('p')
    sum_dict = {}
    currKey = ""
    content = []
    for p in html:
        for child in p.children:
            if str(child).strip() != '':
                if 'strong' in str(child).strip():
                    if str(child.getText()).strip()[-1] == ':':
                        if currKey != "":
                            content_text = " ".join([str(item) for item in content])
                            if ": " in content_text:
                                content_text = content_text[2:]
                            sum_dict[currKey] = content_text
                        currKey = str(child.getText()).strip()[:-1]
                        content.clear()
                    else:
                        if currKey != "":
                            content_text = " ".join([str(item) for item in content])
                            if ": " in content_text:
                                content_text = content_text[2:]
                            sum_dict[currKey] = content_text
                        currKey = str(child.getText()).strip()
                        content.clear()
                else:
                    content.append(str(child.getText()).strip())
    sum_dict["Logo"] = get_team_img(team, year, league)
    return sum_dict
