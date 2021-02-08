import json, time, datetime, os, requests
from tqdm import tqdm
from bs4 import BeautifulSoup

from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer
from another_modules import edit_url_pages
from utilities_make_web import *

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

def downloader_files():

    oscall('cls', 'clear')
    print(f'\n {cyell}What we will do?{cnone}')
    print(f'    0. Go back')
    print(f'    1. Download all pages into downloader/files.txt')
    print(f'    Or type download-url')
    usi = input(f" {cyell}>>>{cnone} ")

    if usi == "0": return "Go back"
    elif usi == "1": return open_file()
    else: 
        if usi.startswith('https://') or usi.startswith('http://'): 
            with open(f'downloader/files.txt', 'a', encoding='utf-8') as e: e.write(f'\n{usi}')
            return start_loading(0, [[usi.strip('\n').strip().split('/')[-1]], [usi]], int(time.time()))
        else: 
            with open(f'downloader/files.txt', 'a', encoding='utf-8') as e: e.write(f'\nhttps://{usi}')
            return start_loading(0, [[usi.strip('\n').strip().split('/')[-1]], ['https://' + usi]], int(time.time()))

def open_file():

    oscall('cls', 'clear')
    oscall('start downloader/files.txt', '')
    print(f'\n {cyell}What we will do?{cnone}')
    print(f'    0. Go back')
    print(f'    1. Start loading')
    print(f'    2. Change files.txt again')
    usi = input(f" {cyell}>>>{cnone} ")

    if usi == "1": return preload_files()
    elif usi == "2": return open_file()
    else: return "Go back"    

def preload_files():
    
    f = open("downloader/files.txt", encoding='utf-8')
    file_pages = f.readlines()
    urls = [[],[]]
    for q in range(len(file_pages)):
        fdir = os.listdir(path="downloader/files/")
        if file_pages[q] != '' and \
        file_pages[q].startswith('#') == False and \
        file_pages[q] != '\n' and \
        file_pages[q].startswith('http') == True and \
        edit_url_pages(file_pages[q].strip('\n')) not in fdir and \
        edit_url_pages(file_pages[q].strip('\n')) not in urls[0] and \
        file_pages[q].strip('\n') not in urls[1]: 
            if file_pages[q].find('api.telegram.org/file/') != -1:
                with open(f"utilities/telegram/data.json", "r", encoding='utf-8') as s1: s = json.load(s1)
                for ex in s:
                    if s[ex]["file_url"] == file_pages[q].strip('\n'): 
                        urls[0].append(s[ex]["file_name"])
                        urls[1].append(file_pages[q].strip('\n'))
            else:
                urls[0].append(file_pages[q].split('/')[-1].strip('\n'))
                urls[1].append(file_pages[q].strip('\n'))
    
    if urls == [[], []]: return 'File is empty or all urls are loaded early'
    return start_loading(0, urls, int(time.time()))

def start_loading(retries, urls, time_log):

    try:

        # После загрузки всех файлов выполняем
        oscall('cls', 'clear')
        if urls == [[], []]: 
            logs_writer(f'Files are loaded at {int(time.time()) - time_log}s', 'DOWNLOADER_FILES')
            oscall('start downloader\\files', '')
            return 'File(s) loaded. Check downloader/files'

        # Размер файла
        chkf = os.path.exists(f"downloader/files/" + urls[0][0])
        if chkf == True: size_file = os.path.getsize(f"downloader/files/" + urls[0][0])
        else: size_file = 0

        # Печать: осталось файлов
        print(f'\n {cyell}Lost:{cnone}')
        for q in urls[1]: print(f'  {q}')
        print(f'{cyell}\n Try №{retries+1}:{cnone} {urls[0][0]}')

        # Устанавливаем соединение
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        full_page = requests.get(urls[1][0], headers=headers, stream=True)
        total_size_in_bytes = int(full_page.headers.get('content-length', 0))
        check_range = full_page.headers['Accept-Ranges']
        need_load = 100-((size_file * 100) // total_size_in_bytes)
        need_load_b = total_size_in_bytes - size_file

        # Печать: информация о файле
        print(f"""\n{cyell} File info: {cnone}
  File size on server: {total_size_in_bytes}b  ({format(total_size_in_bytes/1000, '0.0f')} kB; {format(total_size_in_bytes/1000000, '0.2f')} mB)
  File size on computer: {size_file}b ({format(size_file/1000, '0.0f')} kB; {format(size_file/1000000, '0.2f')} mB)
  Need load: {need_load_b}b ({format(need_load_b/1000, '0.0f')} kB; {format(need_load_b/1000000, '0.2f')} mB)
  Need load: {need_load}%""")

        # Пишем файл
        # Если файл полностью скачан -- удаляем из списка загрузок
        if size_file == total_size_in_bytes:
            logs_writer(f'File: {urls[0][0]} is loaded at {int(time.time()) - time_log}s', 'FILE_DOWNLOADER')
            del urls[0][0]; del urls[1][0]
            return start_loading(retries, urls, time_log)
        # Если файл не полностью скачан -- качаем с места, на котором остановились
        else:
            with open("downloader/files/" + urls[0][0], 'ab') as f:
                headers = {}
                pos = f.tell()
                if pos: headers['Range'] = f'bytes={pos}-'
                response = requests.get(urls[1][0], headers=headers, stream=True)
                progress_bar = tqdm(response.iter_content(chunk_size = 1024), total = (total_size_in_bytes - size_file)//1024, unit = 'kB')
                for data in progress_bar: f.write(data)
                f.close()
        
        # Проверяем до конца ли докачался файл
        size_file = os.path.getsize(f"downloader/files/" + urls[0][0])
        # Если до конца -- удаляем из списка загрузок
        if size_file == total_size_in_bytes:
            logs_writer(f'File: {urls[0][0]} is loaded at {int(time.time()) - time_log}s', 'FILE_DOWNLOADER')
            del urls[0][0]; del urls[1][0]
        # Если нет -- запускаем повторно
        else: retries += 1
        return start_loading(retries, urls, time_log)

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return start_loading(retries, urls, time_log)
    except Exception as err:
        logs_writer(f'Authors error: {err}', 'FILE_DOWNLOADER')
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'
