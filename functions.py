from datetime import datetime
from PIL import Image
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import re, convertapi, os, smtplib, ssl

def getYear():
    now = str(datetime.now()) #yyyy-mm-dd

    yearSlc = slice(0, 4)
    year = now[yearSlc]
    return year


def getMonth():
    now = str(datetime.now()) #yyyy-mm-dd
    monthSlc = slice(5,7)
    montho = now[monthSlc]
    if montho =='01':
        montho = 'January'
    elif montho =='02':
        montho = 'Febuary'
    elif montho =='03':
        montho = 'March'
    elif montho =='04':
        montho = 'April'
    elif montho =='05':
        montho = 'May'
    elif montho =='06':
        montho = 'June'
    elif montho =='07':
        montho = 'July'
    elif montho =='08':
        montho = 'August'
    elif montho =='09':
        montho = 'September'
    elif montho =='10':
        montho = 'October'
    elif montho =='11':
        montho = 'November'
    elif montho =='12':
        montho = 'December'
    
    return montho


def getDate():
    now = str(datetime.now()) #yyyy-mm-dd
    dateSlc = slice(8, 10)
    dato = now[dateSlc]
    if int(dato)<10:
        dato = re.sub('0', '',dato)
    return dato


def getTime():
    now = str(datetime.now()) #yyyy-mm-dd
    timeSlc = slice(11,16)
    timo24 = now[timeSlc]
    convert = datetime.strptime(timo24, "%H:%M")
    timo12 = convert.strftime("%I:%M %p")

    if int(timo12[0:-6])<10:
        i = str(timo12).replace('0','',1) #replace only first 0 in string
        timo12 = i

    if 'PM' in timo12:
        timo = re.sub('PM', 'p.m.', timo12)
    elif 'AM' in timo12:
        timo = re.sub('AM', 'a.m.', timo12)
    return timo

def mail(email): #email image with captions of date 
    year = getYear()
    montho = getMonth()
    dato = getDate()
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


def imageGrab(): #HTML to jpg with proper date
    year =  getYear()
    montho = getMonth()
    dato = getDate()
    
    with open("approved.html", 'r') as file:
        #global dato, montho, year, timo
        r = file.read()
        rr = re.sub('zaTimeo', 'from 7:00 a.m to 11:59 p.m.', r)
        rrr = re.sub('zaDato', 'Valid ' + montho + ' ' + dato + ', ' + year,
                     rr)
    with open('approved2.html', 'w') as file2:
        file2.write('')
        file2.write(rrr)

    convertapi.api_secret = 'gdo6MKEOwB7j1gqR'
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


def webGrab(): #update index.html every minute
    year = getYear()
    montho = getMonth()
    dato = getDate()
    timo = getTime()

    with open("index.html", 'r') as file:
        #global dato, montho, year, timo
        r = file.read()
        rr = re.sub('zaTimeo', 'from ' + timo + ' to 11:59 p.m.', r)
        rrr = re.sub('zaDato', 'Valid ' + montho + ' ' + dato + ', ' + year,
                     rr)
    with open('index2.html', 'w') as file2:
        file2.write('')
        file2.write(rrr)
    #print('index created at ' + timo + ' ' + montho + ' ' + dato + ', ' + year)