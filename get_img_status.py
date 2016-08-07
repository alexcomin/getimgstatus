import requests
import re
from lxml.html import parse
from time import sleep
from datetime import datetime

time_start = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S");
url = input('Вставьте адрес карты сайта .xml \n')
url = url.split('.')

if url[len(url) -1] != 'xml':
    url = '.'.join(url[:-1])
else:
    url = '.'.join(url)
    
host = "/".join(url.split('/')[:-1])
url_xml = []
url_img_bad = []
url_img = {}
counter = 0

get_xml = parse(url).getroot()
links_obj = get_xml.cssselect("loc")

for link in links_obj:
        url_xml.append(link.text)


def parse_page(url):
    get_page = parse(url).getroot()
    image_obj = get_page.cssselect("img")
    for image in image_obj:
        new_string = image.get('src')
        image_format = image.get('src').split('.')
        if image_format[len(image_format) -1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            if not re.match('http', new_string):
                if host+new_string not in url_img:
                    url_img[host+new_string] = [url]
                else:
                    url_img[host+new_string].append(url)
            else:
                if new_string not in url_img:
                    url_img[new_string] = [url]
                else:
                    url_img[new_string].append(url)
                                
for url in url_xml:
    sleep(0.2)
    parse_page(url)
    counter += 1
    print("Страниц просканировано", counter, "из", len(url_xml))
    
print('\nПодождите, идет проверка всех найденых изображений. Это может занять некоторое время')

for img in url_img:
    try:
        response = requests.get(img).status_code
    except requests.ConnectionError:
        response = 0
    if response == 0:
        print(img, 'Не удается получить доступ к сайту')
        for page in url_img[img]:
            if page not in url_img_bad:
                url_img_bad.append(page)
    else:
        if response != 200 and response != 301:
            print(img, response)
            for page in url_img[img]:
                if page not in url_img_bad:
                    url_img_bad.append(page)

time_now = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S");
print('\nНайденные страницы\n'+'\n'.join(url_img_bad), "\nНачало\n"+time_start+"\nКонец\n"+time_now)