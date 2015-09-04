"""
scrap usf related comments from Cappex
"""
import requests
from bs4 import BeautifulSoup


FILE = open('cappex', 'w')
PAGES = 76
INCREMENT = 75
count = 0
i = 1;

if (i == 1):
    request = requests.get("http://www.cappex.com/colleges/University-of-" +
                           "San-Francisco/reviews")

data = BeautifulSoup(request.text, "html.parser")


for person in data.find_all("li", {"class" : "reviewDisplay"}):
    count += 1
    FILE.write(str(count) + ". ")
    for review in person.find_all("p", {"class" : "reviewComments"}):
        FILE.write(review.get_text().encode('utf-8'))
        FILE.write("\n\n")

FILE.write("The count is: " + str(count))
FILE.close()           
