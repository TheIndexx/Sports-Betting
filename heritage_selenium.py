from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def heritage_scrape():
    options = Options()
    options.headless = False
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('window-size=1920x1080') #Headless = True
    web = 'https://plive.heritagesports.eu/live/?#!/sport/2'
    ser = Service('C:\Rishi\chromedriver') #introduce the path of your chromedriver file

    driver = webdriver.Chrome(service=ser, options=options)
    driver.get(web)
    try:
        panels = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'panel')))
    except TimeoutException:
        driver.quit()
        return False

    teams = []
    moneyline = []
    game_index = []

    n = 0

    for panel in panels:
        try:
            events = panel.find_elements(By.CLASS_NAME, "event-list__item")
            for event in events:
                event_continue = True
                
                ## MONEYLINE
                both_odds = event.find_elements(By.CLASS_NAME, 'col-xs-12')
                
                for odd in both_odds[4:]:
                    if not odd.find_element(By.CLASS_NAME, 'emphasis').text:
                        event_continue = False
                        continue
                    else:
                        moneyline.append(odd.find_element(By.CLASS_NAME, 'emphasis').text)
                if not event_continue:
                    continue
                ## TEAMS
                for team_name in event.find_elements(By.CLASS_NAME, 'event-list__item__details__teams__team'):
                    teams.append(team_name.text)
                ## GAME INDEX
                game_index += 2 * [n]
                n += 1
                ## LEAGUE
                #league += 2 * [panel.find_element(By.CLASS_NAME, "panel-title").text]
        except NoSuchElementException:
            driver.quit()
            return False

    driver.quit()
    
    data = {
		"her_index": game_index,
		"her_teams": teams,
		"her_odds": moneyline
	}
    df = pd.DataFrame(data)
    return df

def her_main():
	data = False
	i = 0
	while isinstance(data, bool):
		print('her failed {} times'.format(str(i)))
		i += 1
		data = heritage_scrape()

		if i == 5:
			print('her broken')
			break
	return data

if __name__ == "__main__":
	print(her_main())