from another_modules import *
from inform_check_news import *
from inform_weather import *
from downloader_pages import *
from downloader_files import *
from utilities_make_web import *
from finance_portfolio import *
from utilities_sender import *
from utilities_load_info import *
from utilities_site_headers import *
from utilities_merge_pdf import *

global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

# User Input Menu
def UIM(status_message = ""):
    #input('убрать хрефы в везер > допиливать везер > мутить отправку файлом')
    # clear screen
    oscall('cls', 'clear')

    # print menu text and get usr inp
    menu_text()
    if status_message == "": user_input = input(f"{cyell}\n  Type number of program (or 911)\n  >>> {cnone}")
    elif status_message == None: user_input = input(f"{cyell}\n  >>> Ooops! None response\n  >>> {cnone}")
    else: user_input = input(f'\n  {cyell}{str(status_message)}\n  >>> {cnone}')

    # about info (about/about.html)
    if user_input == "?" or user_input == ",":
        oscall('start about\\about.html','')
        UIM("Thank you for reading. Have fun.")
    
    # logs def (another_modules.py)
    elif user_input == "0":
        UIM(clear_logs())
        
    # open log file
    elif user_input == "00":
        oscall('start C:\\fProgramms\\fArcticGate\\another_logs.log', '')
        UIM('Log file is open')

    # get weather (inform_weather.py)
    elif user_input == "1":
        UIM(weather())

    # check news (inform_check_news.py)
    elif user_input == "2":
        UIM(inform_check_news())

    # file downloader (downloader_files.py)
    elif user_input == "3":
        UIM(downloader_files())

    # open files-folder
    elif user_input == "33":
        oscall('start C:\\fProgramms\\fArcticGate\\downloader\\files', '')
        UIM('Files-folder is open')

    # pages downloader (downloader_pages.py)
    elif user_input == "4":
        UIM(downloader_pages())

    # my portfolio (finance_portfolio.py)
    elif user_input == "5":
        UIM(finance_portfolio())

    # open folder with config
    elif user_input == "55":
        oscall('start C:\\fProgramms\\fArcticGate\\finance\\users', '')
        UIM('Folder with configs is open')

    # one price (finance_portfolio.py >> one_price())
    elif user_input == "6":
        UIM(one_price()) 

    # make local web page (inform_check_news.py >> make_web())
    elif user_input == "7":
        UIM(make_web(0, '', 0))

    # open local web page
    elif user_input == "77":
        oscall('start C:\\fProgramms\\fArcticGate\\utilities\\web_page\\index.html', '')
        UIM('Local web page is open')

    # load site headers (utilities_site_headers.py)
    elif user_input == "8":
        UIM(utilities_site_headers())

    # merge pdf files (utilities_merge_pdf.py)
    elif user_input == "9":
        UIM(utilities_merge_pdf())

    # open pdf folder 
    elif user_input == "99":
        oscall('start C:\\fProgramms\\fArcticGate\\utilities\\merge', '')
        UIM('Local web page is open')

    # load info (utilities_load_info.py)
    elif user_input == "10":
        UIM(utilities_load_info())

    # send info (utilities_sender.py)
    elif user_input == "11":
        UIM(utilities_sender())

    # fast comands (another_modules.py >> )
    elif user_input == "911":
        UIM(fast_comands())

    # fast comands (another_modules.py >> )
    elif user_input == "exit": pass

    else: UIM("Unknown response")

UIM()