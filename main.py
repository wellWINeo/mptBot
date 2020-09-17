import bs4
import requests

class mptPage:
    page = ""

    groups09_02_01 = {
        "Э-1-17" : "specRaspadfee2051545f62df0f88505ac8f0682"
    }

    groups09_02_02 = None
    groups09_02_03 = None
    groups09_02_04 = None
    groups09_02_05 = None
    groups09_02_06 = None
    groups09_02_07 = {
        "П50-2-19" : "specRasp7dc1be19b61fe30104b8c13952e2e8f2"
    }
    groups10_02_03 = None
    groups10_02_05 = None
    groups40_02_01 = None
    groups1 = None


    groups = {
        "09.02.01" : {
            "divId" : "speca19dced47c9224424b0ac966f5fa147c",
            "groupsList" : groups09_02_01
        },
        "09.02.02" : {
            "divId" : "spec278dff28f9f8331e6aa7a977e9def941",
            "groupsList" : groups09_02_02
        },
        "09.02.03" : {
            "divId" : "speca19f2e7a69c0c4b50866f3fbcff83a73",
            "groupsList" : groups09_02_03
        },
        "09.02.04" : { 
            "divid" : "spec6a8424929b16ee75085830c77022cdbf",
            "groupslist" : groups09_02_04
        },
        "09.02.05" : {
            "divId" : "speca43f8d8437b13281f50038a0cb195696",
            "groupsList" : groups09_02_05
        },
        "09.02.06" : {
            "divid" : "speca8def7fcfc1932705d763fc48b81c9e8",
            "groupslist" : groups09_02_06
        },
        "09.02.07" : {
            "divid" : "specf7d56bc1e8c0415bc1a88b8bf4982a61",
            "groupsList" : groups09_02_07
        },
        "10.02.03" : { 
            "divId" : "spec3b4bef2daf9a2b4e38c3044ce1dae3a9",
            "groupsList" : groups10_02_03
        }, 
        "10.02.05" : {
            "divId" : "spece163b71104f4296c734f51fb8b8c3d2a",
            "groupsList" : groups10_02_05
        },
        "40.02.01" : {
            "divId" : "specbabe789cf6617aaccbf20389e8dfbd32",
            "groupsList" : groups40_02_01
        },
        "1" : {
            "divId" : "spece13a3927293dba1001e09b3a971215c3",
            "groupsList" : groups1
        }
    }
    
    def __init__(self): 
        self.page = requests.get("https://mpt.ru/studentu/raspisanie-zanyatiy/") 
        self.page = bs4.BeautifulSoup(self.page.text, "html.parser")   
    
    
    def getWeekCount(self): 
        return self.page.body.main.find("span", class_ = "label label-info")


    def naviToGroup(self, group):
        divs = self.page.body.main.find_all("div", {"class" : "tab-pane"})
        group = "Группа " + group
        for div in divs:
            if div.find("h3").text == group:
                return div
        return None


    def _checkTHead(self, point):
        try:
            if point.thead.th.h4.text != None:
                return True
        except:
            return False


    def getSheduleByDay(self, group, targetDay):
        tmp = []
        dayNum = 0
        bodies = self.naviToGroup(group).find_all("tr")
        for i in range(0, len(bodies) - 1):
            if dayNum == targetDay:
                while True:
                    tmp.append(bodies[i].text)
                    i+= 1
                    if i >= len(bodies) or self._checkTHead(bodies[i]):
                        tmp.pop(0)
                        return tmp
            else:
                if self._checkTHead(bodies[i]):
                    dayNum+= 1


    def getHeader(self, branch, group, day):
        #response = self.page.body.main.find(id=self.groups[branch]["groupsList"][group])
        response = self.naviToGroup(group)
        return response.find_all("thead")[day].h4.text 


if __name__ == "__main__":
    mpt = mptPage()
    #print(mpt.groups["09.02.07"]["groupsList"]["П50-2-19"])
    print(mpt.getSheduleByDay("П50-2-19", 5))
    
