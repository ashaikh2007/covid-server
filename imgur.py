import pyimgur

key = 'c59267d98c1002f'
path = 'bordy.jpg'
im = pyimgur.Imgur(key)
uploaded_image = im.upload_image(path, title="Uploaded with PyImgur")
print(uploaded_image.link)