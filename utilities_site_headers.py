import json, time, datetime, os, requests

from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

def utilities_site_headers():

    oscall('cls', 'clear')
    usi = input(f'\n {cyell}Type url >>> {cnone}')
    return load_headers(0, usi, int(time.time()))

def load_headers(retries, url, time_log):

    try:

        oscall('cls', 'clear')
        print(f'\n {cyell}Try №{retries+1}{cnone} to load headers ...')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        response = requests.get(url, headers=headers)
        headers = response.headers
        ready_headers = ''

        oscall('cls', 'clear')
        print(f'\n {cyell}Headers:{cnone}')
        for key, val in headers.items(): ready_headers += f'  {key}: {val}\n' 
        print(ready_headers)
        logs_writer(f'Headers are loaded at {int(time.time()) - time_log}s', 'HABR_NEWS')

        input(f' {cyell}Type any for go back >>> {cnone}')
        return 'Headers are loaded'

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return load_headers(retries, url, time_log)
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'