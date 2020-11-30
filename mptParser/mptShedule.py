
# base libs
import bs4
import requests
import re
from threading import Thread, RLock

# own libs
from mptParser import updater
from logs import log

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
    lock = RLock() 
    
    def __init__(self):
        """
        Constructor for mptPage class

        ----------------------
        Params:
        None
        """ 
        self.updateDaemon = updater.updaterThread(self, self.lock)
        self.updateDaemon.setDaemon(True)
        
        self.update()
        
        self.updateDaemon.start()

        self.sys_log = log.log("logs/sys_logs.txt")



    def update(self):
        try:
            self.pageShedule = requests.get("https://mpt.ru/studentu/raspisanie-zanyatiy/") 
            self.pageChanges = requests.get("https://mpt.ru/studentu/izmeneniya-v-raspisanii")

            self.pageShedule = bs4.BeautifulSoup(self.pageShedule.text, "html.parser")   
            self.pageChanges = bs4.BeautifulSoup(self.pageChanges.text, "html.parser")
        except:
           self.sys_log.write("[Error] Coonection refused") 
           exit



    def getWeekCount(self):
        """Returns count of current week (числитель/знаменатель) """
        try:
            self.lock.acquire()
            response = self.pageShedule.body.main.find("span", class_ = "label label-info")
            self.lock.release()

            return response

        except AttributeError as err:
            self.sys_log.write("[Error] Atribute error in getWeekCount()")
            return err
    #
    # UNSAFE 
    #
    def __tab_num(self, target, headers):
        for num in range(0, len(headers)):
            if headers[num].a.text == target:
                return num
        return None
    
    # TODO 
    # make spaces deleting via regex
    def __rm_spaces(self, string):
        while "  " in string:
            string = string.replace("  ", " ")[1::]
        string = string[:-1]
        return string

    def get_groups_by_dir(self, direction):
        
        self.lock.acquire()
        tabs = self.pageShedule.find_all("ul", {"class" : "nav nav-tabs"})
        self.lock.release()
        num = self.__tab_num(direction, tabs[0].find_all("li"))
        tabs = tabs[1::]
        
        groups = (list(tabs[num]))[1::2]
        response = []

        for group in groups:
            tmp = group.a.text
            tmp = self.__rm_spaces(tmp)
            tmp = tmp.split(",")

            if len(tmp) == 1:
                self.__rm_spaces(tmp[0])
                response.append(tmp[0])
            elif len(tmp) > 1:
                for elem in tmp:
                    self.__rm_spaces(elem)
                    response.append(elem)
            else:
                pass
        return response
    #
    # /UNSAFE
    #

    def __naviToGroup(self, group):
        """Privete method for navigation in soup to group (for shedule)"""
        
        self.lock.acquire()
        divs = self.pageShedule.body.main.find_all("div", {"class" : "tab-pane"})
        self.lock.release()

        group = "Группа " + group
        for div in divs:
            try:
                if div.find("h3").text == group:
                    return div
            except:
                self.sys_log.write("[error] AttributeError in _naviToGroup(), comparison")
        return None


    def __naviToGroupChanges(self, group):
        """Private method for navigation in soup to group (for changes)"""
        self.lock.acquire()
        divs = self.pageChanges.find_all("div", {"class" : "table-responsive"})
        self.lock.release()

        for div in divs:
            if div.caption.b.text == group:
                    return div
            else:
                pass
        return None

    def __checkTHead(self, point):
        """Private method for checking THead, return bool value"""
        try:
            self.lock.acquire()
            if point.thead.th.h4.text != None:
                return True
        
        except:
            return False
        
        finally:
            self.lock.release()

    
    def getChangesByDay(self, group):

        try:
            tmp = self.__naviToGroupChanges(group)
        except:
            self.sys_log.write("[Error] in __naviToGroupChanges")

        if tmp == None:
            return [] 
        
        tmp = tmp.find_all("tr") 
        
        response = []
         
        for elem in tmp:
            response.append([
                elem.find(class_ = "lesson-number").text,
                elem.find(class_ = "replace-from").text,
                elem.find(class_ = "replace-to").text,
                elem.find(class_ = "updated-at").text
            ])
        return response[1:]



    def getSheduleByDay(self, group, targetDay): 
        """
        Method to get the shedule for day by group 
        ---------------------- 
        Params: group     
            -- string with correct name of group, like it typed on the site targetDay 
            -- number of the day week, starts by 1 
        ---------------------- 
        Returns:
            matrix like this -> [[num1, name1, teacher1], [num2, name2, teacher2] ...]
        """
        
        tmp = []
        dayNum = 0
        bodies = []

        try:
            bodies = self.__naviToGroup(group).find_all("tr")
        except:

            self.sys_log.write("[Error] in calling __naviToGroup")


        for i in range(0, len(bodies) - 1):
        
            if dayNum == targetDay:
        
                while True:
                    lesson = bodies[i].find_all("td")
                    tmp.append([])
        
                    for elem in lesson:
                        append_elem = re.sub(" +", " ", elem.text)
                        tmp[len(tmp) - 1].append(append_elem)
                    i+= 1
        
                    if i >= len(bodies) or self.__checkTHead(bodies[i]):
                        tmp.pop(0)
                        return tmp
        
            else:
        
                if self.__checkTHead(bodies[i]):
                    dayNum+= 1


    def getHeader(self, group, day):
        """Returns string with day of the week name
        ----------------------
        Params:
        group -- string with correct name of group, like it typed on the site
        day   -- number of the day week, starts by 1"""
        response = self.__naviToGroup(group)
        return response.find_all("thead")[day].h4.text 

    def __del__(self):
        self.updateDaemon.join()
        del self.sys_log

if __name__ == "__main__":
    mpt = mptPage()

    print(mpt.getSheduleByDay("П50-2-19", 1))
