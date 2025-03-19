# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U","value":"00D15DFC059793AAA92A55BEF3AC58EA5D9BE378EF278DEA00FF0BAEF8DDCCA458E4AF137BA4BDD554250734EFAC4237CB6FD8BF48C00E4F42AEF7FE6C0E31840E926834DE2B1AEE6DA3993624CF1B40B24AE20DE39DEA6380226AD7BBE2F6202977D620AD87EB73B7E3BC2F0471B5AE84E67CCFBEE4CD0096E772FB29EFEE87D36CD1C15EE496558251C67A9F2DA17420E711B1CABA12E64DB70AB4A2573C8EDBB743D58AB166AD43787F91979C7B017729450B11522EE77B9B29FC37696EDB74A22E5EAF0447E9A626CA75788E9DE83007DED42E451CC019C64BB7F1E2D76F18A72BF1E93875D4B80D81D2B21FED383546C60B500590EDE677D13DF08544EF07B9E95100D9EED7540A25A4453DDCF3B0E98815E1E7FF2C003CAA3AA72F831F7840DD4D41FAAA605938502C227CB3ED6B79E65231FA7D97D778D78146328E01DBE285033DCEE161D6D403932B66A6F854"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
