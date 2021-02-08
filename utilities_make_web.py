import json, time, datetime, os, requests
from bs4 import BeautifulSoup

from another_modules import oscall

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

# Собираем local web page
def make_web(retries, res, time_log):

  #========================== HABR =====================================================================

    # Читаем названия всех файлов в папке, заходим в каждый и забираем информацию
    l_upd = datetime.datetime.fromtimestamp(int(time.time())).strftime("%d.%m.%Y %H:%M:%S")
    file_names_in_dir = os.listdir(path=f"inform/habr/pages/")
    f = []
    count = 1
    size_file = 0

    for q in file_names_in_dir:
        if q.find('.html') != -1:
            oscall('cls', 'clear')
            print(f' {cyell}Into: HABR NEWS.html{cnone}')
            print(f' {cyell}Status:{cnone} {count}/{len(file_names_in_dir)}')
            print(f' {cyell}Now:{cnone} {q}')
            with open(f'inform/habr/pages/{q}', 'r', encoding='utf-8') as filer: content = filer.read()
            soup = BeautifulSoup(content, 'html.parser')

            stat = soup.findAll("span", {"class": "voting-wjt__counter", "class": "voting-wjt__counter_negative", "class": "js-score"})
            if stat == []: stat = soup.findAll("span", {"class": "voting-wjt__counter", "class": "voting-wjt__counter_positive", "class": "js-score"})
            descr = soup.findAll("div", {"class": "post__text"})

            descr = descr[0].text[0:300]
            size_file += os.path.getsize(f"inform/habr/pages/{q}")

            f.append((int(os.path.getctime(f'inform/habr/pages/{q}')), f'{q[:-5]}', f'{stat[0].text}', f'{descr}...'))
            count += 1
    f.sort(reverse = True)

    files_text = ""
    timeq = f''
    for q in f: 
        if timeq == '': 
            timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
            files_text += f'<p id="timed">{timeq}</p><li><a href="../../inform/habr/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a> <br><p id="descr">{q[3]} [{q[2]}]<p></li>\n'
        else:
            if timeq == datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y"): 
                files_text += f'<li><a href="../../inform/habr/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[3]} [{q[2]}]<p></li>\n'
            else:
                timeq = ''
                timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
                files_text += f'<p id="timed">{timeq}</p><li><a href="../../inform/habr/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[3]} [{q[2]}]<p></li>\n'

 #========================== IT PROG =====================================================================
    # Читаем названия всех файлов в папке, заходим в каждый и забираем информацию
    file_names_in_dir2 = os.listdir(path="inform/itprog/pages/")
    f2 = []
    count2 = 1
    size_file2 = 0

    for q in file_names_in_dir2:
        if q.find('.html') != -1:
            oscall('cls', 'clear')
            print(f' {cyell}Into: IT-prog NEWS.html{cnone}')
            print(f' {cyell}Status:{cnone} {count2}/{len(file_names_in_dir2)}')
            print(f' {cyell}Now:{cnone} {q}')
            with open(f'inform/itprog/pages/{q}', 'r', encoding='utf-8') as filer: content = filer.read()
            soup = BeautifulSoup(content, 'html.parser')
            descr = soup.findAll("meta", {"property": "og:description"})
            size_file2 += os.path.getsize(f"inform/itprog/pages/{q}")

            f2.append((int(os.path.getctime(f'inform/itprog/pages/{q}')), f'{q[:-5]}', f'{descr[0].get("content")}'))
            count2 += 1
    f2.sort(reverse = True)

    files_text_itprog = ""
    timeq = f''
    for q in f2: 
        if timeq == '': 
            timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
            files_text_itprog += f'<p id="timed">{timeq}<p><li><a href="../../inform/itprog/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'
        else:
            if timeq == datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y"): 
                files_text_itprog += f'<li><a href="../../inform/itprog/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'
            else:
                timeq = ''
                timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
                files_text_itprog += f'<p id="timed">{timeq}</p><li><a href="../../inform/itprog/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'

 #========================== SOF =====================================================================
    # Читаем названия всех файлов в папке, заходим в каждый и забираем информацию
    file_names_in_dir3 = os.listdir(path="inform/SOF/pages/")
    f3 = []
    count3 = 1
    size_file3 = 0

    for q in file_names_in_dir3:
        if q.find('.html') != -1:
            oscall('cls', 'clear')
            print(f' {cyell}Into: STACK OVERFLOW NEWS.html{cnone}')
            print(f' {cyell}Status:{cnone} {count3}/{len(file_names_in_dir3)}')
            print(f' {cyell}Now:{cnone} {q}')
            with open(f'inform/SOF/pages/{q}', 'r', encoding='utf-8') as filer: content = filer.read()
            soup = BeautifulSoup(content, 'html.parser')
            descr = soup.findAll("meta", {"property": "og:description"}) # - краткое описание статьи
            size_file3 += os.path.getsize(f"inform/SOF/pages/{q}")
            f3.append((int(os.path.getctime(f'inform/SOF/pages/{q}')), f'{q[:-5]}', f'{descr[0].get("content")}'))
            count3 += 1
    f3.sort(reverse = True)

    files_text_sof = ""
    timeq = f''
    for q in f3: 
        if timeq == '': 
            timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
            files_text_sof += f'<p id="timed">{timeq}<p><li><a href="../../inform/SOF/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'
        else:
            if timeq == datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y"): 
                files_text_sof += f'<li><a href="../../inform/SOF/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'
            else:
                timeq = ''
                timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
                files_text_sof += f'<p id="timed">{timeq}</p><li><a href="../../inform/SOF/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'
 
 #========================== ANOTHER (downloader/pages) =====================================================================
    # Читаем названия всех файлов в папке, заходим в каждый и забираем информацию
    file_names_in_dirA = os.listdir(path="downloader/pages/")
    fA = []
    countA = 1
    size_fileA = 0

    for q in file_names_in_dirA:
        if q.find('.html') != -1:
            oscall('cls', 'clear')
            print(f' {cyell}Into: Another.html{cnone}')
            print(f' {cyell}Status:{cnone} {countA}/{len(file_names_in_dirA)}')
            print(f' {cyell}Now:{cnone} {q}')
            with open(f'downloader/pages/{q}', 'r', encoding='utf-8') as filer: content = filer.read()
            soup = BeautifulSoup(content, 'html.parser')
            descr = soup.findAll('body')
            descr = descr[0].text[len(descr[0].text)//3:(len(descr[0].text)//3)+300]
            size_fileA += os.path.getsize(f"downloader/pages/{q}")

            fA.append((int(os.path.getctime(f'downloader/pages/{q}')), f'{q[:-5]}', f'{descr}...'))
            countA += 1
    fA.sort(reverse = True)

    files_text_A = ""
    timeq = f''
    for q in fA: 
        if timeq == '': 
            timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
            files_text_A += f'<p id="timed">{timeq}</p><li><a href="../../downloader/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'
        else:
            if timeq == datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y"): 
                files_text_A += f'<li><a href="../../downloader/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'
            else:
                timeq = ''
                timeq += datetime.datetime.fromtimestamp(q[0]).strftime("%d.%m.%Y")
                files_text_A += f'<p id="timed">{timeq}</p><li><a href="../../downloader/pages/{q[1]}.html" target="_blank"><p id="ttle">{q[1]}</p></a><br><p id="descr">{q[2]}<p></li>\n'

 #========================== WEATHER (inform/weather/last.html) =====================================================================
    # Читаем названия всех файлов в папке, заходим в каждый и забираем информацию
    path_w = "inform/weather/weather.html"
    oscall('cls', 'clear')
    print(f' {cyell}Into: weather.html{cnone}')
    print(f' {cyell}Now:{cnone} {path_w}')

    with open(f'{path_w}', 'r', encoding='utf-8') as filerq: fax = filerq.read()
    weather = BeautifulSoup(fax, 'html.parser')

 #========================== MAKE PAGE =====================================================================

    text = f"""
<!doctype html>
 <html>
    <head>
        <meta charset = "utf-8">
        <link href="style.css" rel="stylesheet" type="text/css" />
        <title>My Site</title>
    </head>
        
        <body> 

                {weather}

                <p id='zag_habr'>&nbsp;&nbsp; Habr ({len(f)})</p>
                <ul id='ul_habr'>
                    {files_text}
                </ul>            

                <p id='zag_itprog'>&nbsp;&nbsp; IT-prog ({len(f2)})</p>
                <ul id='ul_itprog'>
                    {files_text_itprog}
                </ul>   

                <p id='zag_another'>&nbsp;&nbsp; Another ({len(fA)})</p>
                <ul id='ul_another'>
                    {files_text_A}
                </ul>  

                <p id='zag_sof'>&nbsp;&nbsp; SOF:RU ({len(f3)})</p>
                <ul id='ul_sof'>
                    {files_text_sof}
                </ul> 

        </body>
        <script type='text/javascript' src='script.js'></script>
    
 </html>"""
    

    with open('utilities/web_page/index.html', 'w', encoding = 'utf-8') as fe: fe.write(text)
    oscall('start utilities/web_page/index.html','')
    return "Data is loaded; page is maked"