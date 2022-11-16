
import json
from urllib.request import Request, urlopen
from typing import List, Dict
from bs4 import BeautifulSoup
from unidecode import unidecode
import re


URL = 'https://www.goal.com/es-mx/noticias/fantasy-mundial-qatar-2022-como-sera-la-alineacion-titular-de-todas-las-selecciones/bltf2654ae9e7f65872'


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) "
    "Gecko/20100101 Firefox/40.1"
}


def get_page(url):
    page = Request(url=url, headers=HEADERS)
    html = urlopen(page)
    bs = BeautifulSoup(html.read(), "html.parser")
    return bs

def get_lineups_data(bs):
    texts = bs.find_all('p')
    useful_texts = []
    for text in texts:
        if '(' in str(text): 
            # print('text', text)
            country_lineup, team = text.text.split(':')
            
            useful_texts.append((country_lineup, team))
    
    result = {}
    for text in useful_texts:
        # print(text[0].split())
        country, lineup = text[0].split('(')
        country = unidecode(country)
        # lineup = lineup[1:]
        lineup = lineup[0:len(lineup)-1]
        numbers = lineup.split('-')
        players = re.split(', |;', text[1]) 
        temp = players[-1]
        players = players[0 : len(players)-1]
        new_last_players = []
        for i in range(len(temp)):
            if temp[i] == 'y' and temp[i+1] == ' ' and temp[i-1] == ' ':
                new_last_players.append(temp[0:i-1])
                new_last_players.append(temp[i+2:])
                break
        print(new_last_players, 'new')
        players = players + new_last_players
        players = [unidecode(x) for x in players]
        # print('first', players)
        last_player = players[-1]
        players[-1] = last_player[0:len(last_player)-1]
        # print('mmm', players)
        team_lineup = assign_lineups_to_team(numbers, players )
        # print('doble mmm', team_lineup)
        result[country] = team_lineup

    return result
def assign_lineups_to_team(lineup:List[int], players: List[str]):
    goalkeeper = players[0]
    players = players[1:]
    defense = players[0:int(lineup[0])]
    players = players[len(defense):]
    mid = players[0:int(lineup[1])]
    players = players[len(mid):]
    att = players[0:int(lineup[2])]
    # print(len(defense), lineup[0])
    # print(len(mid), lineup[1])
    # print(len(att), lineup[2])

    return {
        'goalkeeper': goalkeeper,
        'def': defense,
        'mid': mid,
        'att': att
    }

def main():
    bs = get_page(URL)
    results = get_lineups_data(bs)
    out_file = open("lineups_preprocess.json", "w")
    print('results')
    print(results)
    json.dump(results, out_file)
    out_file.close()


if __name__ == '__main__':
    main()