
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Set, Tuple


# url of the website
URL = 'https://www.sofascore.com/tournament/football/world/world-cup/16#41087'


def get_player_attributes(driver):
    attributes = {}
    attack = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd attacking"]')
    attack_value = attack.find_element(By.XPATH, '//*[@class="sc-eDWCr dbpNPs"]')
    attributes['attack'] = attack_value.text
    technical = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd technical"]')
    technical_value = technical.find_element(By.XPATH, '//*[@class="sc-eDWCr dbpNPs"]')
    attributes['technical'] = technical_value.text
    defending = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd defending"]')
    defending_value = defending.find_element(By.XPATH, '//*[@class="sc-eDWCr dbpNPs"]')
    attributes['defending'] = defending_value.text
    tactical = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd tactical"]')
    tactical_value = tactical.find_element(By.XPATH, '//*[@class="sc-eDWCr dbpNPs"]')
    attributes['tactical'] = tactical_value.text
    creativity = driver.find_element(By.XPATH, '//*[@class="sc-hLBbgP sc-eDvSVe kRaGsb eRXHvd creativity"]')
    creativity_value = creativity.find_element(By.XPATH, '//*[@class="sc-eDWCr dbpNPs"]')
    attributes['creativity'] = creativity_value.text
    return attributes


def main():
    driver = webdriver.Firefox()
    driver.get(URL)
    
    # Dictionary with teams as keys, values are other dictionaries with players as keys and attributes as values
    results = {}

    links = driver.find_elements(By.XPATH, '//a[@href]')
    football_teams_links: Set[Tuple[str, str]] = set()
    print('links', links)
    for elem in links:
        href = elem.get_attribute("href").split('/')
        if href[3] == 'team' and href[4] == 'football':
            football_teams_links.add((href[5], elem.get_attribute("href")))
    print('football_teams_links', football_teams_links)
    print('len', len(football_teams_links))

    players_links = set()
    for team_link in football_teams_links:
        driver.get(team_link[1])
        links = driver.find_elements(By.XPATH, '//a[@href]')
        for elem in links:
            href = elem.get_attribute("href").split('/')
            if href[3] == 'player':
                players_links.add(elem.get_attribute("href"))
                driver.get(elem.get_attribute("href"))
                player_name = href[4]
                attributes = get_player_attributes(driver)
                temp = {}
                temp[player_name] = attributes
                results[team_link[0]] = temp
                break
        break
    
    print('results')
    print(results)
    

if __name__ == "__main__":
    main()