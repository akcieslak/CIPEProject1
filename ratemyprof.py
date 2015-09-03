import requests
from bs4 import BeautifulSoup

AMOUNT = 9
# f = open('draft', 'w')


# count = 0
COMMENTS = []
for i in range(1, AMOUNT):
    request = requests.get("http://www.ratemyprofessors.com/campusrating/pagi" +
                           "natecampusRatings?page=" + str(i) + "&sid=1600")

    dic = request.json()
    for entry in dic['ratings']:
        COMMENTS.append(entry['crComments'])


for comment in COMMENTS:
    print comment
    print '\n'

print len(COMMENTS)
    # data = BeautifulSoup(request.text, "html.parser")

#     comments = data.get_text()

#     for c in comments:
#         f.write(c)


# d = open('draft', 'r')
# r = open('rate', 'w')
# for line in d:
#     if "crComments" in line:
#         count += 1
#         for word in line.split():
#             word1 = word.replace('\"', '')
#             word2 = word1.replace("crComments", '')
#             word3 = word2.replace(":", '')
#             r.write(word3 + " ")
#         r.write("\n\n")



# r.write("count: " + str(count))
# d.close()
# r.close()
#     
