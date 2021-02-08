from another_modules import oscall
from another_modules import catch_error
from another_modules import logs_writer
from PyPDF2 import PdfFileReader, PdfFileWriter 
import os
global cyell, cnone
cyell = '\033[33m'
cnone = '\033[0m'

def utilities_merge_pdf():

    print(f'hi')
    return pdf_merger()

def pdf_merger():

    def_name = "PDF_MERGER"

    try:

        #step 1: clear screen 
        oscall('cls', 'clear')
        print(f'\n {cyell}Merging{cnone} pdf files...')

        #step 2: open folder with pdf files
        file_names_in_dir = os.listdir(path="utilities/merge")
        file_names_doc = []

        #step 3: get all pdf files > write date in file_names > sorted files
        for i in file_names_in_dir:
            if i.lower().endswith(".pdf") and i != "Merged.pdf":
                file_names_doc.append("utilities/merge/" + i)
        file_names_doc = sorted(file_names_doc)
        len_names_doc = len(file_names_doc)

        #step 4: merge files or call error
        if len_names_doc < 2:
            return "Files not found."
        else:
            paths = file_names_doc    
            pdf_writer = PdfFileWriter()
            for path in paths:
                pdf_reader = PdfFileReader(path)
                for page in range(pdf_reader.getNumPages()):
                    pdf_writer.addPage(pdf_reader.getPage(page))

            with open('utilities/merge/Merged.pdf', 'wb') as out: pdf_writer.write(out)
            oscall('start utilities/merge/Merged.pdf', '')
            return "File is already writen"

    except Exception as err:
        logs_writer(f'Authors error: {err}', 'MERGE_PDF')
        catch_error('AnotherError', err)
        return f'Ooops. Authors error. Sorry for it:\n   \033[31m{err}{cnone}{cyell}'

