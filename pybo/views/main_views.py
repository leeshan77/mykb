from flask import Blueprint, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from pyvirtualdisplay import Display

path='/home/ubuntu/chromedriver'
driver = webdriver.Chrome(path)

bp = Blueprint('main', __name__, url_prefix='/')

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument("--disable-gpu")
#options.add_argument("lang=ko_KR")

options.add_argument('--headless')
options.add_argument('--no-sandbox')

#options.add_argument(
#    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
display = Display(visible=0, size=(1920, 1080))
display.start()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/clock')
def clock():
    return render_template('clock.html')

@bp.route('/stock', methods=['POST'])
def stock():
    data = request.get_json()
    code1 = data['code1']
    code2 = data['code2']
    code3 = data['code3']

    company_codes = []
    company_codes.append(code1)
    company_codes.append(code2)
    company_codes.append(code3)

    prices = selenium_price(company_codes)
    sise = {
        'code1': prices[0], 'code2': prices[1], 'code3': prices[2]
    }
    return jsonify(result2="ok", result3=sise, now=datetime.today())

def selenium_price(company_codes):
    path = '/home/ubuntu/chromedriver'
    driver = webdriver.Chrome(path)
    #driver = webdriver.Chrome('/selenium/chromedriver', chrome_options=options)
    driver.implicitly_wait(10)
    prices = []
    for code in company_codes:
        url = 'https://m.kbsec.com/go.able?linkcd=m04010000&flag=0&JmGb=K&stockcode=' + code
        driver.get(url)
        driver.implicitly_wait(10)

        select = '#container > form > div.stockInfoBox > div:nth-child(1) > div.cellL.stockToday > strong'
        time.sleep(1)
        selected = driver.find_element_by_css_selector(select)

        now_price = selected.text
        prices.append(now_price)
    return prices

