# -*- coding: utf-8 -*-

import PyPDF2
import re



class returMaterias():
    def __init__(self, path_pdf_file):
        self.pdf_file = path_pdf_file
#write a for-loop to open many files -- leave a comment if you'd #like to learn how

#filename = 'matricula_disciplinas_2019.2_turmas_planejadas.pdf' 

#open allows you to read the file
    def get_materias(self):
        pdfFileObj = open(self.pdf_file,'rb')

        #The pdfReader variable is a readable object that will be parsed

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        #discerning the number of pages will allow us to parse through all #the pages

        num_pages = pdfReader.numPages
        count = 0
        text = ""

        #The while loop will read each page
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()

        #This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.

        #if text != "":
        #print(text)

        splitted = re.split('((?:\w|\d){6,}-(?:\w|\d){3,})', text)

        dict_materias = {}

        for x in range(1, len(splitted)-1, 2):
            dict_materias[splitted[x]] = splitted[x+1]
            


        for key, value in dict_materias.items():
            dict_materias[key] = value.replace('\n', ' ')
        return dict_materias

