from bs4 import BeautifulSoup
from tqdm import *

import requests, bs4, wget, os
# openpyxl

#if os.path.isfile('music.html'):
#    print('!!!!!')
#exit(0)
html_main = open('music.html', 'r', encoding='utf-8').read()
bs = BeautifulSoup(html_main, 'html.parser')
tracks = bs.select('.d-track.typo-track.d-track_selectable')

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
session = requests.Session()


for tr in tqdm(tracks):
    tr_name = tr.select('.d-track__name')[0].get('title').replace(', ',' ')
    tr_artist = tr.select('.d-track__artists')[0].text
    if tr_artist.count(',') > 0:
        tr_artist = tr_artist.split(', ')[0]
    tr_txt = tr_name +'+'+tr_artist
    tr_txt = tr_txt.replace('\'','')
    tr_txt = tr_txt.replace('(', '')
    tr_txt = tr_txt.replace(')', '')
    tr_txt = tr_txt.replace(':', '')
    tr_txt = tr_txt.replace('«', '')
    tr_txt = tr_txt.replace('»', '')
    tr_txt = tr_txt.replace('/', '')
    tr_txt = tr_txt.replace('1964', '')
    tr_txt = tr_txt.replace('из фильма', '')
    tr_txt = tr_txt.replace('Remastered', '')
    tr_txt = tr_txt.replace('L***', '')
    tr_txt = tr_txt.replace('Хищные птицы Потрясающая история Харли Квинн', '')
    url = tr_txt.replace(' ', '+')



    url = 'https://ruo.hotmo.org/search?q=' + url
    #print(url)

    s0 = session.get(url, headers=headers)
    b = bs4.BeautifulSoup(s0.text, "html.parser")
    #print(b)
    mp3_url = b.select('.track__download-btn')
    #print(len(mp3_url))
    if len(mp3_url) > 0:
        mp3_link = mp3_url[0].get('href')
        mp3_name = mp3_link.split('/')[-1]
        if not os.path.isfile(mp3_name):
            print('Скачиваем!',mp3_name)
            filename = wget.download(mp3_link)
    else:
        print('Не найдено!',url)

