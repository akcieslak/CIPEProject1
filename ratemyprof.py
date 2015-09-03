"""
test comment
"""

import json
import requests
import ssl
from bs4 import BeautifulSoup


amount = 9
f = open('draft', 'w')

count = 0

for i in range(1, amount):
    request = requests.get("http://www.ratemyprofessors.com/campusrating/paginatecampusRatings?page="
                           + str(i) + "&sid=1600")


   

    data = BeautifulSoup(request.text, "html.parser")

    comments = data.get_text()

    
    for c in comments:
        f.write(c)


f.close()

d = open('draft', 'r')
r = open('rate', 'w')
for line in d:
    if "crComments" in line:
        count += 1
        for word in line.split():
            word1 = word.replace('\"', '')
            word2 = word1.replace("crComments", '')
            word3 = word2.replace(":", '')
            r.write(word3 + " ")
        r.write("\n\n")

##    elif ": " in line:
##        for word in line.split():
##            word1 = word.replace('"', "")
##            word2 = word1.replace(":", ",")
##            r.write(word2)




r.write("count: " + str(count))
d.close()
r.close()
    
         
