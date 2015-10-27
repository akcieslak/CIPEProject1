import requests
from bs4 import BeautifulSoup
import re

count = 0
FILE = open('allText', 'w')


"""
scrape usf related comments from ratemyprofessors.com
"""
AMOUNT = 9


for i in range(1, AMOUNT):
    request = requests.get("http://www.ratemyprofessors.com/campusrating/pag" +
                           "inatecampusRatings?page=" + str(count) + "&sid=1600")

    dic = request.json()
    for entry in dic['ratings']:
        count += 1
        FILE.write(str(count) + ". ")
        FILE.write(entry['crComments'])
        FILE.write("\n\n")



"""
scrap usf related comments from Yelp
"""

TOTAL = 80
INCREMENT = 40


i = 0

while i <= TOTAL:
    request = requests.get("http://www.yelp.com/biz/university-of-san-franci" +
                           "sco-san-francisco?start=" + str(i))
    data = BeautifulSoup(request.text, "html.parser")
    for review in data.find_all("p", {"itemprop": "description"}):
        count += 1
        FILE.write(str(count) + ". ")
        FILE.write(review.get_text().encode('utf-8'))
        FILE.write("\n\n")

    i += INCREMENT


"""
scrape usf related comments from gradereports.com
"""

request = requests.get("http://www.gradreports.com/colleges/university-of-sa" +
                       "n-francisco")

data = BeautifulSoup(request.text, "html.parser")

for review in data.find_all("div", {"class": "review_0"}):
    count += 1
    FILE.write(str(count) + ". ")
    FILE.write(review.get_text())
    FILE.write("\n\n")



"""
scrap usf related comments from Cappex
"""

PAGES = 76
INCREMENT = 75
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


"""
scrap usf related comments from vault
"""

TOTAL = 2


i = 1


while i <= TOTAL:
    response = requests.get("http://www.vault.com/school_profiles/undergrad/uni"+
                            "versity-of-san-francisco/student_reviews?pg=" + str(i))
    data = BeautifulSoup(response.content, "html.parser")

    for page in data.find_all("div", {"class" : "column column8 verticalPadding10"}):
        count += 1
        FILE.write(str(count) + ". ")
        for review in page.find_all("p", {"class":"section"}):
            FILE.write(review.get_text())
            FILE.write("\n\n")

    i += 1



"""
scrap usf related comments from StudyAbroad101
"""

URL = "http://www.studyabroad101.com"

response = requests.get("http://www.studyabroad101.com/programs/bca-study-" +
                        "abroad-quito-university-of-san-francisco-de-quito")
data = BeautifulSoup(response.content, "html.parser")

for info in data.find_all("div", {"id" : "view_review_link"}):
    for page in info.find_all("a", {"target" : "_blank"}):
        link = page['href']

        pageResponse = requests.get(URL + link)
        pageData = BeautifulSoup(pageResponse.content, "html.parser")

        count += 1
        FILE.write(str(count) + ". ")
        
        for blackquote in pageData.find_all("blockquote", {"class" : "margin-top"}):
            FILE.write(blackquote.get_text().encode('utf-8'))
        
        for review in pageData.find_all("p", {"class" : None}):
            FILE.write(review.get_text().encode('utf-8'))


"""
scrap usf related comments from indeed.com
"""


TOTAL = 20
INCREMENT = 20

i = 0

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




"""
scrap usf related comments from College Confidential
"""
TOTAL = 8

i = 1

while i <= TOTAL:
    response = requests.get("http://talk.collegeconfidential.com/university-san" +
                            "-francisco/p" + str(i) + "/")
    data = BeautifulSoup(response.content, "html.parser")


    for page in data.find_all("a", class_="Title"):
        link = page['href']


        pageResponse = requests.get(link)
        pageData= BeautifulSoup(pageResponse.content, "html.parser")

        for review in pageData.find_all("div", {"class":"Message"}):
            count += 1
            FILE.write(str(count) + ". ")
            FILE.write(review.get_text().encode('utf-8'))
            FILE.write("\n\n")

    i += 1



FILE.close()


            

































