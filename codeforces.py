from bs4 import BeautifulSoup
import requests
import textwrap
import fileinput
import notify2
import datetime


flag = 0


def fetch_codeforces(flag):
    now = datetime.datetime.now()

    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def convertDate(line):
        date = "" + str(line[4:6]) + "/"
        mon = month.index(line[0:3]) + 1
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

    for line in fileinput.FileInput("codeforcesdata.txt", inplace=1):
        if line.rstrip():
            print(textwrap.dedent(line))

    contest = []
    with open('codeforcesdata.txt', 'r+') as file:
        res = ""
        count = 0
        for line in file:
            if "Name" in line:
                count+=1
                if count==2:
                    break
            if len(line) == 18 and line[3] == "/" and line[6] == "/":
                res += "Start Time: " + str(line)
                contest.append(res)
                res = ""
            elif line == "\n":
                res += ""
            elif len(line) == 1:
                res += str(line)
            else:
                res = str(line)
    print contest
    ICON_PATH = "/home/vish/Downloads/index.png"
    notify2.init("Contest Notifier")
    # create Notification object
    n = notify2.Notification(None, icon=ICON_PATH)
    # set urgency level
    n.set_urgency(notify2.URGENCY_NORMAL)
    # set timeout for a notification
    n.set_timeout(10000)

    def call(contest):
        res = "Current or Upcoming Contest\n"
        for i in range(len(contest)):
            res += contest[i] + "\n"
        return res

    if flag == 1:
        ans = call(contest)
        n.update("CodeForces Contests", ans)
        n.show()
    else:
        ans = contest[0]
        n.update("CodeForces Contests", ans)
        n.show()


if __name__ == "__main__":
    flag = 1
    fetch_codeforces(flag)
