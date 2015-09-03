import requests
from bs4 import BeautifulSoup

TOTAL = 80
INCREMENT = 40

f = open('yelp', 'w')

i = 0
count = 0

while i <= TOTAL:
    request = requests.get("http://www.yelp.com/biz/university-of-san-francisco"
                           +"-san-francisco?start=" + str(i))
    data = BeautifulSoup(request.text, "html.parser")
    for review in data.find_all("p", {"itemprop" : "description"}):
        count += 1
        f.write(str(count) + ".")
        f.write(review.get_text().encode('utf-8'))
        f.write("\n\n")

    i += INCREMEMENT
    print i

f.write("The count is:" + str(count))
f.close()
