
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from typing import Set, Tuple
from bs4 import BeautifulSoup
import json


# url of the website
URL = 'https://www.sofascore.com/tournament/football/world/world-cup/16#41087'

def get_players_data(driver): 
    players_data = {}
    players_links = set()
    iterations = 0
    
    links = driver.find_elements(By.XPATH, '//a[@href]')
        # players_links[card_name] = set()
    for elem in links:
        href = elem.get_attribute("href").split('/')
            
        if href[3] == 'player':
            player_name = href[4].capitalize()
            players_links.add((player_name, elem.get_attribute('href')))

    # print('players_links', players_links)
    for (c,x) in enumerate(players_links):
        driver.get(x[1])
        attributes = get_player_attributes(driver)
        players_data[x[0]] = attributes
        # print('players_data', players_data)
        # iterations+=1
        print(f"{c}/{len(players_links)}", end='\r')
        driver.back()
        # if iterations == 2:
        #     break
    return players_data

def get_player_attributes(driver):
    attributes = {}
    
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        card_with_data = soup.find('div', {'class': 'sc-hLBbgP sc-eDvSVe gjJmZQ lXUNw'})
        posible_pos = card_with_data.find_all('div', {'class': 'sc-hLBbgP jXHMHH'})
        position = posible_pos[-2].find('div', {'class': 'sc-eDWCr dfLZrf'}).text
        print('pos??', position)
        
        is_goalkepeer = False
        attributes['position'] = position
        print('position', position)
        if position == 'G':
            is_goalkepeer = True
        if is_goalkepeer:
            attributes['aerial'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd aerial"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['anticipation'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd anticipation"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['ballDistribution'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd ballDistribution"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['saves'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd saves"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['tactical'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd tactical"]//*[@class="sc-eDWCr dbpNPs"]').text
            print('goalkeeper', attributes)
            return attributes

        attributes['attack'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd attacking"]//*[@class="sc-eDWCr dbpNPs"]').text
        attributes['technical'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd technical"]//*[@class="sc-eDWCr dbpNPs"]').text
        attributes['defending'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd defending"]//*[@class="sc-eDWCr dbpNPs"]').text
        attributes['tactical'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd tactical"]//*[@class="sc-eDWCr dbpNPs"]').text
        attributes['creativity'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd creativity"]//*[@class="sc-eDWCr dbpNPs"]').text
        return attributes

    except Exception as e:
        print(e)
        return {}
    



def main():
    options = ChromeOptions()
    options.add_argument('--headless --silent --log-level=3')
    driver = Chrome(options=options)
    driver.get(URL)
    print('getting players data\n')
    # Dictionary with teams as keys, values are other dictionaries with players as keys and attributes as values
    results = {}

    links = driver.find_elements(By.XPATH, '//a[@href]')
    football_teams_links: Set[Tuple[str, str]] = set()
    for elem in links:
        href = elem.get_attribute("href").split('/')
        if href[3] == 'team' and href[4] == 'football':
            football_teams_links.add((href[5], elem.get_attribute("href")))

    print(f'found {len(football_teams_links)} football teams')
    print("starting to get players data\n")
    
    for c,team_link in enumerate(football_teams_links):
        print(f"{c}/{len(football_teams_links)}")
        driver.get(team_link[1])
        players_data = get_players_data(driver)
        results[team_link[0]] = players_data
        
    
    out_file = open("data.json", "w")
    print('results')
    print(results)
    json.dump(results, out_file)
    out_file.close()
    

if __name__ == "__main__":
    main()