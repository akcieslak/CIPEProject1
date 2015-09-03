import requests
import re

from bs4 import BeautifulSoup
AMOUNT = 5
MAJORS = []
count = 0


FILE = open('studentR', 'w')

##Goes through the root site and pulls down the html
for i in range(1, AMOUNT):
    request = requests.get("http://www.studentsreview.com/gettingin.php3?SH=USF&ST="
                    +"CA&page=" + str(i) +"&d_school=University%20of%20San%20" +
                       "Francisco&specific=grade_academic_gpa")
    data = BeautifulSoup(request.text, "html.parser")

    ##Finds all the links that have d_name=University of San Francisco"
    for href in data.find_all('a'):
        if "d_name=University of San Francisco" in str(href):
            link = href['href']

            if link in MAJORS:
                break
            else:
                MAJORS.append(link)
            
            pageRequest = requests.get(link)
            pageData = BeautifulSoup(pageRequest.text, "html.parser")
            
            for commentHref in pageData.find_all('a'):
                if "/viewprofile" in str(commentHref):
                    commentPage = commentHref['href']
                    commentRequest = requests.get("http://www.studentsreview.com/" + commentPage)
                    commentData = BeautifulSoup(commentRequest.text, "html.parser")
                    
                    #info is each table
                    for info in commentData.findAll("div", {"class" : "leftColumn"}):

                        for review in info.find_all("div",{"class" : "reviewcomment"}):
                            count += 1
                            FILE.write(str(count) + ". ")
                            regex = re.compile("(Major: )([\w+\s\W*]*)(\(This Major's Salary over time\))")
                            edited = regex.sub('', review.get_text())
                                                                         
                            FILE.write(edited)
                            FILE.write("\n\n")

                       
FILE.write("The count is: " + str(count))
FILE.close()                          
                                                

    

