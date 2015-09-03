"""
scrape usf related comments from gradereports.com
"""
import requests
import re
from bs4 import BeautifulSoup

count = 0
FILE = open('gradreport', 'w')

request = requests.get("http://www.gradreports.com/colleges/university-of-san-" +
                       "francisco")

data = BeautifulSoup(request.text, "html.parser")

for review in data.find_all("div", {"class" : "review_0"}):
    count += 1
    FILE.write(str(count) + ". ")
    FILE.write(review.get_text())
    FILE.write("\n\n")

            
FILE.write("The count is: " + str(count))
FILE.close()
