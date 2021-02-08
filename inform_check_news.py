import json, time, datetime, os, requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer
from utilities_make_web import *

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

# Выбор новостной ленты
def inform_check_news():

    oscall('cls', 'clear')

    print(f'\n {cyell}What type of news your want to load?{cnone}\n')
    print(f'    0. Go back')
    print(f'    1. Habr news')
    print(f'    2. IT-proger news')
    print(f'    3. Stack Overflow\n')

    usi = input(f" {cyell}>>>{cnone} ")
    if usi == "1": return preload('habr')
    elif usi == "2": return preload('itprog')
    elif usi == "3": return preload('SOF')
    else: return ""

# Выбор каталога в выбранной ленте
def preload(res):

    oscall('cls', 'clear')
 #      === HABR ===
    if res == "habr":
        print(f"""\n {cyell}Habr news. What we will do?{cnone}

    0. Go back
    1. Load lst news [all]
    2. Load top news [day]
    3. Load top news [week]
    4. Load top news [month]
    5. Load top news [year]
    6. Search on Habr\n""")

        us_inp = input(f'>>> ')
        if us_inp == "0": return "" 
        elif us_inp == "1": return habr_news(retries = 0, url = 'https://habr.com/ru/all/', res=res, time_log=int(time.time()))
        elif us_inp == "2": return habr_news(retries = 0, url = 'https://habr.com/ru/top/', res=res, time_log=int(time.time()))
        elif us_inp == "3": return habr_news(retries = 0, url = 'https://habr.com/ru/top/weekly/', res=res, time_log=int(time.time()))
        elif us_inp == "4": return habr_news(retries = 0, url = 'https://habr.com/ru/top/monthly/', res=res, time_log=int(time.time()))
        elif us_inp == "5": return habr_news(retries = 0, url = 'https://habr.com/ru/top/yearly/', res=res, time_log=int(time.time()))
        elif us_inp == "6": 
            vr = input(f'Type response >>> ')
            return habr_news(retries = 0, url = f'https://habr.com/ru/search/?q={vr}#h', res=res, time_log=int(time.time()))
        else: return "" 
    
 #      === IT PROG ===
    elif res == "itprog":
        print(f"""\n {cyell}IT-proger news. What we will do?{cnone}

    0. Go back
    1. Load last news 
    2. Load tasks 
    3. Load posts
    4. Load best
    5. Search on IT-proger\n""")

        us_inp = input(f'>>> ')
        if us_inp == "0": return "" 
        elif us_inp == "1": return habr_news(retries = 0, url = 'https://itproger.com/news/', res=res, time_log=int(time.time()))
        elif us_inp == "2": return habr_news(retries = 0, url = 'https://itproger.com/tasks/', res=res, time_log=int(time.time()))
        elif us_inp == "3": return habr_news(retries = 0, url = 'https://itproger.com/news/only/', res=res, time_log=int(time.time()))
        elif us_inp == "4": return habr_news(retries = 0, url = 'https://itproger.com/news/best/', res=res, time_log=int(time.time()))
        elif us_inp == "5": 
            vr = input(f'Type response >>> ')
            return habr_news(retries = 0, url = f'https://itproger.com/search/{vr}', res=res, time_log=int(time.time()))
        else: return ""        

 #      === SOF ===
    elif res == "SOF":
        print(f"""\n {cyell}StackOverFlow news. What we will do?{cnone}

    0. Go back
    1. Load interesting
    2. Load top
    3. Load top week
    4. Load top month
    5. Search on SOF
    6. Search with tags\n""")

        us_inp = input(f'{cyell}>>>{cnone} ')
        if us_inp == "0": return "" 
        elif us_inp == "1": return habr_news(retries = 0, url = 'https://ru.stackoverflow.com/?tab=interesting', res=res, time_log=int(time.time()))
        elif us_inp == "2": return habr_news(retries = 0, url = 'https://ru.stackoverflow.com/?tab=hot', res=res, time_log=int(time.time()))
        elif us_inp == "3": return habr_news(retries = 0, url = 'https://ru.stackoverflow.com/?tab=week', res=res, time_log=int(time.time()))
        elif us_inp == "4": return habr_news(retries = 0, url = 'https://ru.stackoverflow.com/?tab=month', res=res, time_log=int(time.time()))
        elif us_inp == "5": 
            vr = input(f' {cyell}Type response >>>{cnone} ')
            return habr_news(retries = 0, url = f'https://ru.stackoverflow.com/search?q={vr}', res=res, time_log=int(time.time()))
        elif us_inp == "6":
            tags_dict = ['asyncio', 'async', 'python', 'javascript', 'python-3.x', 'c++', 'c#', 'php', 'html', 'css', 'java', 'linux', 'pyqt5', 'gui', 'android', 'pyqt', 'c', 'строки', 'jquery', 'node.js', 'unity3d', 'pandas', 'mysql', 'sql', 'массивы', 'windows', 'oracle', 'telegram-bot', 'wpf', 'парсер', 'wordpress', 'база-данных', 'django', 'reactjs', 'vue.js', 'svg', 'нейронные-сети', 'dataframe', 'plsql', 'словари', 'qt', 'ubuntu', 'вёрстка', 'selenium', 'opengl', 'обработка-данных', '.net', 'json', 'регулярные-выражения', 'веб-программирование', 'многопоточность', 'spring', 'сервер', 'mongobd', 'list', 'tkinter', 'qt-designer', 'css3', 'lavarel', 'xml', 'файлы', 'asp.net-mvc']
            print(f'\n{cyell}Type tags from next list:{cnone}')
            for k in tags_dict: print(f'  {k}')
            print(f' \n{cyell}Example:{cnone} python+selenium+asyncio')
            us_inp = input(f'{cyell}>>>{cnone} ')
            return habr_news(retries = 0, url = f'https://ru.stackoverflow.com/questions/tagged/{us_inp}', res=res, time_log=int(time.time()))
        else: return ""  

# Загрузка последних новостей в консоль
def habr_news(retries, url, res, time_log):

    try:

        # Переменные с данными постов
        tittles = []        # название поста
        links = []          # ссылки на пост
        text_tittles = []   # короткий текст поста
        counter = []        # рейтинг поста
        files = []          # уже сохраненные посты
        
        # Создаем подключение к сайту
        oscall('cls', 'clear')
        print(f'{cyell}\n Try №{retries+1}:{cnone} {url}')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        full_page = requests.get(url, headers=headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')

 #=============================== HABR ==========================================================
        if res == "habr":
            # Ищем ссылки и названия статей
            convert = soup.findAll("a", {"class": "post__title_link"})
            for q in range(len(convert)):
                er = convert[q].text
                er = er.replace("\\", "")
                er = er.replace("/", "")
                er = er.replace(":", "")
                er = er.replace("*", "")
                er = er.replace("?", "")
                er = er.replace('"', "")
                er = er.replace("<", "")
                er = er.replace(">", "")
                er = er.replace("|", "")
                er = er.replace("#", "")
                tittles.append(f'{er}')
                links.append(f'{convert[q].get("href")}')

            # Ищем короткий текст статьи
            post_text = soup.findAll("div", {"class": "post__text", "class": "post__text-html"})
            for q in range(len(post_text)):
                r = post_text[q].text
                r2 = r.replace("\n", "")
                text_tittles.append(f'{r2}')

            # Ищем рейтинг поста
            stat = soup.findAll("span", {"class": "post-stats__result-counter"})
            for q in range(len(stat)):
                counter.append(f'{stat[q].text}')

            # Проверяем существование загруженных статей на компьютер
            file_names_in_dir = os.listdir(path="inform/habr/pages/")
            for q in file_names_in_dir:
                files.append(f'{q.replace(".html", "")}')

            # Запускаем функцию загрузки сайтов в файл
            oscall('cls', 'clear')
            for u in range(len(tittles)):
                print(f'\n {u}. {cyell}{tittles[u]}{cnone} \033[36m[{counter[u]}]{cnone}', end = "")
                if tittles[u] in files: print(f"\033[36m [Loaded!]{cnone}")
                else: print(f"")
                print(f'   {text_tittles[u]}\n')
          
            logs_writer(f'Habr news are loaded in console at {int(time.time()) - time_log}s', 'HABR_NEWS')
            us_in = input(f'''\n {cyell}Its last news.{cnone} \n  0. Go back\n  1. Numbers of titles\n  2. Or load all data?\n >>> ''')            
            if us_in == "0": return "Return"
            elif us_in == "1": 
                img = input(f'\n  0. Without images \n  1. With images\n >>> ')
                if img == "0":
                    us_in = input(f'\n Type numbers >>> ')
                    us_in = us_in.split(" ")
                    return loading_sites(retries = 0, what_loading=us_in, tittles=tittles, links=links, files=files, url=url, res=res, img=0, time_log=int(time.time()))
                elif img == "1":
                    us_in = input(f'\n Type numbers >>> ')
                    us_in = us_in.split(" ")
                    return loading_sites(retries = 0, what_loading=us_in, tittles=tittles, links=links, files=files, url=url, res=res, img=1, time_log=int(time.time()))
                else: return "Unknown response"
            elif us_in == "2": 
                img = input(f'\n\n  0. Without images \n  1. With images\n >>> ')
                if img == "0": return loading_sites(retries = 0, what_loading="all", tittles=tittles, links=links, files=files, url=url, res=res, img=0, time_log=int(time.time()))
                elif img == "1": return loading_sites(retries = 0, what_loading="all", tittles=tittles, links=links, files=files, url=url, res=res, img=1, time_log=int(time.time()))
                else: return "Unknown response"
            else:
                return "Unknown response" 
 #=============================== IT PROG ==========================================================
        elif res == "itprog":
            convert = soup.findAll("div", {"class": "article"})
            for q in range(len(convert)):
                # Ищем названия статей
                wq = convert[q].findAll("a")
                wq = wq[0].get("title")
                wq = wq.replace("\\", "")
                wq = wq.replace("/", "")
                wq = wq.replace(":", "")
                wq = wq.replace("*", "")
                wq = wq.replace("?", "")
                wq = wq.replace('"', "")
                wq = wq.replace("<", "")
                wq = wq.replace(">", "")
                wq = wq.replace("|", "")
                wq = wq.replace("#", "")
                tittles.append(f'{wq}')

                # Ищем ссылки статей
                wq = convert[q].findAll("a")
                if url == "https://itproger.com/news/": 
                    if wq[0].get("href").find("tasks") != -1: links.append(f'https://itproger.com{wq[0].get("href")}')
                    else: links.append(f'https://itproger.com/{wq[0].get("href")}')
                elif url == "https://itproger.com/news/best/": 
                    if wq[0].get("href").find("tasks") != -1: links.append(f'https://itproger.com{wq[0].get("href")}')
                    else: links.append(f'https://itproger.com/news/{wq[0].get("href")}')
                elif url == "https://itproger.com/tasks/": links.append(f'https://itproger.com/{wq[0].get("href")}')
                elif url == "https://itproger.com/news/only/": links.append(f'https://itproger.com/news/{wq[0].get("href")}')
                elif url.find("https://itproger.com/search/") != 1: links.append(f'https://itproger.com{wq[0].get("href")}')

                # Ищем короткое описание статей
                wq = convert[q].findAll("span")
                text_tittles.append(f'{wq[1].text}')

            # Проверяем существование загруженных статей на компьютер
            file_names_in_dir = os.listdir(path="inform/itprog/pages/")
            for q in file_names_in_dir:
                files.append(f'{q.replace(".html", "")}')  

            # Запускаем функцию загрузки сайтов в файл
            oscall('cls', 'clear')
            for u in range(len(tittles)):
                print(f'\n {u}. {cyell}{tittles[u]}{cnone}', end = "")
                if tittles[u] in files: print(f"\033[36m [Loaded!]{cnone}")
                else: print(f"")
                print(f'   {text_tittles[u]}\n')
            
            logs_writer(f'IT-prog news are loaded in console at {int(time.time()) - time_log}s', 'ITPROG_NEWS')
            us_in = input(f'\n {cyell}Its last news.{cnone} \n  0. Go back\n  1. Numbers of titles\n  2. Or load all data?\n >>> ')
            if us_in == "0": return "Return"
            elif us_in == "1": 
                us_in = input(f'\n Type numbers >>> ')
                us_in = us_in.split(" ")
                return loading_sites(retries = 0, what_loading=us_in, tittles=tittles, links=links, files=files, url=url, res=res, img=0, time_log=int(time.time()))
            elif us_in == "2": 
                img = input(f'\n  0. Without images \n  1. With images\n >>> ')
                if img == "0": return loading_sites(retries = 0, what_loading="all", tittles=tittles, links=links, files=files, url=url, res=res, img=0, time_log=int(time.time()))
                elif img == "1": return loading_sites(retries = 0, what_loading="all", tittles=tittles, links=links, files=files, url=url, res=res, img=1, time_log=int(time.time()))
                else: return "Unknown response"
            else:
                return "Unknown response"           

  #=============================== SOF ==========================================================
        if res == "SOF":
            # Ищем ссылки и названия статей
            convert = soup.findAll("a", {"class": "question-hyperlink"})
            for q in range(len(convert)):
                er = convert[q].text
                er = er.replace("\\", "")
                er = er.replace("/", "")
                er = er.replace(":", "")
                er = er.replace("*", "")
                er = er.replace("?", "")
                er = er.replace('"', "")
                er = er.replace("<", "")
                er = er.replace(">", "")
                er = er.replace("|", "")
                er = er.replace("#", "")    
                er = er.replace("            ", "")  
                er = er.replace("        ", "")   
                er = er.replace("\r\n", "")      
                tittles.append(f'{er}')
                links.append(f'https://ru.stackoverflow.com{convert[q].get("href")}')

            # Ищем рейтинг поста
            if url.find('search?q=') != -1 or url.find('ions/tagged/') != -1:
                stat = soup.findAll("div", {"class": "stats"}) 
                for q in range(len(stat)):
                    er = stat[q].text
                    er = er.replace("\r\n                    \n", "")
                    er = er.replace("\n\n\n", "")
                    er = er.replace("\nголос\n", " голос; ")
                    er = er.replace("\nголоса\n", " голоса; ")
                    er = er.replace("\nголосов\n", " голосов; ")
                    er = er.replace("\nголос", " голос")
                    er = er.replace("\nголоса", " голоса")
                    er = er.replace("\nголосов", " голосов")
                    er = er.replace("ответ", " ответ")
                    er = er.replace("\n", "")
                    er = er.replace("\r            ", "")
                    counter.append(f'{er}')
            else:
                stat = soup.findAll("div", {"class": "cp"}) 
                for q in range(len(stat)):
                    er = stat[q].text
                    er = er.replace("\n\n", "")
                    er = er.replace("\n", " ")
                    counter.append(f'{er}')

            # Ищем короткий текст статьи
            if url.find('search?q=') != -1 or url.find('ions/tagged/') != -1:
                post_text = soup.findAll("div", {"class": "excerpt"})
                for q in range(len(post_text)):
                    r = post_text[q].text
                    r2 = r.replace("\n", "")
                    r2 = r.replace("\r                 ", "  ")
                    r2 = r.replace("\r            ", "")
                    r2 = r.replace("\r\n            ", "")
                    r2 = r.replace("\r\n        ", "")
                    text_tittles.append(f'{r2}')
            else:
                post_text = soup.findAll("div", {"class": "tags"})
                for q in range(len(post_text)):
                    r2 = post_text[q].get("class")
                    text_tittles.append(f'{r2}')
                    
            # Проверяем существование загруженных статей на компьютер
            file_names_in_dir = os.listdir(path="inform/SOF/pages/")
            for q in file_names_in_dir:
                files.append(f'{q.replace(".html", "")}')

            # Запускаем функцию загрузки сайтов в файл

            oscall('cls', 'clear')
            #print(soup)
            for u in range(len(tittles)):
                print(f'\n {u}. {cyell}{tittles[u]}{cnone} \033[36m[{counter[u]}]{cnone}', end = "")
                if tittles[u] in files: print(f"\033[36m [Loaded!]{cnone}")
                else: print(f"")
                print(f'   {text_tittles[u]}\n')
          
            logs_writer(f'SOF news are loaded in console at {int(time.time()) - time_log}s', 'SOF_NEWS')
            us_in = input(f'''\n {cyell}Its last news.{cnone} \n  0. Go back\n  1. Numbers of titles\n  2. Or load all data?\n >>> ''')            
            if us_in == "0": return "Go back"
            elif us_in == "1": 
                img = input(f'\n  0. Without images \n  1. With images\n >>> ')
                if img == "0":
                    us_in = input(f'\n Type numbers >>> ')
                    us_in = us_in.split(" ")
                    return loading_sites(retries = 0, what_loading=us_in, tittles=tittles, links=links, files=files, url=url, res=res, img=0, time_log=int(time.time()))
                elif img == "1":
                    us_in = input(f'\n Type numbers >>> ')
                    us_in = us_in.split(" ")
                    return loading_sites(retries = 0, what_loading=us_in, tittles=tittles, links=links, files=files, url=url, res=res, img=1, time_log=int(time.time()))
                else: return "Unknown response"
            elif us_in == "2": 
                img = input(f'\n\n  0. Without images \n  1. With images\n >>> ')
                if img == "0": return loading_sites(retries = 0, what_loading="all", tittles=tittles, links=links, files=files, url=url, res=res, img=0, time_log=int(time.time()))
                elif img == "1": return loading_sites(retries = 0, what_loading="all", tittles=tittles, links=links, files=files, url=url, res=res, img=1, time_log=int(time.time()))
                else: return "Unknown response"
            else:
                return "Unknown response" 
                

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return habr_news(retries=retries, url=url, res=res, time_log=time_log)
    except Exception as err:
        logs_writer(f'Authors error: {err}', 'LOAD_NEWS')
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'

# Загрузка выбранных новостей в файл
def loading_sites(retries, what_loading, tittles, links, files, url, res, img, time_log):

    try: 

        load = []

        if what_loading == "all": 
            what_loading = []
            for q in range(len(tittles)): what_loading.append(q)

        files = []
        
        file_names_in_dir = os.listdir(path=f"inform/{res}/pages/")
        for q in file_names_in_dir:
            files.append(f'{q.replace(".html", "")}')

        for q in what_loading:
            if tittles[int(q)] not in files:
                load.append(f'{links[int(q)]}')

        if load == []: 
            logs_writer(f'{res} pages are loaded at {int(time.time()) - time_log}s', 'PAGES_LOAD')
            return make_web(retries=retries, res=res, time_log=time_log)
        else:
            oscall('cls', 'clear')
            print(f'{cyell}\n Lost:{cnone}')
            for q in range(len(load)): print(f'  {q}. {load[q]}')
            print(f'\n{cyell} Try №{retries+1}:{cnone} {load[0]}')
            url = f'{load[0]}'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
            full_page = requests.get(url, headers=headers)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            page = full_page.text

            # Названия статей
            ttl = soup.findAll("meta", {"property": "og:title"})
            ttl = ttl[0].get("content")
            ttl = ttl.replace("\\", "")
            ttl = ttl.replace("/", "")
            ttl = ttl.replace(":", "")
            ttl = ttl.replace("*", "")
            ttl = ttl.replace("?", "")
            ttl = ttl.replace('"', "")
            ttl = ttl.replace("<", "")
            ttl = ttl.replace(">", "")
            ttl = ttl.replace("|", "")
            ttl = ttl.replace("#", "")

            # Картинки в статье

                    # ======= HABR IMG =======
            if img == 1:
                if res == "habr": 
                    imgs_dict = []
                    imgs = soup.findAll("img")
                    for nz in range(len(imgs)): 
                        if imgs[nz].get("src").find("https://habrastorage.org") != -1:
                            imgs_dict.append(imgs[nz].get("src"))
                            page = page.replace(imgs[nz].get("src"), f"img/{imgs[nz].get('src').split('/')[-1]}")
                    load_images(retries=0, img=imgs_dict, time_log=time_log, res=res)
                    # ======= IT PROG IMG =======
                if res == "itprog":
                    pass
                    # ======= SOF IMG =======
                if res == "SOF":
                    pass

            # Меняем css
            stl = soup.findAll("link", {"rel": "stylesheet"}) 
            for q in stl: hrf = q.get("href"); page = page.replace(hrf, 'css/1.css')
            page = page.replace("https://use.fontawesome.com/releases/v5.8.2/css/all.css", "css/1.css")
            page = page.replace("/css/A.main-style.css.pagespeed.cf.Lk7iJwZHZH.css", "css/2.css")
            page = page.replace("/css/A.aside.css.pagespeed.cf.WUE28L1Nvv.css", "css/3.css")
            page = page.replace("/css/A.one-article.css.pagespeed.cf.Jr-8wfOxxq.css", "css/4.css")
            page = page.replace('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>', '')
            page = page.replace('<script src="https://cdn.sstatic.net/Js/stub.ru.js?v=87ba97fcd781"></script>', '')

            # Пишем в файл
            with open(f'inform/{res}/pages/' + ttl + '.html', 'w', encoding='utf-8') as f: f.write(page)
            return loading_sites(retries=retries, what_loading=what_loading, tittles=tittles, links=links, files=files, url=url, res=res, img=img, time_log=time_log)

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return loading_sites(retries=retries, what_loading=what_loading, tittles=tittles, links=links, files=files, url=url, res=res, img=img, time_log=time_log)
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'

# Загрузка изображений, если требуется
def load_images(retries, img, time_log, res):

    try:

        oscall('cls', 'clear')
        # Существование файла
        url = img[0]
        name = url.split("/")[-1]
        # Размер файла
        chkf = os.path.exists(f"inform/{res}/pages/img/" + name)
        if chkf == True: szf = os.path.getsize(f"inform/{res}/pages/img/" + name)
        else: szf = 0

        #print(f'{name}')
        print(f' {cyell}Try №{retries+1}{cnone} to connecting ...')
        print(f' {url}')
        
        # Вес файла на сервере/грузим файл
        r = requests.get(url)
        ttlsz = int(r.headers.get('content-length', 0))
        check_range = r.headers['Accept-Ranges']

        oscall('cls', 'clear')
        print(f' {cyell}Lost:{cnone}')
        for ger in img: print(f'  {ger.split("/")[-1]}')
        print(f'\n {cyell}Try №{retries+1}.{cnone} Download {name}')
        if szf == ttlsz: 
            del img[0]
            if img == []: return
            else: return load_images(retries=retries, img=img, time_log=time_log, res=res)
        else:
            with open(f"inform/{res}/pages/img/{name}", 'ab') as f:
                headers = {}
                pos = f.tell()
                if pos:
                    headers['Range'] = f'bytes={pos}-'
                response = requests.get(url, headers=headers, stream=True)
                progress_bar = tqdm(response.iter_content(chunk_size = 1024), total = (ttlsz - szf)//1024, unit = 'kB')
                for data in progress_bar:
                    f.write(data)
                f.close()

            szf = os.path.getsize(f"inform/{res}/pages/img/" + name)
            if szf == ttlsz:
                del img[0]
                if img == []: return 'ok'
                else: return load_images(retries=retries, img=img, time_log=time_log, res=res)       

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return load_images(retries=retries, img=img, time_log=time_log, res=res)
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'