import pandas as pd
import bs4
from twocaptcha import TwoCaptcha
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv


url_login = 'https://www.keysearch.co/user/login'

def check_global_variables():
    """Check if global variables are set"""
    load_dotenv()
    try:
        os.getenv('2CAPTCHA-API-KEY')
    except :
        print("Global variables not set. Please set them in your .env file. See README.md for more information or contact zrx938@alumni.ku.dk.")
        exit()



def setup_driver():
    print("Downloading driver")
    global driver

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def open_login_page():
    """Open Login Page"""
    setup_driver()
    driver.get(url_login)
    time.sleep(2)

def enter_credentials():
    """Enter Credentials"""
    driver.find_element(By.ID,"identity").send_keys(os.getenv('USERNAME'))
    driver.find_element(By.ID,"password").send_keys(os.getenv('PASSWORD'))
    time.sleep(2)


def get_recaptcha_response():
    """Get Response from 2 Captcha"""
    solver = TwoCaptcha(os.getenv('2CAPTCHA-API-KEY'))

    try:
        result = solver.recaptcha(
        sitekey='6LfGZ_wUAAAAAChCP5Krqa-AY2IzjOpexVw-Cx4n',
        url='https://www.keysearch.co/user/login')

    except Exception as e:
        print(e)

    else:
        print(result)
        return result 


def insert_recaptcha_response(response):
    """Insert Recaptcha Response"""
    script_1 = "document.getElementById('g-recaptcha-response').style.display='visible';"
    time.sleep(2)
    script_2 = f'document.getElementById("g-recaptcha-response").innerHTML="{response}";'
    driver.execute_script(script_1)
    driver.execute_script(script_2)
 

def submit_login():
    driver.find_element(By.ID, "submit").submit()
    time.sleep(5)


def click_recaptcha_checkbox():
    """Click Recaptcha Checkbox - this is actually not needed"""
    WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='reCAPTCHA']")))
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()


def enter_keywords():
    """Enter Keywords"""
    keyword = driver.find_element(By.ID,"keyword")
    keyword.clear()
    keyword.send_keys("best pizza in Copenhagen")
    time.sleep(2)
    driver.find_element(By.ID,"search_button").click()
    time.sleep(4)


def get_soup():
    """Get Soup"""
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def get_table(soup):
    """Get Table"""
    table = soup.find_all('table', attrs={'id': 'url-tab-data'})[0]
    return table


def table_to_df(table):
    """Table to Dataframe"""
    df = pd.read_html(str(table))[0]
    return df   


def save_df(df):
    """Save Dataframe"""
    df.to_csv("keysearch_serp.csv")


def login_main():
    check_global_variables()
    open_login_page()
    enter_credentials()
    print("Waiting for 2Captcha response. This can take a while (up to 2 minutes)...")
    response = get_recaptcha_response()
    print("Response received. Inserting response.")
    insert_recaptcha_response(response['code'])
    submit_login()


def research_main():
    print("Entering Keywords")
    enter_keywords()
    print("Getting Data and saving to CSV")
    soup = get_soup()
    table = get_table(soup)
    df = table_to_df(table)
    save_df(df)
    print("Done, check your folder for the csv file")


def main():
    login_main()
    research_main()

main()