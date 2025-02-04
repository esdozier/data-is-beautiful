from bs4 import BeautifulSoup
import requests


print('Welcome to request.get.https.urlhtml v1.0')
#Version 1.0#

print('Enter in a http(s):// URL you want to extract HTML data from:')
url1 = input()
#This is where the user inputs their request#

r=requests.get(url1)
data=r.text
soup=BeautifulSoup(data)
print(soup)
#Data Extraction of HTML data from webpage#

if('https.html.txt==true'):
    with open('https.html.txt', 'a', encoding='utf-8') as f:
        f.write(str(soup))
elif():
    with open('https.html.txt', 'x') as f:
        f.close()
    with open('https.html.txt', 'a' , encoding='utf-8') as f:
        f.write(str(soup))
#Writing data extraction to txt document for readability enhancement#
