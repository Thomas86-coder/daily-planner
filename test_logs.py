from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# enable console logging
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
driver.get("file:///Users/jaehyun/인생관리시스템/index.html")

time.sleep(1) # wait for load

# click nav-completed
driver.find_element(By.ID, "nav-completed").click()

time.sleep(1) # wait for search to complete (ch_searchCompleted runs inside navigate)

# select "이번 주" (week)
select = driver.find_element(By.ID, "ch-filter-period")
for option in select.find_elements(By.TAG_NAME, "option"):
    if option.get_attribute("value") == "week":
        option.click()
        break

# click search button
driver.find_element(By.XPATH, "//button[contains(text(), '🔍 검색')]").click()

time.sleep(2) # wait for query

logs = driver.get_log('browser')
for log in logs:
    if "===" in log['message'] or "필터:" in log['message'] or "날짜 범위:" in log['message'] or "결과:" in log['message'] or "컨테이너 찾음?" in log['message']:
        print(log['message'])

driver.quit()
