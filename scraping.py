from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import uuid

def scrape_sicilia(inizio, fine):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")
    options.binary_location = "/usr/bin/google-chrome"

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(browser, 5)

    def open_url(url):
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    url = f"https://www.regione.sicilia.it/istituzioni/servizi-informativi/decreti-e-direttive?start_date={inizio}&end_date={fine}&f%5B0%5D=group%3A7&f%5B1%5D=group%3A26&subject=&field_decree_number="
    open_url(url)

    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accetto')]")))
        cookie_button.click()
        time.sleep(2)
    except:
        pass

    data_list = []
    pagination_buttons = browser.find_elements(By.XPATH, "//li[contains(@class, 'page-item')]")
    pagination_buttons_len = len(pagination_buttons)
    last_page = int(pagination_buttons[pagination_buttons_len - 2].find_element(By.TAG_NAME, "a").text.strip().split()[-1]) - 1
    counter = 0

    while True:
        soup = BeautifulSoup(browser.page_source, "html.parser")
        table = soup.find('table', {'class': 'cols-7 table-striped table-borderless table table--smaller-font'})
        if table:
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                data = [col.text.strip() for col in cols[:-1]]
                data_list.append(data)

        if counter == last_page:
            break
        counter += 1
        next_url = f"https://www.regione.sicilia.it/istituzioni/servizi-informativi/decreti-e-direttive?start_date={inizio}&end_date={fine}&f%5B0%5D=group%3A7&f%5B1%5D=group%3A26&subject=&field_decree_number=&page={counter}"
        open_url(next_url)
        time.sleep(5)

    browser.quit()
    filename = f"decreti_sicilia_{uuid.uuid4().hex}.csv"
    df = pd.DataFrame(data_list, columns=["N.", "Oggetto", "Data emissione", "Pubblicazione", "Tipologia", "Assessorato/Dipartimento"])
    df.to_csv(filename, index=False)
    return filename
