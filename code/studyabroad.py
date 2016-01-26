"""
scrap usf related comments from StudyAbroad101
"""

from bs4 import BeautifulSoup
import requests

URL = "http://www.studyabroad101.com"
FILE = open('studyabroad', 'w')

count = 0

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

        FILE.write("\n\n")

FILE.write("The count is: " + str(count))
FILE.close()
