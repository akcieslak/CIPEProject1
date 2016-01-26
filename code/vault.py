"""
scrap usf related comments from vault
"""

from bs4 import BeautifulSoup
import requests
import re

TOTAL = 2
FILE = open('vault', 'w')


i = 1
count = 0



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


FILE.write("The count is:" + str(count))
FILE.close()
    
