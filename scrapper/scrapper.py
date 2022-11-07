
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Set, Tuple
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
                
                
    print('players_links', players_links)
    for x in players_links:
        driver.get(x[1])
        attributes = get_player_attributes(driver)
        players_data[x[0]] = attributes
        print('players_data', players_data)
        iterations+=1
        driver.back()
        if iterations == 4:
            break
    return players_data

def get_player_attributes(driver):
    attributes = {}
    position = driver.find_element(By.XPATH, '//*[@class="sc-eDWCr dfLZrf"]').text
    is_goalkepeer = False
    if position == 'G':
        is_goalkepeer = True
    try:
        if is_goalkepeer:
            attributes['aerial'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd aerial"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['anticipation'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd anticipation"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['ballDistribution'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd ballDistribution"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['saves'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd saves"]//*[@class="sc-eDWCr dbpNPs"]').text
            attributes['tactical'] = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd tactical"]//*[@class="sc-eDWCr dbpNPs"]').text
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
    driver = webdriver.Firefox()
    driver.get(URL)
    
    # Dictionary with teams as keys, values are other dictionaries with players as keys and attributes as values
    results = {}

    links = driver.find_elements(By.XPATH, '//a[@href]')
    football_teams_links: Set[Tuple[str, str]] = set()
    for elem in links:
        href = elem.get_attribute("href").split('/')
        if href[3] == 'team' and href[4] == 'football':
            football_teams_links.add((href[5], elem.get_attribute("href")))


    for team_link in football_teams_links:
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