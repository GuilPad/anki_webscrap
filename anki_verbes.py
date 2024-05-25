import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

url='https://vvlexicon.ninjal.ac.jp/db/'
# Set up the Chrome WebDriver
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
driver.get(url)
#driver.implicitly_wait(0.5)
select_translation_div = driver.find_element(By.ID, "select_translation")
select_translation_div.click()
select_translation_div = driver.find_element(By.LINK_TEXT, "English")
select_translation_div.click()
driver.implicitly_wait(2)
for i in range(1,3):
    csv_download=driver.find_element(By.ID, "honbun_list")
    csv_download=csv_download.find_element(By.TAG_NAME, "tbody")
    
    for j in range(1,3):
        element_id = str(j)
        tr_element = csv_download.find_element(By.XPATH, value=f"//tr[@id='{element_id}']/descendant::td[@style='border-bottom: dotted 1pt #85B534']")
        list_span=tr_element.find_elements(By.TAG_NAME, "span")
        kanji_verb=list_span[0]
        furigana_verb=list_span[1]
        romanji_verb=list_span[2]
        print(kanji_verb.text)