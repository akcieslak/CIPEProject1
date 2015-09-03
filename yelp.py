"""
scrap usf related comments from Yelp
"""
import requests
from bs4 import BeautifulSoup

TOTAL = 80
INCREMENT = 40

FILE = open('yelp', 'w')

i = 0
count = 0

while i <= TOTAL:
    request = requests.get("http://www.yelp.com/biz/university-of-san-franci" +
                           "sco-san-francisco?start=" + str(i))
    data = BeautifulSoup(request.text, "html.parser")
    for review in data.find_all("p", {"itemprop": "description"}):
        count += 1
        FILE.write(str(count) + ".")
        FILE.write(review.get_text().encode('utf-8'))
        FILE.write("\n\n")

    i += INCREMENT
    print i

FILE.write("The count is:" + str(count))
FILE.close()
