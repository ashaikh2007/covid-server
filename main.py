from flask import Flask, send_file, redirect
from datetime import datetime
from waitress import serve
import os, functions, time, threading, requests, json, pyimgur

os.environ['TZ'] = 'UTC+5'
time.tzset()
now = datetime.now()
time_ = now.strftime("%H:%M")
print(time_)



app = Flask(__name__)

@app.route('/')
def redir():
    return redirect('/school-screening/approved')


@app.route('/school-screening/approved')
def index():
    return send_file('index2.html')

@app.route('/web')
def web():
    return send_file('approved2.html')

def webRefresh():
    while True:
        while True:
            now = datetime.now()
            seconds = now.strftime("%S")
            if seconds=='00':
                break
            time.sleep(1)
        try:
            functions.webGrab()
        except:
            functions.webGrab()
        time.sleep(10)

def imageRefresh():
    while True:
        while True:
            now = datetime.now()
            time_ = now.strftime("%H:%M")
            if time_=='07:00':
                break
            time.sleep(1)
        try:
            functions.imageGrab()
        except:
            functions.imageGrab()
        time.sleep(120)

def sendMail():
    while True:
        while True:
            now = datetime.now()
            time_ = now.strftime("%H:%M")
            if time_=='07:15':
                break
            time.sleep(1)
        try:
          functions.mail("almujtabadika@gmail.com")
          functions.mail("hasanjalal@gmail.com")
          functions.mail('ashaikh3008@gmail.com')
        except:
          functions.mail("almujtabadika@gmail.com")
          functions.mail("hasanjalal@gmail.com")
          functions.mail('ashaikh3008@gmail.com')
        time.sleep(120)

def insta():
  toke1 = TOKEN
  while True:
      while True:
          now = datetime.now()
          time_ = now.strftime("%H:%M")
          if time_=='07:20':
              break
          time.sleep(1)
      try:
        tempToke = json.loads(requests.get('https://graph.facebook.com/oauth/access_token?client_id=970533190237321&client_secret=a171eadfaae8bbfea6cb1e057a3e7537&grant_type=fb_exchange_token&fb_exchange_token='+toke1))
        toke2 = tempToke['access_token']
        
        key = 'c59267d98c1002f'
        path = 's2.png'
        im = pyimgur.Imgur(key)
        uploaded_image = im.upload_image(path)
        url = uploaded_image.link
        print(f"Image link - {url}")
        time.sleep(10)
        
        year = functions.getYear()
        montho = functions.getMonth()
        dato = functions.getDate()
        cap = montho+' '+dato+', '+year

        getContainer = requests.post(f"https://graph.facebook.com/17841451306738097/media?image_url={url}&caption={cap}&access_token={toke2}")
        idFind = getContainer.content.decode()
        idJson = json.loads(idFind)
        id_ = idJson['id']
        print(f'creation id - {id_}')
        time.sleep(2)

        postImage = requests.post(f"https://graph.facebook.com/17841451306738097/media_publish?creation_id={id_}&access_token={toke2}")
        idPost = postImage.content.decode()
        print(f"posted to insta with id {idPost}")
        toke1 = toke2

      except:
        tempToke = json.loads(requests.get('https://graph.facebook.com/oauth/access_token?client_id=970533190237321&client_secret=a171eadfaae8bbfea6cb1e057a3e7537&grant_type=fb_exchange_token&fb_exchange_token='+toke1))
        toke2 = tempToke['access_token']
        
        key = 'c59267d98c1002f'
        path = 's2.png'
        im = pyimgur.Imgur(key)
        uploaded_image = im.upload_image(path)
        url = uploaded_image.link
        print(f"Image link - {url}")
        time.sleep(10)
        
        year = functions.getYear()
        montho = functions.getMonth()
        dato = functions.getDate()
        cap = montho+' '+dato+', '+year

        getContainer = requests.post(f"https://graph.facebook.com/17841451306738097/media?image_url={url}&caption={cap}&access_token={toke2}")
        idFind = getContainer.content.decode()
        idJson = json.loads(idFind)
        id_ = idJson['id']
        print(f'creation id - {id_}')
        time.sleep(2)

        postImage = requests.post(f"https://graph.facebook.com/17841451306738097/media_publish?creation_id={id_}&access_token={toke2}")
        idPost = postImage.content.decode()
        print(f"posted to insta with id {idPost}")
        toke1 = toke2
      
      time.sleep(120)

threading.Thread(target=webRefresh).start()
threading.Thread(target=imageRefresh).start()
threading.Thread(target=sendMail).start()
threading.Thread(target=insta).start()

serve(app, host='0.0.0.0', port=5000)
