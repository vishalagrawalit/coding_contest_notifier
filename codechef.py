from bs4 import BeautifulSoup

import requests
import fileinput
import textwrap
import notify2

import datetime
now = datetime.datetime.now()

month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def convertDate(line):
    date = "" + str(line[0:2]) + "/"
    mon = month.index(line[3:6])+1
    date += str(mon) + "/" + str(line[7:11]) + " " + str(line[13:])
    return date


site = "https://www.codechef.com/contests"

page = requests.get(site).text

soup = BeautifulSoup(page,"html.parser")

file = open("parseddata.txt", "wb")

for link in soup.find_all('tbody'):
    file.write(link.text.encode("UTF-8"))

file.close()

for line in fileinput.FileInput("parseddata.txt",inplace=1):
    if line.rstrip():
        print textwrap.dedent(line)

ICON_PATH = "/home/vish/Downloads/index.png"
notify2.init("Contest Notifier")
# create Notification object
n = notify2.Notification(None, icon = ICON_PATH)
# set urgency level
n.set_urgency(notify2.URGENCY_NORMAL)
# set timeout for a notification
n.set_timeout(10000)

present = 0
future = 0
present_contest=[]
future_contest=[]

res = ""
count = 0
with open('parseddata.txt','rw') as file:
    for line in file:
        l = len(line)
        if l == 1:
            count += 1
        elif count == 4:
            count = 0
            res += str(line)
        elif count == 2:
            ExpectedDate = convertDate(str(line))
            ExpectedDate = datetime.datetime.strptime(ExpectedDate, "%d/%m/%Y %H:%M:%S ")
            if now < ExpectedDate:
                future = 1
            else:
                present = 1
            res += str(line)
        elif future == 1:
            res += str(line)
            future_contest.append(res)
            res = ""
            future = 0
        elif present == 1:
            ExpectedDate = convertDate(str(line))
            ExpectedDate = datetime.datetime.strptime(ExpectedDate, "%d/%m/%Y %H:%M:%S ")
            if now > ExpectedDate:
                break
            else:
                res += str(line)
                present_contest.append(res)
                res = ""
                present = 0
        elif l>1:
            res += str(line)


def call(present_contest, future_contest):
    l1, l2 = len(present_contest), len(future_contest)
    ans = ""
    for i in range(l1+l2):
        if i == 5:
            return ans
        elif i == 0:
            ans += "Running Contests:\n"
            ans += present_contest[i] + "\n"
        elif 0 < i < l1:
            ans += present_contest[i] + "\n"
        elif i == l1:
            ans += "Future Contests:\n"
            ans += future_contest[i-l1] + "\n"
        elif l1 < i:
            ans += future_contest[i-l1] + "\n"

    return ans


ans = call(present_contest, future_contest)
n.update("Profile Details", ans)
n.show()
