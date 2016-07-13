import os
import re

# get_xml = os.popen('curl http://aleksandr-komin.oml.ru/sitemap.701385.xml').read()
# array_xml = get_xml.split('\n')

# url_xml = {}

# for i in array_xml:
# 	i = i.split(" ")
# 	a = list(filter(bool, map(str.rstrip, i)))
# 	if re.match('<loc>', a[0]):
# 		result_url = a[0].replace('<loc>','').replace('</loc>','')
# 		url_xml[result_url] = []

# print(url_xml)

a = ['http://aleksandr-komin.oml.ru/oplata-i-dostavka', 'http://aleksandr-komin.oml.ru/magazin/folder/mebel']

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
                    if image_format[len(image_format) -1] in ['jpg', 'jpeg', 'png']:
                        if not re.match('http', new_string):
                            print('http://aleksandr-komin.oml.ru'+new_string)
                        else:
                            print(new_string)
                            
for i in a:
    test(i)