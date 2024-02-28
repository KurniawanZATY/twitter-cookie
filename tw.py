import base64
import json
import time
import logging
from selenium import webdriver

def encrypto_cookies(cookies):
    decoded_bytes = base64.b64decode(cookies)
    return decoded_bytes.decode('utf-8')

def auth_to_twitter(driver, cookies):
    log = logging.getLogger(__name__)
    log.info('Started twitter auth')

    driver.get("https://twitter.com")

    decoded_cookies = encrypto_cookies(cookies)
    cookies_dict = json.loads(decoded_cookies)

    for cookie in cookies_dict:
        if 'sameSite' in cookie:
            if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                cookie['sameSite'] = "Lax"
        driver.add_cookie(cookie)

    log.info(driver.current_url)
    driver.refresh()
    time.sleep(5)  # Mengganti time_break dengan 5 detik
    driver.implicitly_wait(10)
    time.sleep(5)  # Mengganti time_break dengan 5 detik
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(5)  # Mengganti time_break dengan 5 detik
    driver.refresh()

    # Periksa apakah login berhasil
    if "twitter.com" in driver.current_url:
        log.success("Login to Twitter | Successfully")
        return True
    else:
        log.success("Login to Twitter | Successfully")
        #log.error("Login to Twitter | Failed")
        return False

# Membuka WebDriver
driver = webdriver.Chrome()

# Membaca data cookie dari file
with open('tw.txt', 'r') as file:
    encoded_cookie = file.read()

# Melakukan otentikasi ke Twitter
if auth_to_twitter(driver, encoded_cookie):
    print('Login berhasil')
else:
    print('Login gagal')

# Menutup WebDriver
driver.quit()
