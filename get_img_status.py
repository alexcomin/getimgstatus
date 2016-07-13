import os
import re
from time import sleep

url = input('Вставьте адрес карты сайта .xml \n')
url = url.split('.')

if url[len(url) -1] != 'xml':
    url = '.'.join(url[:-1])
else:
    url = '.'.join(url)
    
host = "/".join(url.split('/')[:-1])
get_xml = os.popen('curl '+url).read()
array_xml = get_xml.split('\n')
url_img = []
url_xml = {}

for i in array_xml:
	i = i.split(" ")
	a = list(filter(bool, map(str.rstrip, i)))
	if re.match('<loc>', a[0]):
		result_url = a[0].replace('<loc>','').replace('</loc>','')
		url_xml[result_url] = []


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
                            url_xml[arg].append(host+new_string)
                        else:
                            url_xml[arg].append(new_string)

for i in url_xml:
    sleep(0.5)
    test(i)
	
for page in url_xml:
    for index in range(len(url_xml[page])):
        response = os.popen('curl -Is '+url_xml[page][index]+' | head -1').read().split(' ')[1]
        if response != '200':
            print("Страница сайта: " + page)
            print('Изображение: ' + url_xml[page][index] + " " + response)
        else:
            continue