"""
scrap usf related comments from indeed.com
"""

from bs4 import BeautifulSoup
import requests

TOTAL = 20
INCREMENT = 20
FILE = open('indeed', 'w')

i = 0
count = 0

while i <= TOTAL:
    response = requests.get("http://www.indeed.com/cmp/University-of-SAN-" +
                            "Francisco/reviews?fcountry=US&start=" + str(i))
    data = BeautifulSoup(response.content, "html.parser")

    for page in data.find_all("div", {"class" : "review_content"}):
        count += 1
        FILE.write(str(count) + ". ")
        for cons in page.find_all("div", {"class" : "review_cons"}):
            FILE.write(cons.get_text().encode('utf-8'))
            FILE.write("\n")
        for pros in page.find_all("div", {"class" : "review_pros"}):
            FILE.write(pros.get_text().encode('utf-8'))
            FILE.write("\n")
        for review in page.find_all("div", {"class" : "description"}):
            FILE.write(review.get_text().encode('utf-8'))
            FILE.write("\n")
        FILE.write("\n\n")

    i += INCREMENT

FILE.write("The count is: " + str(count))
FILE.close()
            
