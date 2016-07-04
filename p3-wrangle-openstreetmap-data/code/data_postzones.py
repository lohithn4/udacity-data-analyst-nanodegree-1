# -*- coding: utf-8 -*-

'''
Code adapted from Lesson 2 problem set
'''

import pprint
from bs4 import BeautifulSoup
html_page = "postzones.html"


def extract_postzones(page):
    
    data = {}

    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        
        table = soup.find(id='postzones')
        rows = table.find_all('tr')
        
        for r in rows:
            cols = r.find_all('td')

            zone = cols[0].text
            code = cols[2].text[1:] # removing first char because its a 0
            
            if code in data:
                data[code].append(zone)
            else:
                data[code] = []
                data[code].append(zone)
            
    return data
    
    
if __name__ == '__main__':
    
    data = extract_postzones(html_page)
    pprint.pprint(data)