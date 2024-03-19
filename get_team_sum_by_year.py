import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
from shared import abrevs

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
