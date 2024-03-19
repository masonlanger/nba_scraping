import requests
from bs4 import BeautifulSoup
import numpy as np
from shared import abrevs

def get_team_roster(team, year, league='NBA'):
    season = str(year[-4:])
    abr = abrevs[team][league] if type(abrevs[team]) == dict else abrevs[team]
    url = 'https://www.basketball-reference.com/teams/' + abr + '/' + str(season) + '.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    players = soup.find('table', id='roster')
    roster = {}
    for td in players.findAll('td'):
        if td["data-stat"] == 'player' and td.getText() == '':
            break
        elif td["data-stat"] == 'player':
            curr_player = td.getText()
            roster[td.getText()] = {}
        elif td.getText() != '':
            roster[curr_player][td['data-stat']] = td.getText()
    return roster
