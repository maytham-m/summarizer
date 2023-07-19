import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
import PySimpleGUI as sg

url = "https://api.meaningcloud.com/summarization-1.0"




while True:

    layout = [[sg.Text('File to be summarised', size =(18, 1)), sg.Input(key='_FILES_'), sg.FilesBrowse()],
            [sg.Text('Number of sentences', size =(18, 1)), sg.InputText()],
            [sg.OK(), sg.Cancel()]]
    
    window = sg.Window('Text Summarizer', layout)
    event, values = window.read()
    window.close()

    if event == sg.WIN_CLOSED or event == "Cancel":
        window.close()
        quit()

    print(values['_FILES_'].split(';')[0])

    print(values)


    data = {
        "key" : "7dfc1112b15480bff0e1a99a6532bb97", 
        "sentences": values[0]
    }

    files={'doc': open(values['_FILES_'].split(';')[0],'rb')}

    resp = requests.post(url, files = files, data= data)

    print(resp.status_code)
    print(resp.json())

    #Save each file with timestamp
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    f = open("/Users/maytham/Desktop/summary_{}.txt".format(current_time), "w")
    response = resp.json()
    f.write(response['summary'])
    f.close()


    layout = [[sg.Text('File written with the following summary:')],       
                    [sg.Multiline(response['summary'], disabled = True, size=(80, 25))],  
                    [sg.Button("Restart"), sg.Cancel()]]      

    window = sg.Window('Summary', layout)    
    event, values = window.read()  

    window.close()
    
    if event == sg.WIN_CLOSED or event == "Cancel":
        quit()
