import os
import requests
import string
import codecs
from flask import Flask, render_template, request, redirect, url_for
import os
import six.moves.urllib as urllib
import sys
import tarfile
import zipfile
import scipy.misc
import shutil

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from bs4 import BeautifulSoup

from os import path
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def make_wc(text, image):
    stopwords = set(STOPWORDS)

    wc = WordCloud(background_color="white", max_words=2000, mask=image,
               stopwords=stopwords, max_font_size=100, random_state=42)

    wc.generate(text)

    image_colors = ImageColorGenerator(image)

    try:
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")

    except:
        plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('result.jpg')
    shutil.copy('result.jpg','./static')
    os.remove('result.jpg')

d = path.dirname(__file__)

app=Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config["CACHE_TYPE"] = "null"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
	return render_template("upload.html")


@app.route('/upload', methods=["POST"])
def upload():
    file=request.files["file"]
    song = request.form.get('textbox')

    lyrics = ""
    text = ""

    if(len(song) > 0):
        for i in list(range(len(song))):
            if(song[i]==" "):
                song=song.replace(" ","%20")
        url = 'https://music.bugs.co.kr/search/track?q='+song+"'"
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            Find_url = str(soup.find("div",{"id": "DEFAULT0"}).find('input', {'type':'hidden'}).get('value'))
        except AttributeError:
            print('{}는 노래제목이 아닙니다.')
        req = requests.get('https://music.bugs.co.kr/track/'+Find_url+'?wl_ref=list_tr_08_search')
        html = req.text
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        lyrics = str(soup.find_all('xmp'))
        lyrics=lyrics.replace("/","")
        lyrics=lyrics.replace("<xmp>"," ")
        lyrics=lyrics.replace("["," ")
        lyrics=lyrics.replace("]"," ")
        lyrics=lyrics.replace("\r\n", " ")

        text = lyrics
    
    else:
        txtfile=request.files["txtfile"]
        txtfile.save('test/exam.txt')

    file.save('test/image1.png')
    
    #
    if(len(song) > 0):
        print("")
        
    else:
        text = open('test/exam.txt', 'rt', encoding='UTF8').read()
    #
    image_np = np.array(Image.open(path.join(d, 'test/image1.png')))
    #
    make_wc(text, image_np)

    return render_template("complete.html")

if __name__  ==  "__main__":
    app.run(debug=True, use_reloader=True)
