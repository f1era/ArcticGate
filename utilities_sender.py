import json, time, datetime, os, requests, telebot

from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer
from another_modules import data_config

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

def utilities_sender():

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

    print(f'\n {cyell}What we will send?{cnone}')
    print(f'  0. Go back')
    print(f'  1. Portfolio data send')
    print(f'  2. Send another text')
    print(f'  3. Send weather file')
    usi = input(f" {cyell}>>>{cnone} ")
    if usi == "1": return read_ab('telegram')
    elif usi == "2": return read_ab('another')
    elif usi == "3": return read_ab('weather_file')
    else: return 'Go back'

def read_ab(service):

    oscall('cls', 'clear')
    file_names_in_dir = os.listdir(path="finance/users/")
    abonents = []

    print(f'\n {cyell}Find {service} users:{cnone}')

    if service == 'telegram' or service == 'another' or service == 'weather_file':
        for q in file_names_in_dir:
            if q.find('PORTFOLIO@') != -1 and q.endswith('.json'): 
                with open(f"finance/users/{q}", "r") as read_file: data = json.load(read_file)
                if data["TLGID"] != 0: abonents.append(q)

    print('  0. Send to all users') 
    for q in range(len(abonents)): print(f'  {q+1}. {abonents[q][abonents[q].find("@"):-5]}')
    print('  Or type id') 
    user_input = int(input(f'\n {cyell}Send to >>{cnone} '))
    if user_input == 0: 
        if service == 'telegram' or service == 'another': return make_text(service, abonents)
    else: 
        if user_input > 10000: return make_text(service, [user_input])
        if service == 'telegram' or service == 'another': return make_text(service, [abonents[user_input-1]])
        elif service == 'weather_file': return sender(0, service, [abonents[user_input-1]], [' '], int(time.time()))
        
def make_text(service, abonent):

    ready_text = []

    if service == 'another':
        oscall('cls', 'clear')
        print(f'\n {cyell}Type text for send:{cnone}')
        usq = input(f'  {cyell}>>>{cnone} ')
        ready_text.append(usq)
        return sender(0, service, abonent, ready_text, int(time.time()))

    for q in abonent:

        with open(f"finance/users/{q}", "r") as read_file: data = json.load(read_file)
        summ = 0
        changes_summ = 0
        send_text = ""

        if service == 'telegram': send_text += f'<b><u>'
        send_text += f'Update for {q[q.find("@")+1:-5]}:'
        if service == 'telegram': send_text += f'</u></b>'
        send_text += f'\n{datetime.datetime.fromtimestamp(data["LASTUPDATE"]).strftime("%d.%m.%Y %H:%M:%S")}\n\n'

        if service == 'telegram': send_text += f'<b><u>'
        send_text += f'Portfolio:'
        if service == 'telegram': send_text += f'</u></b>\n'
        
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

        if service == 'telegram': send_text += f'\n<b><u>'
        send_text += f'Prices:'
        if service == 'telegram': send_text += f'</u></b>\n'

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

        ready_text.append(send_text)
    
    return sender(0, service, abonent, ready_text, int(time.time()))

def sender(retries, service, abonent, ready_text, time_log):

    try:

        oscall('cls', 'clear')

        if len(abonent) == 0: 
            logs_writer(f'Data sended at {int(time.time()) - time_log}s', 'SENDER')
            return f'Data send ({retries} try)'
        else:
            print(f'\n {cyell}Try №{retries+1}{cnone} to send data for {abonent[0][abonent[0].find("@")+1:-5]} ...')
            if service == 'telegram' or service == 'another':
                tlg_token = data_config('TLG_TK')
                send_text = ready_text[0]
                with open(f"finance/users/{abonent[0]}", "r") as read_file: data2 = json.load(read_file)
                abonent_id = data2["TLGID"]
                url = f'http://api.telegram.org/bot{tlg_token}/sendMessage?parse_mode=html&chat_id={abonent_id}&text={send_text}'
                response = requests.get(url)
                data = response.json()
            if service == 'weather_file':
                # Конфиги
                document = open(r'inform/weather/Weather.html', 'rb')
                token = data_config('TLG_TK')
                with open(f"finance/users/{abonent[0]}", "r") as read_file: data2 = json.load(read_file)
                abonent_id = data2["TLGID"]
                # Пишем сообщение
                url = f'http://api.telegram.org/bot{token}/sendMessage?parse_mode=html&chat_id={abonent_id}&text=Weather_for_{abonent[0][abonent[0].find("@")+1:-5]}'
                response = requests.get(url)
                # Отправляем файл
                bot = telebot.TeleBot(token)
                bot.send_document(abonent_id, document)
            del abonent[0]
            del ready_text[0]
            return sender(retries, service, abonent, ready_text, time_log)

    except requests.RequestException as r_err:
        retries += 1
        catch_error('ConnectionError', r_err)
        return sender(retries, service, abonent, ready_text, time_log)
    except Exception as err:
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'



