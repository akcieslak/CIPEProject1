"""
scrape usf related comments from ratemyprofessors.com
"""
import requests

AMOUNT = 9

FILE = open('rate', 'w')
count = 0


for i in range(1, AMOUNT):
    request = requests.get("http://www.ratemyprofessors.com/campusrating/pag" +
                           "inatecampusRatings?page=" + str(i) + "&sid=1600")

    dic = request.json()
    for entry in dic['ratings']:
        count += 1
        FILE.write(str(count) + ". ")
        FILE.write(entry['crComments'])
        FILE.write("\n\n")


FILE.write("The count is: " + str(count))
FILE.close
