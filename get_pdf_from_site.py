import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

base_url = "http://consensus.hankyung.com/apps.analysis/analysis.list"
start_date = "2021-06-01"
end_date = "2021-09-25"


def fetch_pdf_url():
    url = f"http://consensus.hankyung.com/apps.analysis/analysis.list?sdate={start_date}&edate={end_date}&now_page=1&search_value=&report_type=CO&pagenum=10000000&search_text=&business_code="
    driver = webdriver.Chrome(".\\chromedriver.exe")
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.select("div > table > tbody > tr > td > div > a")
    for url in urls:
        if str(url["href"]).strip().startswith("/apps.analysis/analysis.downpdf?report_idx="):
            pdf_url = str(url["href"]).strip()
            title = str(url["title"]).strip()
            download_pdf(pdf_url, title)


def download_pdf(url, title):
    print(url, title)
    Path(".\\reports\\").mkdir(parents=True, exist_ok=True)
    url = f"http://consensus.hankyung.com{url}"
    options = webdriver.ChromeOptions()
    profile = {
        "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
        "download.default_directory": ".\\reports\\",
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "download.extensions_to_open": "applications/pdf"
    }
    options.add_experimental_option("prefs", profile)
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get(url)
    time.sleep(1.5)
    driver.close()
