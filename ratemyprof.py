import requests

AMOUNT = 9

f = open('rate', 'w')
count = 0


for i in range(1, AMOUNT):
    request = requests.get("http://www.ratemyprofessors.com/campusrating/pagi" +
                           "natecampusRatings?page=" + str(i) + "&sid=1600")

    dic = request.json()
    for entry in dic['ratings']:
        count += 1
        f.write(str(count) + ".")
        f.write(entry['crComments'])
        f.write("\n\n")


f.write("The count is: " + str(count))
f.close
