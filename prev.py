from flask import Flask, send_file, redirect
from datetime import datetime
from PIL import Image
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from waitress import serve
import re, convertapi, os, smtplib, ssl, functions, telnyx, time

os.environ['TZ'] = 'UTC+5'
time.tzset()
print(datetime.now())


def mail(email):
    year = functions.getYear()
    montho = functions.getMonth()
    dato = functions.getDate()
    subject = montho + ' ' + dato + ', ' + year
    sender_email = "throwway7892@gmail.com"
    receiver_email = email
    password = "sunwing.CA1"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    filename = "s1.png"

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    print("mailed")


def imageGrab():
    year = functions.getYear()
    montho = functions.getMonth()
    dato = functions.getDate()
    timo = functions.getTime()

    with open("approved.html", 'r') as file:
        #global dato, montho, year, timo
        r = file.read()
        rr = re.sub('zaTimeo', 'from ' + timo + ' to 11:59 p.m.', r)
        rrr = re.sub('zaDato', 'Valid ' + montho + ' ' + dato + ', ' + year,
                     rr)
    with open('approved2.html', 'w') as file2:
        file2.write('')
        file2.write(rrr)

    convertapi.api_secret = 'H3rZS0ogbFnNtuwd'
    result = convertapi.convert('png', {'File': 'approved2.html'})
    result.file.save('s.png')

    im = Image.open('s.png')
    im_crop = im.crop((0, 0, 375, 825))
    im_crop.save('s1.png', quality=100)

    im = Image.open('s.png')
    im_crop = im.crop((0, 0, 850, 850))
    im_crop.save('s2.png', quality=100)

    if os.path.getsize('s1.png') < 25000:  #checks if image was properly grabbed.
        imageGrab()
        print('Image size ' + str(os.path.getsize('s1.png')))
        print("restarting image grab")
    else:
        print("Grabbed correctly")
        print('Image size ' + str(os.path.getsize('s1.png')))
    print("image made")


def webGrab():
    year = functions.getYear()
    montho = functions.getMonth()
    dato = functions.getDate()
    timo = functions.getTime()

    with open("index.html", 'r') as file:
        #global dato, montho, year, timo
        r = file.read()
        rr = re.sub('zaTimeo', 'from ' + timo + ' to 11:59 p.m.', r)
        rrr = re.sub('zaDato', 'Valid ' + montho + ' ' + dato + ', ' + year,
                     rr)
    with open('index2.html', 'w') as file2:
        file2.write('')
        file2.write(rrr)
    print('index created at ' + timo + ' ' + montho + ' ' + dato + ', ' + year)


def sendMessage(number):
    year = functions.getYear()
    montho = functions.getMonth()
    dato = functions.getDate()

    telnyx.api_key = 'KEY017E6B39B625DAF8218E086497C0B3DE_bJnhMhd3tOmWoR4QrDG810'

    mms = telnyx.Message.create(
        from_='+16062129753',
        to='+1' + number,
        text=montho + ' ' + dato + ', ' + year,
        media_urls=['https://covid-screener.bobsirmani.repl.co/image'])
    print(f'messaged {number}')


app = Flask(__name__)

@app.route('/')
def redir():
    return redirect('/school-screening/approved')


@app.route('/school-screening/approved')
def index():
    return send_file('index2.html')


@app.route('/screen')  #where all functions are
def screen():
    try:
      imageGrab()
    except:
      imageGrab()
    #sendMessage('3658883872')
    try:
      mail("almujtabadika@gmail.com")
      mail("hasanjalal@gmail.com")
      mail('ashaikh3008@gmail.com')
    except:
      mail("almujtabadika@gmail.com")
      mail("hasanjalal@gmail.com")
      mail('ashaikh3008@gmail.com')

    return ''


@app.route('/web')
def web():
    webGrab()
    return ''

@app.route('/image')
def image():
    return send_file('s1.png')

@app.route('/image2')
def image1():
    return send_file('s2.png')


serve(app, host='0.0.0.0', port=80)
