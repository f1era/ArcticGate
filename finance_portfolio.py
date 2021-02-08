import json, time, os, datetime, requests
from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

# ======================== СОБИРАЕМ СПИСОК ИМЕЮЩИХСЯ ПОЛЬЗОВАТЕЛЕЙ ===============================
def finance_portfolio():

    oscall('cls', 'clear')
    abonents = []
    start_abon = []

    # Собираем пользователей из папки
    file_names_in_dir = os.listdir(path="finance/users")
    for q in file_names_in_dir: 
        if q.endswith('.json'): abonents.append(q)
    if abonents == []: return 'Have no users'

    # Выводим на экран всех пользователей
    print(f'\n{cyell} Find users:{cnone}')
    print(f'  0. All users')
    for q in range(len(abonents)): print(f'  {q+1}. {abonents[q][abonents[q].find("@"):-5]}')

    # Интересует кто?
    user_input = int(input(f'\n {cyell}Who ur interested?{cnone} >> '))
    if user_input == 0: 
        # Собираем все symbol для каждого пользователя и добавляем в список symbols
        symbols = []
        for q in abonents:
            with open(f"finance/users/{q}", "r") as rd: rdd = json.load(rd)
            for q in rdd["USERPORTFOLIO"]: 
                if q not in symbols: symbols.append(q)        
        oscall('cls', 'clear'); return print_portfolio(abonents, symbols, abonents[:])
    else: 
        # Собираем все symbol для каждого пользователя и добавляем в список symbols
        symbols = []
        with open(f"finance/users/{abonents[user_input-1]}", "r") as rd: rdd = json.load(rd)
        for q in rdd["USERPORTFOLIO"]: 
            if q not in symbols: symbols.append(q)         
        oscall('cls', 'clear'); return print_portfolio([abonents[user_input-1]], symbols, [abonents[user_input-1]])

# ================== ВЫВОД НА ЭКРАН СОХРАНЕННЫХ ЦЕН ДЛЯ ПОЛЬЗОВАТЕЛЯ(-ЛЕЙ) =====================================   

def print_portfolio(abonents, symbols, start_abon):
  
    send_text = ''
    summ = 0
    changes_summ = 0

    # Если запрашиваемые пользователи кончились в списке
    if abonents == []:
        # Что делаем дальше?
        print(f'{cyell}What we will do?{cnone} ')
        user_input2 = input(f' 0. Go back\n 1. Update prices\n{cyell}>>{cnone} ')
        if user_input2 == "1": return update_prices(0, symbols, start_abon, int(time.time()))
        else: return "Go back"

    # Открываем файл пользователя и собираем всю информацию > печать на экран
    with open(f"finance/users/{abonents[0]}", "r") as read_file: data = json.load(read_file)
    send_text += f'{cyell}Update for {abonents[0][abonents[0].find("@"):-5]}{cnone}:\n{datetime.datetime.fromtimestamp(data["LASTUPDATE"]).strftime("%d.%m.%Y %H:%M:%S")}\n\n'
    send_text += f'{cyell}Portfolio:{cnone}\n'
    for q in data["USERPORTFOLIO"]: 
        if data["USERPORTFOLIO"][q]["enum"] != 0:
            if data["USERPORTFOLIO"][q]["val"] == "RUB":
                if q.find(".ME") != -1: send_text += f'{q[:-3]}: '
                elif q.find("RUB=X") != -1: send_text += f'{q[:3]}: '
                else: send_text += f'{q}: '
                send_text += f'{format(data["USERPORTFOLIO"][q]["enum"]*data["USERPORTFOLIO"][q]["price"], "0.0f")}₽ ({data["USERPORTFOLIO"][q]["enum"]} шт.)\n'
                summ += data["USERPORTFOLIO"][q]["enum"]*data["USERPORTFOLIO"][q]["price"]
                changes_summ += data["USERPORTFOLIO"][q]["enum"]*data["USERPORTFOLIO"][q]["change"]
            else: 
                send_text += f'{q}: {format(data["USERPORTFOLIO"][q]["enum"]*data["USERPORTFOLIO"][q]["price"]*data["USERPORTFOLIO"]["USDRUB=X"]["price"], "0.2f")}$ ({data["USERPORTFOLIO"][q]["enum"]} шт.)\n'
                summ += data["USERPORTFOLIO"][q]["enum"]*data["USERPORTFOLIO"][q]["price"]*data["USERPORTFOLIO"]["USDRUB=X"]["price"]
                changes_summ += data["USERPORTFOLIO"][q]["enum"]*data["USERPORTFOLIO"][q]["change"]*data["USERPORTFOLIO"]["USDRUB=X"]["price"]
    send_text += f'Ɵ = {data["STARTBALANCE"]}₽\n'
    percent = ((summ*100)/data["STARTBALANCE"])-100
    send_text += f'∑ = {format(summ, "0.0f")}₽ ({format(percent, "0.2f")}%)\n\
        ({format(summ - data["STARTBALANCE"], "0.2f")}₽)\n'
    send_text += f'\n{cyell}Prices{cnone}:\n'
    for q in data["USERPORTFOLIO"]: 
        if data["USERPORTFOLIO"][q]["val"] == "RUB":
            if q.find(".ME") != -1: send_text += f'{q[:-3]}: '
            elif q.find("RUB=X") != -1: send_text += f'{q[:3]}: '
            else: send_text += f'{q}: '
            if q == "VTBR.ME": send_text += f'{format(data["USERPORTFOLIO"][q]["price"], "0.4f")}₽ ({format(data["USERPORTFOLIO"][q]["change"], "0.4f")}₽)\n'
            else: send_text += f'{format(data["USERPORTFOLIO"][q]["price"], "0.2f")}₽ ({format(data["USERPORTFOLIO"][q]["change"], "0.2f")}₽)\n'
        else: 
            if q == "BZ=F": send_text += f'BRENT: '
            else: send_text += f'{q}: '
            send_text += f'{format(data["USERPORTFOLIO"][q]["price"], "0.2f")}$ ({format(data["USERPORTFOLIO"][q]["change"], "0.2f")}$)\n \
     {format(data["USERPORTFOLIO"][q]["price"]*data["USERPORTFOLIO"]["USDRUB=X"]["price"], "0.2f")}₽\
 ({format(data["USERPORTFOLIO"][q]["change"]*data["USERPORTFOLIO"]["USDRUB=X"]["price"], "0.2f")}₽)\n'
            if q == "BZ=F": send_text += "\n"
    
    # Выводим на экран > запускаем заново
    print(send_text); del abonents[0]
    return print_portfolio(abonents, symbols, start_abon)

# ==================================== ОБНОВЛЯЕМ ЦЕНЫ ДЛЯ ПОЛЬЗОВАТЕЛЯ(-ЛЕЙ) ========================================
def update_prices(retries, symbols, start_abon, time_log):

    try:
        oscall('cls', 'clear')
        # Если тикеры кончились
        if symbols == []:
            for n in start_abon:
                with open(f"finance/users/{n}", "r") as rq: d3 = json.load(rq)
                d3["LASTUPDATE"] = int(time.time())
                with open(f"finance/users/{n}", "w") as w2: json.dump(d3, w2, indent = 4)  
            logs_writer(f'Prices are loaded at {int(time.time()) - time_log}s', 'DOWNLOADER_FILES')
            return 'Prices are loaded'          
        
        # Выводим сколько осталось и что грузим
        print(f"\n {cyell}From:{cnone}")
        for q in start_abon: print(f'  {q}') 
        print(f"\n{cyell} Lost:{cnone} ")
        for e in symbols: print(f'  {e}')
        print(f"\n {cyell}[{symbols[0]}] {cnone}{retries+1} try...")

        url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbols[0]}?modules=price'
        response = requests.get(url)
        data = response.json()

        # Перезаписываем файл согласно обновленной информации
        for n in start_abon:
            with open(f"finance/users/{n}", "r") as rf: d2 = json.load(rf)
            if symbols[0] in d2["USERPORTFOLIO"]:
                d2["USERPORTFOLIO"][symbols[0]]["change"] = data["quoteSummary"]["result"][0]["price"]["regularMarketChange"]["raw"]
                d2["USERPORTFOLIO"][symbols[0]]["price"] = data["quoteSummary"]["result"][0]["price"]["regularMarketPrice"]["raw"]
                with open(f"finance/users/{n}", "w") as wf: 
                    if symbols[0] in d2["USERPORTFOLIO"]: json.dump(d2, wf, indent = 4)

        del symbols[0]
        return update_prices(retries, symbols, start_abon, time_log)

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return update_prices(retries, symbols, start_abon, time_log)
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'

# ==================================== ФУНКЦИЯ ДЛЯ ВЫВОДА ЦЕНЫ ПО ОДНОМУ ТИКЕРУ ========================================
def one_price(retries=0, symbol=''): 
    
    try:

        oscall('cls', 'clear')
        symbol = input(f'\n {cyell}Type symbol ticker{cnone} >>> ')

        print(f"\n {cyell}{str(retries + 1)} try{cnone} >> {symbol} >> Collecting data...")
        url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=price'
        #url = f'https://query1.finance.yahoo.com/v8/finance/chart/{get_val}?period1={int(time.time()) - 345600}&period2={int(time.time())}&interval=1d&includePrePost=False&events=div%2Csplits'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        response = requests.get(url, headers)
        data = response.json()
        print(data)
        input(f'\n {cyell}Data is loaded. Type any for go back >>{cnone} ')
        return "Price is loaded"

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return one_price(retries=retries, symbol=symbol) 
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'