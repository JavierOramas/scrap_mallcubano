import requests
from bs4 import BeautifulSoup
import re
import csv

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def dump_data(data:dict):
    csv_cols = data[0].keys()
    csv_file = 'mallcubano.csv'
    
    
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_cols)
        writer.writeheader()
        for d in data:
            writer.writerow(d)
    # except IOError:
    #     print("I/O error")

url = 'https://www.mallcubano.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
payload = {
    'query':'test'
}

response = requests.get(url, data=payload, headers=headers, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

links = soup.find_all('a', {"class":"nav-item nav-link"})

final_data = []
for i in links:
    response = requests.get(i['href'], data=payload, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_next = soup.find('a', {'class':'next i-next'}) 
    count = 1
    while(page_next != None):
        count += 1
        response = requests.get(page_next['href'], data=payload, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_next = soup.find('a', {'class':'next i-next'}) 
        print(f"\n\npage {count}\n\n")
        items = soup.find_all('a', {"class":"product-image"})
        cat = cleanhtml(str(soup.find('title')))
        for j in items:
            data = {}
            item_response = requests.get(j['href'], data=payload, headers=headers, verify=False)
            soup = BeautifulSoup(item_response.text, 'html.parser')    

            data['name'] = cleanhtml(str(soup.find('div', {'class':'product-name'})))
            data['cattegory'] = cat
            data['description'] = cleanhtml(str(soup.find('div', {'class':'short-description'})))
            data['price'] = cleanhtml(str(soup.find('span',{'class':'price'})))
            data['extras'] = cleanhtml(str(soup.findAll('div', {'class':'box-collateral'})))
            final_data.append(data)
    

dump_data(final_data)