import bs4
import requests

class mptPage:
    """
    Class for parsing data from mpt.ru

    ----------------------
    Attributes:
    pageShedule -- store the soup of https://mpt.ru/studentu/raspisanie-zanyatiy/
    pageChanges -- store the soup of https://mpt.ru/studentu/izmeneniya-v-raspisanii

    ----------------------
    Methods
    
    getWeekCount(None)
        Return is week odd
    
    getShedyleByDay(group, targetDay)
        Return matrix with shedule of the group by this day

    getHeader(group, day)
        Return name of week's day
    """
    pageShedule = ""
    pageChanges = ""

    
    def __init__(self):
        """
        Constructor for mptPage class

        ----------------------
        Params:
        None
        """ 
        self.pageShedule = requests.get("https://mpt.ru/studentu/raspisanie-zanyatiy/") 
        self.pageChanges = requests.get("https://mpt.ru/studentu/izmeneniya-v-raspisanii")

        self.pageShedule = bs4.BeautifulSoup(self.pageShedule.text, "html.parser")   
        self.pageChanges = bs4.BeautifulSoup(self.pageChanges.text, "html.parser")
    
    def getWeekCount(self):
        """Returns count of current week (числитель/знаменатель) """

        return self.pageShedule.body.main.find("span", class_ = "label label-info")


    def _naviToGroup(self, group):
        """Privete method for navigation in soup to group (for shedule)"""
        divs = self.pageShedule.body.main.find_all("div", {"class" : "tab-pane"})
        group = "Группа " + group
        for div in divs:
            if div.find("h3").text == group:
                return div
        return None


    def _naviToGroupChanges(self, group):
        """Private method for navigation in soup to group (for changes)"""
        
        divs = self.pageChanges.find_all("div", {"class" : "table-responsive"})
        for div in divs:
            if div.caption.b.text == group:
                return div
            else:
                pass
        return None

    def _checkTHead(self, point):
        """Private method for checking THead, return bool value"""
        try:
            if point.thead.th.h4.text != None:
                return True
        except:
            return False


    def getSheduleByDay(self, group, targetDay):
        """Method to get the shedule for day by group
        ----------------------
        Params:
        group     -- string with correct name of group, like it typed on the site
        targetDay -- number of the day week, starts by 1 
        ----------------------
        Returns:
        matrix like this -> [[num1, name1, teacher1], [num2, name2, teacher2] ...]
        """
        
        tmp = []
        dayNum = 0
        bodies = self._naviToGroup(group).find_all("tr")
        for i in range(0, len(bodies) - 1):
            if dayNum == targetDay:
                while True:
                    lesson = bodies[i].find_all("td")
                    tmp.append([])
                    for elem in lesson:
                        tmp[len(tmp) - 1].append(elem.text)
                    i+= 1
                    if i >= len(bodies) or self._checkTHead(bodies[i]):
                        tmp.pop(0)
                        return tmp
            else:
                if self._checkTHead(bodies[i]):
                    dayNum+= 1


    def getHeader(self, group, day):
        """Returns string with day of the week name
        ----------------------
        Params:
        group -- string with correct name of group, like it typed on the site
        day   -- number of the day week, starts by 1"""
        response = self._naviToGroup(group)
        return response.find_all("thead")[day].h4.text 


if __name__ == "__main__":
    mpt = mptPage()
    print(mpt._naviToGroupChanges("П50-2-19")) 