from lxml import html
from openpyxl.styles import Font
from time import sleep
from openpyxl.drawing.image import Image as Im
from PIL import Image
import requests, openpyxl, urllib.request, PIL, os, logging
from bs4 import BeautifulSoup

def GetURLS():
    """Asks the user for URLs"""
    urls = []
    print("Paste as many url's as you like, when you are done, simply press 'enter'.")

    while True:
        url = input(': ')
        if url == '':
            break
        else:
            urls.append(url)

    return urls

def decorator_function(function):
    logging.basicConfig(filename='aliexpressBot.log', level=logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info('{} - {} {}'.format(function.__name__, str(count).zfill(2), image))
        return function(*args, **kwargs)

    return wrapper


@decorator_function
def GetBiggestImage(filename, count):
    """Prints the resolution of the images, and saves it if bigger than 75 there is only one"""
    with open(filename, 'rb') as img:
        #Height of image (in 2 bytes) is at 164th positioin
        img.seek(163)

        # read the 2 byte
        a = img.read(2)

        #calculate height
        height = (a[0] << 8) + a[1]

        # next 2 bytes is width
        a = img.read(2)

        #calculate width
        width = (a[0] << 8) + a[1]

    print(count, 'The resolution of the image is ',width,'x',height)

    if width != 50 and height != 50:
        # resize image
        sleep(2)
        picture = PIL.Image.open(path)
        picture = picture.resize((200, 200), PIL.Image.ANTIALIAS)
        picture.save(path, quality=95, optimize=True)

        count += 1
    else:
        logging.info('img is too small, skipping it')
        os.remove(path)

    return count


urls = GetURLS()
print('You entered: {} url(s)'.format(len(urls)))
#print(urls)

count = 0
for url in urls:
    print('Page:', url)
    mess = requests.get(url).content
    root = html.fromstring(mess)

    print(mess)
    exit()

    lst = root.xpath('//img/@src')[1:]

    # We don't want the first picture, so skip it
    for image in lst:


        # We don't want small pictures
        if '50x50' in image:
            continue

        # To avoid "bad url" add https
        if not image.startswith('https'):
            image = 'https:' + image


        #print('here', image)
        ext = image.rsplit('.', 1)[-1]

        path = 'C:\\USERS\\sebastian\\desktop\\temp\\picture{}.{}'.format(count, ext)
        urllib.request.urlretrieve(image, path)


        count = GetBiggestImage(path, count)
        exit()






sleep(2)


wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()
sheet.column_dimensions['A'].width = 30

for i in range(0, count):
    sheet.row_dimensions[i+1].height = 150

    img = Im('C:\\USERS\\sebastian\\desktop\\temp\\picture{}.jpg'.format(i))
    sheet.add_image(img, 'A'+str(i+1))





wb.save('C:\\USERS\\sebastian\\desktop\\AliexpressBot.xlsx')