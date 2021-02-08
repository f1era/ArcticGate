import os, time, datetime, json, keyboard
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

global cyell, cnone
cyell = '\033[33m'
cblue = '\033[36m'
cnone = '\033[0m'

#======================== SCREEN CLEANER =======================================

def oscall(call, else_call):
    os.system(f'{call}' if os.name == 'nt' else f'{else_call}')

#======================== LOGS WRITER ==========================================

#1 arg = message for logging
#2 arg: 1 - not end file. 0 - end file.
#3 arg: def who call logs_writer

def logs_writer(message, defwhocall):
    
    with open('another_logs.log', 'a', encoding = 'utf-8') as file:
        file.write(f"Caller: {defwhocall}\n")
        file.write(f"Time: {datetime.datetime.now()}\n")
        file.write(f'  >> {message} \n\n')

#========================== URL CUTTER ==========================================

#url_name(url, 0) -- returns url like 'https://www.google.com/login/input'
#url_name(url, 1) -- returns url like 'www.google.com'
#url_name(url, 2) -- returns url like 'google.com'
#url_name(url, 3) -- returns url like 'google'
#url_name(url, 4) -- returns all elements 
#url_name(url, 5) -- returns file_name

def url_cutter(url, val):

    urls_container = ["", "", "", "", ""]

    urls_container[0] = url

    urls_container[1] = url.split('/')[2:3][0]
    if urls_container[1].find("www.") == -1:
        if urls_container[1].find("api.") == -1:
            urls_container[1] = "www." + urls_container[1]

    urls_container[2] = urls_container[1].lstrip("www.")
    urls_container[2] = urls_container[1].lstrip("api.")

    if urls_container[1].find("www.") != -1 or urls_container[1].find("api.") != -1:
        urls_container[3] = urls_container[1].split('.', 2)[1]
    else: urls_container[3] = urls_container[2]

    urls_container[4] = url.split('/')[-1]
    
    if val == 4: return urls_container
    elif val == 5: return urls_container[4]
    elif val == 3: return urls_container[3]
    elif val == 2: return urls_container[2]
    elif val == 1: return urls_container[1]
    elif val == 0: return urls_container[0]
    elif val > 4: return "Unknown arg for url_cutter"
    elif type(val) == "str": return "Unknown arg for url_cutter"

#================================ READ AND CLEAR LOGS ================================

def clear_logs():

    oscall('cls', 'clear')
    f = open('another_logs.log', encoding = 'utf-8')
    s = f.readlines()
    print(f'\n  {cyell}another_logs.log{cnone}:\n')
    for q in range(len(s)):
        print(f'    {s[q]}', end='')

    rew = input(f"\n  {cyell}What we will do?{cnone}\n   1. Clear logs\n   2. Open log file\n   3. Go back\n  {cyell}>>>{cnone} ")
    if rew == "1":
        with open('another_logs.log', 'w') as file:
            file.write("")
        return "Logs are cleared!"
    elif rew == "2": 
        oscall('start another_logs.log', '')
        return clear_logs()
    else: return ""

#red \033[31m
#yellow {cyell} 
#blue 033[34m

# =========== MENU TEXT ==================

def menu_text():

  print(f""" {cyell}
  Arctic Gate v1.0
  * by Python 3.8.5
  * by fiera Korobejnikov{cnone}

       ?. About info
       0. Logs file

    \033[36mInform:{cnone}
       1. Check weather
       2. Check news
      
    \033[36mDownloader:{cnone}
       3. Download files
       4. Download pages       

    \033[36mFinance:{cnone}
       5. My portfolio
       6. Price from TS
      
    \033[36mUtilities:{cnone}
       7. Make local web-page
       8. Load site headers
       9. Merge pdf files 
      10. Load info
      11. Send data""")

#======================== CATH ERROR =======================================

def catch_error(reas, err):
    
    if reas == "ConnectionError":
        print(f'\n\033[31m Connection Error:{cnone}')
        print(f' {err}')
        print(f'\n {cyell}>>>{cnone} Reconnection after 5s...')
        time.sleep(5)
        return
    if reas == "AnotherError":
        print(f'\n\033[31m Authors error:{cnone}')
        print(f' {err}')
        print(f'\n {cyell}>>>{cnone} Go back after 5s...')
        time.sleep(5)
        return 

# =========== DATA CONFIG ===================

def data_config(data):

    with open(f"another_config.json", "r") as r: data_config = json.load(r)

    if data_config[data] != '' and data_config[data] != 0: return data_config[data]
    else: return "no data"

# ======= EDIT URL FOR DOWNLOADER_PAGES ============

def edit_url_pages(errr):
    errr = errr.strip("\n")
    errr = f'{errr}.html'
    errr = errr.replace("https://", "")
    errr = errr.replace("http://", "")

    intab = ':/*"|\?>< '
    trantab = str.maketrans(intab, '_' * len(intab))

    return errr.translate(trantab)

# ========= FAST COMANDS ====================

def fast_comands():

    oscall('cls', 'clear')
    print(f'\n {cyell}U have next scripts{cnone}\n')
    print(f'  1. Load N urls into telegram and download files next')
    print(f'  2. Load all top day news on habr without images')
    print(f'  3. Check Tiksi-weather (rp5) ')
    print(f'  4. Tiksi-weather (rp5) + load top day news (habr) ')
    print(f'  5. Update fiera`s portfolio data and send to fiera ')
    print(f'  6. Update users portfolio data and send to all users ')
    print(f'  7. Tiksi-weather + send to telegram ')

    rew = input(f"\n {cyell}Type number of script for run >>>{cnone} ")
    if rew == '1':
        usi = int(input(f'{cyell}\n Type N >>> {cnone}'))
        script = f'1, 0, enter, 1, enter, 1, enter, {usi}, enter, 1, enter, 1, enter'
        keyboard.press_and_release(script)
    elif rew == '2':
        script = f'2, enter, 1, enter, 2, enter, 2, enter, 0, enter'
        keyboard.press_and_release(script)
    elif rew == '3':
        script = f'1, enter, 2, enter, 1, enter'
        keyboard.press_and_release(script)
    elif rew == '4':
        script = f'9, 1, 1, enter, 3, enter, 9, 1, 1, enter, 2, enter'
        keyboard.press_and_release(script)
    elif rew == '5':
        script = f'5, enter, 1, enter, 1, enter, 1, 1, enter, 1, enter, 1, enter, 1, enter'
        keyboard.press_and_release(script)
    elif rew == '6':
        script = f'5, enter, 0, enter, 1, enter, 1, 1, enter, 1, enter 1, enter 0, enter'
        keyboard.press_and_release(script)
    elif rew == '7':
        script = f'1, enter, 2, enter, 1, enter, 1, 1, enter, 1, enter, 3, enter, 1, enter, e, x, i, t, enter'
        keyboard.press_and_release(script)
    else: return "Unknown response"

