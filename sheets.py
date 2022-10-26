import googleapiclient.discovery
import httplib2
import re
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

from config import credentials_file, sheet_id

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, ['https://spreadsheets.google.com/feeds',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)


def searcher_video(url):
    req= requests.get(url)
    soup=BeautifulSoup(req.text, "html.parser")
    search=soup.find_all("script")
    key='"videoId":"'
    data=re.findall(key+r"([^*]{11})",str(search))
    return data
def links():
    b=[]
    url = "https://www.youtube.com/playlist?list=PLDyJYA6aTY1lPWXBPk0gw6gR8fEtPDGKa"
    vid = searcher_video(url)
    vid=vid[::3]
    vid=vid[:-1]
    for i in vid:
        b.append("https://www.youtube.com/watch?v="+i)
    return b
body={
    "valueInputOption":"USER_ENTERED",
    "data":[
        {"range":"A1:A23",
        "majorDimension":"COLUMNS",
        "values":[links()]
        },
        {"range":"B1:B3",
        "majorDimension":"COLUMNS",
        "values":[["https://pythonworld.ru/samouchitel-python","https://www.onlinegdb.com/online_python_compiler"
         ]     ] }
    ]
}
def Update():
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=sheet_id,
        body=body
         ).execute()
    return (values)

def data_video():
    values=Update()
    values=service.spreadsheets().values().batchGet(
        spreadsheetId=sheet_id,
        ranges="A1:A30"
         ).execute()
    return values

def data_more():
    values = Update()
    values = service.spreadsheets().values().batchGet(
        spreadsheetId=sheet_id,
        ranges="B1:B30"
    ).execute()
    return values


def output_V():
    a=[]
    dic=data_video()
    for key, value in dic.items():
        if 'valueRanges' in key:
            vid_dic=value
            for j in vid_dic:
               for k, v in j.items():
                   if 'values' in k:
                       link=v
                       for i in link:
                           for s in i:
                               a.append(s)
    return a
def output_M():
    a=[]
    dic=data_more()
    for key, value in dic.items():
        if 'valueRanges' in key:
            vid_dic=value
            for j in vid_dic:
               for k, v in j.items():
                   if 'values' in k:
                       link=v
                       for i in link:
                           for s in i:
                               a.append(s)
    return a
