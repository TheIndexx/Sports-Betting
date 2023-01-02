from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

"""
Team		Score		Book
----------------------------
Knicks		-450		1
Jazz		+210		1
Knicks		-340		2
Jazz		+200		2
"""

def bovada_scrape():
	options = Options()
	options.headless = False
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('window-size=1920x1080') #Headless = True
	web = 'https://www.bovada.lv/sports/basketball'
	ser = Service('C:\Rishi\chromedriver') #introduce the path of your chromedriver file

	driver = webdriver.Chrome(service=ser, options=options)
	driver.get(web)
	
	try:
		all_live = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'happening-now-bucket')))
		event_teams = all_live.find_elements(By.CLASS_NAME, 'event-title')
	except NoSuchElementException or TimeoutException:
		driver.quit()
		return False

	teams = []
	game_index = []
	moneyline = []

	n = 0

	"""
	all_live = all live events
	event_teams = list of events (only containing names of teams playing)
	team_group = a group of 2 teams in an event
	event = an event with the teams AND odds
	"""
	try:
		for team_group in event_teams:
			event = team_group.find_element(By.XPATH, '..')
			if len(event.find_elements(By.CLASS_NAME, 'market-type')) > 0:
				## TEAM NAMES
				for team_name in team_group.find_elements(By.CLASS_NAME, 'name'):
					teams.append(team_name.text)
				game_index += 2 * [n]
				n += 1

				#grouped_events = event.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
				#league_name = grouped_events.find_element(By.CLASS_NAME, 'league-header-collapsible__description')
				#league += 2 * [league_name.text]

				## MONEYLINE ODDS
				market_types = event.find_elements(By.CLASS_NAME, 'market-type')
				for betprice in market_types[1].find_elements(By.CLASS_NAME, 'bet-price'):
					moneyline.append(betprice.text)
	except StaleElementReferenceException:
		driver.quit()
		return False

	driver.quit()

	data = {
		"bov_index": game_index,
		"bov_teams": teams,
		"bov_odds": moneyline
	}
	df = pd.DataFrame(data)
	return df

def bov_main():
	data = False
	i = 0
	while isinstance(data, bool):
		print('bov failed {} times'.format(str(i)))
		i += 1
		data = bovada_scrape()

		if i == 5:
			print('bov broken')
			break
	return data

if __name__ == "__main__":
	print(bov_main())