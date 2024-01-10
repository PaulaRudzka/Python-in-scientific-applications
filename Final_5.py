import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filename",type=str)  

args=parser.parse_args()

res=requests.get('https://targipracy.org.pl/pracodawca-dla-inzyniera/')

soup = BeautifulSoup(res.text, 'html.parser')
print('halo')

div_companies_rank=soup.find_all('section', {'data-id': '7172a18'})[0] 

div_companies=div_companies_rank.find_all('div', class_='elementor-widget-container')[2:-1]

company=[]
valuenow=[]
for i in range(len(div_companies)):
    name=str(div_companies[i].findAll('span', class_='elementor-title')[0].string)
    name=name.split(". ")[1]
    value = float(div_companies[i].find('div', attrs={'aria-valuenow': True})['aria-valuenow'])

    company.append(name)
    valuenow.append(value)
    

plt.barh(company,valuenow)
plt.gca().invert_yaxis()
plt.show()

ranking=list(zip(company,valuenow))

with open(args.filename+'.json', 'w') as f:
    json.dump(ranking, f, indent=4)

with open(args.filename+'.json', 'r') as f:
    ranking_json = json.load(f)

print(ranking_json)