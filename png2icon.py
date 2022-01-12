from PIL import Image
filen = r'logo.png'
img = Image.open(filen)
img.save('logo.ico',format = 'ICO', sizes=[(32,32)])