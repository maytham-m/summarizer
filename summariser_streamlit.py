import streamlit as st

import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime

####################### PDF word count stuff ###############################

import os
import sys
import re
import time
import PyPDF2

def getPageCount(pdf_file):

	pdfFileObj = open(pdf_file, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pages = pdfReader.numPages
	return pages

def extractData(pdf_file, page):

	pdfFileObj = open(pdf_file, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pageObj = pdfReader.getPage(page)
	data = pageObj.extractText()
	return data

def getWordCount(data):

	data=data.split()
	return len(data)

def pdf_count(pdfFile):
	#if len(sys.argv)!=2:
	#	print('command usage: python word_count.py FileName')
	#	exit(1)
	#else:
	#	pdfFile = sys.argv[1]
	
		# check if the specified file exists or not
		try:
			if os.path.exists(pdfFile):
				print("file found!")
		except OSError as err:
			print(err.reason)
			exit(1)


		# get the word count in the pdf file
		totalWords = 0
		numPages = getPageCount(pdfFile)
		for i in range(numPages):
			text = extractData(pdfFile, i)
			totalWords+=getWordCount(text)
		time.sleep(1)

		return (totalWords)

###########################################################################


url = "https://api.meaningcloud.com/summarization-1.0"


st.title('Summariser')
text_file = st.file_uploader("Pick a file")
number = st.slider("Pick a number", 0, 100)

data = {
    "key" : "7dfc1112b15480bff0e1a99a6532bb97", 
    "sentences": number
}

if st.button('Run'):

    st.text('Success!!')
    print(text_file.name)
    files = {'doc': open(text_file.name,'rb')}
    resp = requests.post(url, files = files, data= data)
    response = resp.json()
    st.write(response['summary'])
    

    #Calculate percentage reduced
    if text_file.name[-3:] == 'txt':
        file = open(text_file.name, "rt")
        data = file.read()
        words_original = data.split()
    #elif text_file.name[-3:] == 'pdf':
    #    words_original = pdf_count(text_file.name)


    words_reduced = response['summary'].split()

    

    percentage_val = '{:.2f}%'.format((len(words_reduced)/len(words_original)) * 100 )

    st.text('Reduced to {} of the original text'.format(percentage_val))


    print(resp.status_code)
    print(resp.json())

    



    #Save each file with timestamp
    #now = datetime.now()
    #current_time = now.strftime("%H_%M_%S")
    #f = open("/Users/maytham/Desktop/summary_{}.txt".format(current_time), "w")
    #f.write(response['summary'])
    #f.close()
