import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

url = 'https://www2.ninjal.ac.jp/vvlexicon/'
filename = "verbes_composes.csv"

# Set up the WebDriver
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
driver.get(url)
timeout = 5
# Use explicit wait instead of implicit wait for more control
wait = WebDriverWait(driver, 10)

# Click on the English option
select_translation_div = wait.until(EC.element_to_be_clickable((By.ID, "english")))
select_translation_div.click()
close_modal_window = wait.until(EC.element_to_be_clickable((By.ID, "modal-window-close")))
close_modal_window.click()
time.sleep(3)

# Loop through multiple pages
hiragana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよろ"
index_button = driver.find_element(By.ID, "index-buttons")
list_button = index_button.find_elements(By.TAG_NAME, "button")

with open(filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
                        
    # Écrire un en-tête si nécessaire
    writer.writerow(["Verbe", "Prononciation", "Romaji", "Autre Ecriture", "Type", "Composition", "Définition", "Formation", "Exemple Avec Kanji", "Exemple Furigana", "Exemple Romaji"])
    
    for character in hiragana:
        click_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{character}']")))
        click_button.click()
        time.sleep(1)
        total_pages = driver.find_element(By.CLASS_NAME, "total-pages")
        
        for page in range(int(total_pages.text)):
            tr_elements = driver.find_elements(By.XPATH, "//table[@id='results']/tbody/tr")
            
            # Boucle pour chaque <tr> trouvé
            for tr in tr_elements:
                verb_elements = tr.find_elements(By.XPATH, ".//td/table/tbody")
                verb_kanji = verb_elements[0].find_elements(By.XPATH, ".//tr/td/span")
                verb_word = verb_kanji[0].text
                verb_furigana = verb_kanji[1].text
                verb_romaji = verb_kanji[2].text
                
                try:
                    other_pro = verb_elements[0].find_element(By.XPATH, ".//tr[contains(@style,'height:25px')]/td/span[contains(@style, 'font-size:13px') and not(contains(@style, 'font-weight:600'))]")
                    other_writing = other_pro.text
                except NoSuchElementException:
                    other_writing = ""
                
                verb_type = verb_elements[0].find_element(By.XPATH, ".//tr[contains(@style,'height:25px')]/td/span[contains(@style, 'font-size:13px') and contains(@style, 'font-weight:600')]")
                verb_type_abb = verb_type.text
                if verb_type_abb == "VV":
                    verb_type_abb = "Verbe + Verbe"
                elif verb_type_abb == "Vs":
                    verb_type_abb = "Verbe + Verbe Subsidiaire"
                elif verb_type_abb == "pV":
                    verb_type_abb = "Préfixe + Verbe"
                elif verb_type_abb == "V":
                    verb_type_abb = "Mot"
                
                verb_comp = verb_elements[0].find_element(By.CLASS_NAME, 'jita')
                verbe_composition = verb_comp.text
                
                definition_bloc = verb_elements[1].find_elements(By.XPATH, "./tr/td[not(contains(@style, 'font-weight:bold'))]")
                for verb_definition in definition_bloc:
                    try:
                        verb_meaning = verb_definition.find_element(By.XPATH, './/b')
                        verbe_definition = verb_meaning.text
                        formation = verb_definition.find_elements(By.CLASS_NAME, 'kaku')
                        texts = [element.text for element in formation]
                        texts.append(verb_word)
                        verb_examples = verb_definition.find_elements(By.XPATH, './/table')
                        if len(verb_examples) > 1:
                            examples = verb_examples[1].find_elements(By.XPATH, './/span')
                            if len(examples) >= 3:
                                phrase_kanji = examples[0].text
                                phrase_furigana = examples[1].text
                                phrase_romaji = examples[2].text
                                
                                # Préparer la ligne à écrire
                                row = [verb_word, verb_furigana, verb_romaji, other_writing, verb_type_abb, verbe_composition, verbe_definition, " ".join(texts), phrase_kanji, phrase_furigana, phrase_romaji]
                                
                                # Écrire la ligne complète (une seule fois par définition)
                                writer.writerow(row)
                    except (NoSuchElementException, IndexError):
                        pass
            
            if(page!=int(total_pages.text)):    
                time.sleep(2)
                right_button=driver.find_element(By.CLASS_NAME, "fa-circle-chevron-right")
                right_button.click()
                time.sleep(2)
        #print(total_pages.text)