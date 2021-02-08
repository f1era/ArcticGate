import json, time, datetime, os, requests
from bs4 import BeautifulSoup

from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer
from another_modules import edit_url_pages
from utilities_make_web import *

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

def downloader_pages():

    oscall('cls', 'clear')
    print(f'\n {cyell}What we will do?{cnone}')
    print(f'    0. Go back')
    print(f'    1. Download all pages into downloader/urls.txt')
    print(f'    Or type google response/url')
    usi = input(f" {cyell}>>>{cnone} ")

    if usi == "0": return "Go back"
    elif usi == "1": return open_file_page()
    else: 
        if usi.startswith('https://') or usi.startswith('http://'): 
            with open(f'downloader/urls.txt', 'a', encoding='utf-8') as e: e.write(f'\n{usi}')
            return preload_page()
        else: 
            with open(f'downloader/urls.txt', 'a', encoding='utf-8') as e: e.write(f'\nsearch: {usi}')
            return preload_page()

def open_file_page():

    oscall('cls', 'clear')
    oscall('start downloader/urls.txt', '')
    print(f'\n {cyell}What we will do?{cnone}')
    print(f'    0. Go back')
    print(f'    1. Start loading')
    print(f'    2. Change urls.txt again')
    usi = input(f" {cyell}>>>{cnone} ")

    if usi == "1": return preload_page()
    elif usi == "2": return open_file_page()
    else: return "Go back"    

def preload_page():
    
    f = open("downloader/urls.txt", encoding='utf-8')
    file_pages = f.readlines()
    urls = [[],[]]
    for q in range(len(file_pages)):
        fdir = os.listdir(path="downloader/pages/")
        if file_pages[q] != '' and \
        file_pages[q].startswith('#') == False and \
        file_pages[q] != '\n' and \
        file_pages[q].startswith('http') == True and \
        edit_url_pages(file_pages[q].strip('\n')) not in fdir and \
        edit_url_pages(file_pages[q].strip('\n')) not in urls[0] and \
        file_pages[q].strip('\n') not in urls[1]: 
            urls[0].append(edit_url_pages(file_pages[q]))
            urls[1].append(file_pages[q].strip('\n'))
        if file_pages[q].startswith('search:'):
            fr = 'search...' + file_pages[q].strip('\n')[8:].replace(' ', '_') + '.html'
            if fr not in fdir:
                urls[0].append('search...' + file_pages[q].strip('\n')[8:].replace(' ', '_') + '.html')
                urls[1].append("https://google.com/search?q=" + file_pages[q].strip('\n')[7:])
    
    if urls == [[], []]: return 'File is empty or all urls are loaded early'
    return start_loading_page(0, urls, int(time.time()))

def start_loading_page(retries, urls, time_log):

    try:

        if urls == [[], []]: 
            logs_writer(f'Pages are loaded at {int(time.time()) - time_log}s', 'DOWNLOADING_PAGES')
            return make_web(0, '', 0)

        # Создаем подключение к сайту
        oscall('cls', 'clear')
        print(f'\n {cyell}Lost:{cnone}')
        for q in urls[1]: print(f'  {q}')
        print(f'{cyell}\n Try №{retries+1}:{cnone} {urls[1][0]}')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        full_page = requests.get(urls[1][0], headers=headers)
        page = full_page.text

        # Пишем в файл
        with open(f'downloader/pages/{urls[0][0]}', 'w', encoding='utf-8') as f: f.write(page)
        
        del urls[0][0]; del urls[1][0]
        return start_loading_page(retries, urls, time_log)

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return start_loading_page(retries, urls, time_log)
    except Exception as err:
        logs_writer(f'Authors error: {err}', 'DOWNLOADING_PAGES')
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'
