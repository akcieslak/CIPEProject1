import requests
from bs4 import BeautifulSoup


TOTAL = 9
TAG = "crComments"
temp = []
count = 0
r = open('rate', 'w')


for i in range(1, TOTAL):
    request = requests.get("http://www.ratemyprofessors.com/campusrating/paginatecampusRatings?page="
                           + str(i) + "&sid=1600")


   

    data = BeautifulSoup(request.text, "html.parser")

    comments = data.get_text()

    
    for c in comments:
        temp.append(c)



for line in temp:
    if TAG in line:
        count += 1
        for word in line.split():
            word1 = word.replace('\"', '').replace(TAG, '').replace(":", '')
            r.write(word1 + " ")
        r.write("\n\n")


r.write("count: " + str(count))
r.close()
    
         
