import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import argparse


parser = argparse.ArgumentParser(description="wifiResetter")
parser.add_argument("-w", "--window", help="Window mode. Show browser window.", action="store_true")
args = parser.parse_args ()

options = Options()
options.page_load_strategy = 'eager'
if args.window == True:
    options.headless = False
else:
	options.headless = True
os.environ['WDM_LOG'] = "false"
import logging
logging.getLogger('WDM').setLevel(logging.NOTSET)


###########################################################
### 			SETTINGS			###
###########################################################
url = "https://192.168.1.1"
login = ""
passw = ""


###########################################################

# Login Elements by CSS Selector
loginCSS = "#username"
passwCSS = "#password"
btnCSS = "#loginbtn"

# A list with Clicks that will be done.
clickCSS = [
	".coc-hidecourse-8060 div:nth-child(1) div:nth-child(1) div:nth-child(1) h3:nth-child(2) a",
]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

try:
	driver.set_page_load_timeout(30)
	driver.get(url)
	driver.implicitly_wait(1)
except WebDriverException:
	print("WebDriverException. Couldnt get "+url)
except TimeoutException:
	print("Webdriver: Timeout. Try again later.")
time.sleep(1)

try:
	wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, loginCSS)))
	loginEl = driver.find_element(by=By.CSS_SELECTOR, value=loginCSS)
	passwEl = driver.find_element(by=By.CSS_SELECTOR, value=passwCSS)
	btnEl = driver.find_element(by=By.CSS_SELECTOR, value=btnCSS)
except Exception as e:
	print("No such element.", e)
	raise(e)

try:
	loginEl.send_keys(login)
	passwEl.send_keys(passw)
	btnEl.click()
except Exception as e:
	print("Couldnt login.")
	raise(e)

time.sleep(1)

## Now we are logged in. Click Buttons now.]
for btn in clickCSS:
	try:
		wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, btn)))
		bEL = driver.find_element(by=By.CSS_SELECTOR, value=btn)
		bEL.click()
		print("Clicked element: ", btn)
	except Exception as e:
		print("Could not click element: ", btn, "\n", e)
		continue

print("Exiting script.")
time.sleep(10)