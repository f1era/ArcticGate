import json, time, datetime, os, requests
from bs4 import BeautifulSoup

from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer
from another_modules import data_config 
from utilities_make_web import *

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

def weather():

        oscall('cls', 'clear')
        if data_config('OWM_API') == "no data": owm_check = '1. OpenWeatherMap: API    \033[31mHave no TOKEN. Type "1" for add{cnone}'
        else: owm_check = '1. OpenWeatherMap: API'

        usi = input(f'\n  {cyell}Select resourse:{cnone}\n   {owm_check}\n   2. rp5: web-scraping\n  {cyell}>>>{cnone} ')
        if usi == '1':
            if data_config('OWM_API') == "no data": oscall('start another_config.json', ''); return f'\033[31mYou havent OWM TOKEN. Change OWM_API{cnone}{cyell}'
            usi = input(f'\n  {cyell}Select city:{cnone}\n   1. Tiksi-3\n   Or type city_id (OWM resourse)\n  {cyell}>>>{cnone} ')
            if usi == '1': 
                return get_weather(0, 2015306, 'OpenWeatherMap', int(time.time()))
            else: return get_weather(0, usi, 'OpenWeatherMap', int(time.time()))
        elif usi == '2':
            usi = input(f'\n  {cyell}Select city:{cnone}\n   1. Tiksi-3\n   Or type rp5 url (ex: Погода_в_Москве_(аэропорт))\n  {cyell}>>>{cnone} ')
            if usi == '1': return get_weather(0, 'Погода_в_Тикси_(аэропорт)', 'rp5.ru', int(time.time()))
            else: return get_weather(0, usi, 'rp5.ru', int(time.time()))
        else: return 'Unknown response'

def get_weather(retries, usi, resq, time_log):

    try:

        now_time = datetime.datetime.fromtimestamp(int(time.time())).strftime("%d.%m.%Y %H:%M:%S")
        text_in_html = ""

        oscall('cls', 'clear')
        print(f'\n {cyell}[{resq}]{cnone} Try №{retries} to connecting...')

        if resq == 'rp5.ru':
            url = f'https://rp5.ru/{usi}'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
            full_page = requests.get(url, headers=headers)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            convert = soup.findAll("div", {"class": "ftab_content"})
            text_in_html = str(convert[0])

            # Убираем облачность и осадки
            trq = soup.findAll("tr")
            for q in trq: 
                if str(q).find('Облачность</a>') != -1 or str(q).find('Осадки, мм</a>') != -1: text_in_html = text_in_html.replace(str(q), '') 
            # Убираем onmouseout & onmouseover
            trq = soup.findAll("td")
            for q in trq: 
                onmouseout = q.get('onmouseout')
                onmouseover = q.get('onmouseover')
                if onmouseout != None: text_in_html = text_in_html.replace(onmouseout, '')
                if onmouseover != None: text_in_html = text_in_html.replace(onmouseover, '')
            trq = soup.findAll("div")
            for q in trq: 
                onmouseout = q.get('onmouseout')
                onmouseover = q.get('onmouseover')
                if onmouseout != None: text_in_html = text_in_html.replace(onmouseout, '')
                if onmouseover != None: text_in_html = text_in_html.replace(onmouseover, '')
            text_in_html = text_in_html.replace('onmouseout=""', '')
            text_in_html = text_in_html.replace('onmouseover=""', '')
        
        elif resq == 'OpenWeatherMap':
            appid = data_config('OWM_API')
            if appid == 'no data': return f'\033[31mYou have no OpenWeatherMap API. Change config.json file.{cnone}{cyell}'
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={'id': usi, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            for i in data['list']:
                text_in_html += f"Data: {i['dt_txt']}<br>Temp: {'{0:+3.0f}'.format(i['main']['temp'])}<br>Descr: {i['weather'][0]['description']}<br>Wind: {i['wind']['speed']}<br><br>"

        with open(f'utilities/web_page/css/weather.css', 'r') as bx: stsheet = bx.read()
        text = f"""<style>{stsheet}</style><meta charset = "utf-8">
            <p id='zagSB'>&nbsp;&nbsp;Status bar&nbsp;&nbsp;&nbsp;&nbsp;</p>
                <ul id='SB'>
                    <li style="padding-right: 50px;">
                        <span id ='wthr'>Weather from {resq} at {now_time}</span>
                        {text_in_html}
                    </li>
                <br>
            </ul>"""

        logs_writer(f'{resq} weather is loaded at {int(time.time()) - time_log}s', 'WEATHER_LOAD')
        with open(f'inform/weather/Weather.html', 'w', encoding='utf-8') as e: e.write(text)
        oscall('start inform/weather/Weather.html', '')
        return 'Weather is loaded. Check inform/weather/'

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return get_weather(retries, usi, resq, time_log)
    except Exception as err:
        logs_writer(f'Authors error: {err}', 'WEATHER_LOAD')
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'
