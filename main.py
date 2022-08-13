import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#driver.get("https://www.imobiliare.ro/")


class Apartment:
    def __init__(self):
        self.driver_ap = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver_ap.get('https://www.imobiliare.ro/')
        self.ap_link = ''
        self.ap_pret = 0

    def get_link(self):
        pass

    def get_price(self):
        pass

    def set_filters(self, pret_max, nr_camere): #0 for oricate
        self.driver_ap.find_element(By.CSS_SELECTOR, '#btn_vezi_filtrele > div.button.btn_collapse').click()
        try:
            pret_drop_down = self.driver_ap.find_element(By.XPATH, '//*[@id="form_filtre"]/div[1]/div[1]/div[1]/div/div/div/div[3]/div/button')
            pret_drop_down.click()
        except selenium.common.exceptions.ElementNotInteractableException:
            time.sleep(3)
            self.driver_ap.find_element(By.CSS_SELECTOR, '#btn_vezi_filtrele > div.button.btn_collapse').click()
            pret_drop_down = self.driver_ap.find_element(By.XPATH,
                                                         '//*[@id="form_filtre"]/div[1]/div[1]/div[1]/div/div/div/div[3]/div/button')
            pret_drop_down.click()

        correct_price = int(pret_max / 50)
        price_selection = self.driver_ap.find_element(By.XPATH, f'//*[@id="bs-select-2-{correct_price-1}"]')
        price_selection.click()

        camere = int(nr_camere + 1)
        camere_selection = self.driver_ap.find_element(By.XPATH, f'// *[ @ id = "form_filtre"] / div[1] / div[1] / div[3] / div / div / label[{camere}]')
        camere_selection.click()

        self.driver_ap.find_element(By.XPATH, '//*[@id="form_filtre"]/div[2]/div[2]/div/a').click()


ap = Apartment()
time.sleep(3)

accept_cookies = ap.driver_ap.find_element(By.XPATH, '//*[@id="modCookies"]/div/div/div/div[2]/div[2]/div[3]/a')
accept_cookies.click()

locatie = ap.driver_ap.find_element(By.XPATH, '//*[@id="b_cautator_locatie_val"]')
locatie.clear()
locatie.send_keys("Bucuresti")
time.sleep(2)

type_select = ap.driver_ap.find_element(By.XPATH, '//*[@id="b_cautator_form"]/div/div[2]/div[1]/div[2]/button')
type_select.click()
type_select = ap.driver_ap.find_element(By.XPATH, '//*[@id="b_cautator_form"]/div/div[2]/div[1]/div[2]/ul/li[1]/ul/li[1]/a')
type_select.click()

in_chirie = ap.driver_ap.find_element(By.XPATH, '//*[@id="b_cautator_form"]/div/div[2]/div[2]/div/button')
in_chirie.click()
in_chirie = ap.driver_ap.find_element(By.XPATH, '//*[@id="b_cautator_form"]/div/div[2]/div[2]/div/div/ul/li[2]/a')
in_chirie.click()

ap.driver_ap.find_element(By.CSS_SELECTOR, '#b_cautator_form > div > div.box-buton-cauta > input').click()

ap.set_filters(300, 3)
time.sleep(4)
link = ap.driver_ap.find_element(By.XPATH, '//*[contains(@id,"anunt")]/div').text
print(link)
ap_list_names = ap.driver_ap.find_elements(By.XPATH, '//*[contains(@id,"anunt")]/div/div[1]/div[2]/div[1]/div[1]/div[2]/h2/span')
ap_list_links = []
ap_list_price = []
ap_list_anunturi = []
main_search_url = ap.driver_ap.current_url
try:
    for aps in ap_list_names:
        print(aps.text)

except selenium.common.exceptions.StaleElementReferenceException:
    ap.driver_ap.find_element(By.XPATH, '//*[@id="buton-exit-modal-imoagent"]').click()
    ap.driver_ap.find_element(By.XPATH, '// *[ @ id = "auth-go-back"]').click()

try:
    ap_list_anunturi = ap.driver_ap.find_elements(By.XPATH, '//*[contains(@id,"anunt")]/div/div[1]/div[2]/div[1]/div[1]')
    for apart in ap_list_anunturi:
        apart.click()
        ap_list_links.append(ap.driver_ap.current_url)
        try:
            ap_list_price.append(ap.driver_ap.find_element(By.XPATH,
                                                           '//*[@id="content-detalii"]/div[1]/div[1]/div[3]/div/div/div/text()'))
            print(ap_list_price)
        except selenium.common.exceptions.NoSuchElementException:
            ap_list_price.append("Pret necomunicat")
            print(ap_list_price)
        time.sleep(3)
        ap.driver_ap.get(main_search_url)
        time.sleep(3)

except selenium.common.exceptions.StaleElementReferenceException:
    ap.driver_ap.find_element(By.XPATH, '//*[@id="buton-exit-modal-imoagent"]').click()
    ap.driver_ap.find_element(By.XPATH, '// *[ @ id = "auth-go-back"]').click()

except selenium.common.exceptions.ElementClickInterceptedException:
    ap.driver_ap.find_element(By.XPATH, '//*[@id="buton-exit-modal-imoagent"]').click()
    ap.driver_ap.find_element(By.XPATH, '// *[ @ id = "auth-go-back"]').click()

