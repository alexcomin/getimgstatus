import os
import re
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
get_xml = os.popen('curl '+url).read()
array_xml = get_xml.split('\n')
url_xml = []
url_img_bad = []
url_img = {}
counter = 0

for i in array_xml:
    i = i.split(" ")
    a = list(filter(bool, map(str.rstrip, i)))
    if re.match('<loc>', a[0]):
        result_url = a[0].replace('<loc>','').replace('</loc>','')
        url_xml.append(result_url)


def test(arg):
    get_page = os.popen('curl '+arg).read()
    array_page = get_page.split('\n')
    for i in array_page:
        if re.search('<img', i):
            i = i.split(' ')
            for index in i:
                if re.search('src=', index):
                    new_string = index.replace('"','').replace('src=','')
                    image_format = new_string.split('.')
                    if image_format[len(image_format) -1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
                        if not re.match('http', new_string):
                            if host+new_string not in url_img:
                                url_img[host+new_string] = [arg]
                            else:
                                url_img[host+new_string].append(arg)
                        else:
                            if new_string not in url_img:
                                url_img[new_string] = [arg]
                            else:
                                url_img[new_string].append(arg)
                                
    
for i in url_xml:
    sleep(0.2)
    test(i)
    counter += 1
    print("Страниц просканировано", counter, "из", len(url_xml))
    
print('\nПодождите, идет проверка всех найденых изображений. Это может занять некоторое время')

for img in url_img:
    response = os.popen('curl -Is \''+img+'\' | head -1').read().split(' ')
    if len(response) < 2:
        print('Что то не так с изображением, проверьте страницы', img, url_img[img])
        continue
    else: 
        if response[1] != '200' and response[1] != '301':
            print(img, response[1])
            for page in url_img[img]:
                if page not in url_img_bad:
                    url_img_bad.append(page)

time_now = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S");
print('\nСтраницы\n'+'\n'.join(url_img_bad), "\n"+time_start+"\n"+time_now)