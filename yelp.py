import requests
from bs4 import BeautifulSoup

f = open('yelp', 'w')

i = 0

count = 0
while i <= 80:
    request = requests.get("http://www.yelp.com/biz/university-of-san-francisco"
                           +"-san-francisco?start=" + str(i))
    data = BeautifulSoup(request.text, "html.parser")
    for review in data.find_all("p", {"itemprop" : "description"}):
        try:
            count += 1
            f.write(str(count) + ".")
            f.write(review.get_text())
            f.write("\n\n")
        except UnicodeEncodeError:
            f.write("\n\n")
            print "There was a UnicodeEncodeError"
            pass

    i += 40
    print i

f.write("The count is:" + str(count))
f.close()
