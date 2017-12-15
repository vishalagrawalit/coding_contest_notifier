from bs4 import BeautifulSoup
import requests
import textwrap
import fileinput
import datetime
now = datetime.datetime.now()

month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def convertDate(line):
    date = "" + str(line[4:6]) + "/"
    mon = month.index(line[0:3])+1
    date += str(mon) + "/" + str(line[7:11]) + " " + str(line[12:17]) + ":00"
    return date

url = "http://codeforces.com/contests"
page = requests.get(url).text
soup = BeautifulSoup(page, "html.parser")
data = soup.find_all("table")

file = open("codeforcesdata.txt", "wb")

for link in data:
    file.write(link.text.encode("UTF-8"))

file.close()
print("Yes")

for line in fileinput.FileInput("codeforcesdata.txt",inplace=1):
    if line.rstrip():
        print(textwrap.dedent(line))

contest = []
with open('codeforcesdata.txt', 'r+') as file:
    res = ""
    for line in file:
        if len(line) == 18 and line[3]=="/" and line[6]=="/":
            print(res)
            res += str(line)
            ExpectedDate = convertDate(str(line))
            ExpectedDate = datetime.datetime.strptime(ExpectedDate, "%d/%m/%Y %H:%M:%S")
            if now < ExpectedDate:
                contest.append(res)
                res = ""
            else:
                break
        elif line == "\n":
            res += ""
        elif len(line) == 1:
            res += str(line)
        else:
            res = str(line)




















            
