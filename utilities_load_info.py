import json, time, datetime, os, requests, json

from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer
from another_modules import data_config
from downloader_files import *

global cyell, cnone
cyell = '\033[33m'
cblue = '\033[36m'
cnone = '\033[0m'
cred = '\033[31m'

def utilities_load_info():

    if data_config('TLG_TK') == "no data": tlgtk_check = f'1. Telegram  \033[31mHave no TOKEN. Type "1" for add{cnone}'
    else: tlgtk_check = '1. Telegram'

    oscall('cls', 'clear')
    print(f'\n {cyell}What service we will use?{cnone}')
    print(f'  0. Go back')
    print(f'  {tlgtk_check}')
    usi = input(f" {cyell}>>>{cnone} ")
    if usi == "1":
        if data_config('TLG_TK') == "no data": oscall('start another_config.json', ''); return 'Change "TLG_TK" and retry'
    else: return 'Go back'

    print(f'\n {cyell}What we will load?{cnone}')
    print(f'  0. Go back')
    print(f'  1. Last updates')
    usi = input(f" {cyell}>>>{cnone} ")
    if usi == "1": return telegram_request()
    else: return 'Go back'    

def telegram_request(url = "", retries = 0):
    
    try:

        oscall('cls', 'clear')
        token = data_config('TLG_TK')
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        print(f"\n {cyell}Try №{retries+1}{cnone} to connecting telegram ...")
        
        response = requests.get(url)
        data = response.json()
        results = data['result']
        with open("utilities/telegram/dict_data.json", "w", encoding='utf-8') as write_file: json.dump(data, write_file, indent=4)

        oscall('cls', 'clear')
        if len(results) == 0: return f'Telegram BOT: have no updates' 
        print(f'\n Loaded {cyell}{len(results)}{cnone} updates.\n How many last updates ur want {cyell}to load?{cnone}')
        usi = input(f'\n {cyell}>>>{cnone} ')

        if int(usi) > len(results): return f'\n {cred}Wrong response{cnone}{cyell} ({usi} > {len(results)})'
        else: update = results[-int(usi):]; return get_data(update)

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return telegram_request(url, retries)
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'

def get_data(update):

        oscall('cls', 'clear')
        info_dict = []
        load_dict = []

        # Собираем информацию из json ответа telegram'a
        for i in update:
            message_id = str(i['message']['message_id'])
            first_name = str(i['message']['chat']['first_name'])
            chat_id = str(i['message']['chat']['id'])
            if 'audio' in i['message']: 
                file_name = str(i['message']['audio']['performer']) if 'performer' in i['message']['audio'] else 'Unknown'
                file_name += ' - '
                file_name += str(i['message']['audio']['title']) if 'title' in i['message']['audio'] else 'Unknown'
                file_name += '.' + str(i['message']['audio']['file_name'].split('.')[-1]) if 'file_name' in i['message']['audio'] else '.mp3'
                if 'file_name' in i['message']['audio']: file_name = str(i['message']['audio']['file_name']) 
                file_size = str(i['message']['audio']['file_size']) if 'file_size' in i['message']['audio'] else 'Unknown'
                if int(i['message']['audio']['file_size']) > 19999999: file_size = 'Too big' 
                file_id = str(i['message']['audio']['file_id']) if 'file_id' in i['message']['audio'] else 'Unknown'
                file_url = 'Unknown'
                file_text = 'No text'
            elif 'photo' in i['message']: 
                file_name = str(i['message']['photo'][len(i['message']['photo'])-1]['file_name']) if 'file_name' in i['message']['photo'][len(i['message']['photo'])-1] else 'Unknown'
                file_size = str(i['message']['photo'][len(i['message']['photo'])-1]['file_size']) if 'file_size' in i['message']['photo'][len(i['message']['photo'])-1] else 'Unknown'
                file_id = str(i['message']['photo'][len(i['message']['photo'])-1]['file_id']) if 'file_id' in i['message']['photo'][len(i['message']['photo'])-1] else 'Unknown'
                file_url = 'Unknown'       
                file_text = 'No text'
            elif 'video' in i['message']: 
                file_name = str(i['message']['video']['file_name']) if 'file_name' in i['message']['video'] else 'Unknown'
                file_size = str(i['message']['video']['file_size']) if 'file_size' in i['message']['video'] else 'Unknown'
                if int(i['message']['video']['file_size']) > 19999999: file_size = 'Too big' 
                file_id = str(i['message']['video']['file_id']) if 'file_id' in i['message']['video'] else 'Unknown'
                file_url = 'Unknown'       
                file_text = 'No text'
            elif 'document' in i['message']: 
                file_name = str(i['message']['document']['file_name']) if 'file_name' in i['message']['document'] else 'Unknown'
                file_size = str(i['message']['document']['file_size']) if 'file_size' in i['message']['document'] else 'Unknown'
                if int(i['message']['document']['file_size']) > 19999999: file_size = 'Too big' 
                file_id = str(i['message']['document']['file_id']) if 'file_id' in i['message']['document'] else 'Unknown'
                file_url = 'Unknown'       
                file_text = 'No text'
            elif 'text' in i['message']: 
                file_name = 'No name'
                file_size = 'No size'
                file_id = 'No id'
                file_url = 'No url'   
                file_text = str(i['message']['text'])
            else:
                file_name = 'Unknown type'
                file_size = 'Unknown type'
                file_id = 'Unknown type'
                file_url = 'Unknown type'
                file_text = 'Unknown type'
            info_dict.append((message_id, first_name, chat_id, file_name, file_size, file_id, file_url, file_text))

        # Составляем json текст и пишем его в файл
        txt_json = '{'
        for q in range(len(info_dict)):
            txt_json += f'"{info_dict[q][0]}":'
            txt_json += '{'
            txt_json += f'"first_name": "{info_dict[q][1]}",'
            txt_json += f'"chat_id": "{info_dict[q][2]}",'
            txt_json += f'"file_name": "{info_dict[q][3]}",'
            txt_json += f'"file_size": "{info_dict[q][4]}",'
            txt_json += f'"file_id": "{info_dict[q][5]}",'
            txt_json += f'"file_url": "{info_dict[q][6]}",'
            txt_json += f'"file_text": "{info_dict[q][7]}"'
            txt_json += '}'
            if q != len(info_dict)-1: txt_json += ','
            if info_dict[q][5] != 'No id' and info_dict[q][4] != 'Too big': load_dict.append((
                                                                                info_dict[q][3],  # name
                                                                                info_dict[q][4],  # size
                                                                                info_dict[q][5],  # file id
                                                                                info_dict[q][0])) # msg id
        txt_json += '}'
        dataz = json.loads(txt_json)
        with open(f"utilities/telegram/data.json", "w", encoding='utf-8') as wwe_file: json.dump(dataz, wwe_file, indent = 4)

        # Выводим на экран данные о каждом update
        txt = ''
        for q in range(len(info_dict)):
            txt += f' {cyell}{q}.{cnone}'
            txt += f'\n  Message id: {info_dict[q][0]}'
            txt += f'\n  First name: {info_dict[q][1]}'
            txt += f'\n  Chat id: {info_dict[q][2]}'
            txt += f'\n  File name: {info_dict[q][3]}'
            txt += f'\n  File size: {info_dict[q][4]}'
            txt += f'\n  File id: {info_dict[q][5]}'
            txt += f'\n  File url: {info_dict[q][6]}'
            txt += f'\n  Text: {info_dict[q][7]} \n'
        print(txt)

        print(f'\n {cyell}Its ur updates. What we will do?{cnone}')
        print(f'  0. Go back')
        print(f'  1. Load urls for all files')
        usi = input(f' {cyell}>>>{cnone} ')

        if usi == '1': return load_urls(0, load_dict)
        else: return 'Go back'

def load_urls(retries, load_dict):

    try:

        if load_dict != []:
            oscall('cls', 'clear')
            token = data_config('TLG_TK')
            url = f"https://api.telegram.org/bot{token}/getFile?file_id={load_dict[0][2]}"
            
            print(f"\n {cyell}Lost:{cnone}")
            for q in range(len(load_dict)): print(f'  {q+1}. {load_dict[q][0]}')
            print(f"\n {cyell}Try №{retries+1}{cnone} to collecting url for {cblue}{load_dict[0][0]}{cnone}")
            
            response = requests.get(url)
            data = response.json()
            file_url = data['result']['file_path']
            file_size = data['result']['file_size']
            url_load = f'https://api.telegram.org/file/bot{token}/{file_url}'

            # Записываем в файл ссылки на файлы
            with open(f"utilities/telegram/data.json", "r", encoding='utf-8') as read_file: data2 = json.load(read_file)
            with open(f"utilities/telegram/data.json", "w", encoding='utf-8') as w_file: 
                if load_dict[0][0] == 'Unknown': data2[load_dict[0][3]]["file_name"] = file_url.split('/')[-1]
                else: data2[load_dict[0][3]]["file_name"] = load_dict[0][0]
                data2[load_dict[0][3]]["file_url"] = url_load
                json.dump(data2, w_file, indent = 4)

            del load_dict[0]
            time.sleep(1)
            return load_urls(retries, load_dict)

        # Выводим на экран обновленную информацию
        oscall('cls', 'clear') 
        with open(f"utilities/telegram/data.json", "r", encoding='utf-8') as rf: rff = json.load(rf)
        for q in rff:
            print(f' {cyell}{q}.{cnone}')
            print(f'  First name: {str(rff[q]["first_name"])}')
            print(f'  Chat id: {str(rff[q]["chat_id"])}')
            print(f'  File name: {str(rff[q]["file_name"])}')
            print(f'  File size: {str(rff[q]["file_size"])}')
            print(f'  File id: {str(rff[q]["file_id"])}')
            print(f'  File url: {str(rff[q]["file_url"])}')
            print(f'  File text: {str(rff[q]["file_text"])}')

        print(f'\n {cyell}Done. What we will do?{cnone}')
        print(f'  0. Write data in file and go back')
        print(f'  1. Start downloading this files')
        usi = input(f' {cyell}>>>{cnone} ')

        if usi == '1': 
            with open(f"utilities/telegram/data.json", "r", encoding='utf-8') as s1: s = json.load(s1)
            with open(f'downloader/files.txt', 'a', encoding='utf-8') as e: 
                for fz in s: 
                    if s[fz]["file_url"] != 'No url' and s[fz]["file_url"] != 'Unknown':
                        e.write(f'\n{str(s[fz]["file_url"])}')
            return preload_files()
        else: return 'Done. Check utilities/telegram/data.json'

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return load_urls(retries, load_dict)
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'    