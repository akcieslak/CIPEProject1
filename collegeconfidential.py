"""
scrap usf related comments from College Confidential
"""

from bs4 import BeautifulSoup
import requests

TOTAL = 8
FILE = open('cconfidential', 'w')

i = 1
count = 0

while i <= TOTAL:
    response = requests.get("http://talk.collegeconfidential.com/university-san" +
                            "-francisco/p" + str(i) + "/")
    data = BeautifulSoup(response.content)


    for page in data.find_all("a", class_="Title"):
        link = page['href']


        pageResponse = requests.get(link)
        pageData= BeautifulSoup(pageResponse.content)

        for review in pageData.find_all("div", {"class":"Message"}):
            count += 1
            FILE.write(str(count) + ". ")
            FILE.write(review.get_text().encode('utf-8'))
            FILE.write("\n\n")

    i += 1

FILE.write("The count is: " + str(count))
FILE.close()

    
    
           
