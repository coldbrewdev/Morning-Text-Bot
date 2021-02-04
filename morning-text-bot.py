import requests
import urllib.parse
from bs4 import BeautifulSoup
import datetime as dt
import time
import config

"""My Helper Bot"""

headers = {
    'User-Agent': 'Mozilla/5.0'
}


def send_tel_update(message):
    parsetext = urllib.parse.quote_plus(message)
    print(message + '\n')
    if dt.datetime.now(dt.timezone(dt.timedelta(0))).astimezone().tzname() == 'UTC':  # Check whether we're on server
        requests.get(config.telegram_message_URL.format(parsetext))


def send_tel_photo(url):
    requests.get(config.telegram_photo_URL.format(url))


def get_age(bday):
    bd = dt.datetime.strptime(bday, '%m/%d/%Y')
    now = dt.datetime.now()
    age = (now - bd).days
    return age


def get_weather():
    response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=41.881832&lon=-87.623177'
                            '&units=imperial&appid=' + config.weather_api_key)
    x = response.json()
    current_temperature = int(x["current"]["temp"])
    today_high_temp = int(x["daily"][0]["temp"]["max"])
    today_low_temp = int(x["daily"][0]["temp"]["min"])
    today_weather_main = x["daily"][0]["weather"][0]["main"]
    today_weather_description = x["daily"][0]["weather"][0]["description"]
    message = 'Current Temp: ' + str(current_temperature) + '\nHigh Temp: ' + str(today_high_temp) + '\nLow Temp: ' +\
              str(today_low_temp) + '\nThe weather in Chicago calls for ' + str(today_weather_main) + ' today.'
    return message


def get_cnn_top():
    url = 'https://lite.cnn.com/en'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for h in soup.find('li'):
        top = '(Lite) ' + h.text
        return top


def get_bi_top():
    url = 'https://www.businessinsider.com/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for h in soup.findAll('a', {"class": "tout-title-link"}):
        return h.text.lstrip().rstrip()


def get_mw_top():
    url = 'https://www.marketwatch.com/'
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for h in soup.findAll('h3', {"class": "article__headline"}):
        return h.text.lstrip().rstrip()


def get_djif_quote():
    url = 'https://www.marketwatch.com/investing/future/djia%20futures'
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for h in soup.findAll('h3', {"class": "intraday__price"}):
        current = h.text.lstrip().rstrip().replace('\n','')
    for h in soup.findAll('bg-quote', {"class": "intraday__change"}):
        change = h.text.lstrip().rstrip().split('\n')[1]
    return 'DJI Futures ' + current + ' ' + change


def get_spxf_quote():
    url = 'https://www.marketwatch.com/investing/future/sp%20500%20futures'
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for h in soup.findAll('h3', {"class": "intraday__price"}):
        current = h.text.lstrip().rstrip().replace('\n','')
    for h in soup.findAll('bg-quote', {"class": "intraday__change"}):
        change = h.text.lstrip().rstrip().split('\n')[1]
    return 'SPX Futures ' + current + ' ' + change


def get_headlines():
    cnn = get_cnn_top()
    bi = get_bi_top()
    mw = get_mw_top()
    message = 'The headlines today are...' \
              + '\nCNN: ' + cnn  \
              + '\nBI: ' + bi  \
              + '\nMW: ' + mw  \
              + '\n' + get_djif_quote() \
              + '\n' + get_spxf_quote()
    return message


def get_vax_data():
    x = requests.get("https://data.cityofchicago.org/resource/2vhs-cf6b.json").json()
    w = x[3]['date'][5:10]
    y = str(x[3]['total_doses_daily'])
    z = str(round(float(x[3]['_1st_dose_percent_population'])*100,2))
    message = 'Chicago COVID Vaccine Update ('+ w + ')\n' + y + ' doses administered.\n' \
              + z + '% of Chicago has received first dose.'
    return message


def get_covid_data():
    x = requests.get("https://data.cityofchicago.org/resource/e68t-c7fv.json").json()
    date_current = x[0]['date'][5:10]
    date_t1 = x[1]['date'][5:10]
    date_t7 = x[7]['date'][5:10]
    y_current = str(int(float(x[0]['cases_total'])))  # this is average cases for last 7 days
    y_t1 = str(int(float(x[1]['cases_total'])))  # and that number from 1 days ago
    y_t7 = str(int(float(x[7]['cases_total'])))  # and that number from 7 days ago
    z_current = x[0]['deaths_total']  # this is average deaths for last 7 days
    z_t1 = x[1]['deaths_total']  # and that number from 1 days ago
    z_t7 = x[7]['deaths_total']  # and that number from 7 days ago
    message = 'Chicago COVID Update\n' \
              + 'Date  ' + (date_current + '--' + date_t1 + '--' + date_t7).center(20) + '\n' + \
              'Cases ' + (y_current + '---' + y_t1 + '---' + y_t7).center(20) + '\n' + \
              'Deaths' + (z_current + '---' + z_t1 + '---' + z_t7).center(20)
    return message


if __name__=='__main__':
    try:
        message0 = 'Good morning! Today is ' + dt.datetime.utcnow().strftime("%A %B %d, %Y") + \
                   ". You are " + str(get_age(config.a_bday)) + ' days old. ' + config.b + ' is ' \
                   + str(get_age(config.b_bday)) + ' days old.'
        send_tel_update(message0)
        time.sleep(2)
    except:
        send_tel_update('Error sending dates/ages.')
    try:
        message1 = get_weather()
        send_tel_update(message1)
        time.sleep(2)
    except:
        send_tel_update('Error sending weather.')
    try:
        message2 = get_headlines()
        send_tel_update(message2)
        time.sleep(2)
    except:
        send_tel_update('Error sending headlines.')
    try:
        message3 = get_covid_data() + '\n\n' + get_vax_data()
        send_tel_update(message3)
        time.sleep(2)
    except:
        send_tel_update('Error sending COVID data.')
