import bs4
import logging
from mptParser import updater
from mptParser import types
import requests
import re
from threading import Thread, RLock

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
    pageShedule: str
    pageChanges: str
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


    def update(self):
        try:
            self.pageShedule = requests.get("https://mpt.ru/studentu/raspisanie-zanyatiy/") 
            self.pageChanges = requests.get("https://mpt.ru/studentu/izmeneniya-v-raspisanii")

            self.pageShedule = bs4.BeautifulSoup(self.pageShedule.text, "html.parser")   
            self.pageChanges = bs4.BeautifulSoup(self.pageChanges.text, "html.parser").body.main

        except:
            logging.error("Connection refused")
            exit



    def getWeekCount(self) -> str:
        """Returns count of current week (числитель/знаменатель) """
        try:
            self.lock.acquire()
            response = self.pageShedule.find("span", class_="label label-danger")
            self.lock.release()
            
            if response != None:
                return response.text
            else:
                response = self.pageShedule.find("span", class_="label label-info")
                if response != None:
                    return response.text
                else:
                    return "¯\\_(ツ)_/¯"

        except AttributeError:
            logging.error("Attribute erro in getWeekCount()")
            return "¯\\_(ツ)_/¯"

    def __tab_num(self, target: str, headers: list):
        for num in range(0, len(headers)):
            if headers[num].a.text == target:
                return num
        return None
    
    def __rm_spaces(self, string: str):
        while "  " in string:
            string = string.replace("  ", " ")[1::]
        string = string[:-1]
        return string

    def get_groups_by_dir(self, direction: str):
        
        self.lock.acquire()
        tabs = self.pageShedule.find_all("ul", {"class" : "nav nav-tabs"})
        self.lock.release()
        num = self.__tab_num(direction, tabs[0].find_all("li"))
        tabs = tabs[1::]
        
        try:
            groups = (list(tabs[num]))[1::2]
        except:
            groups = []

        response = []

        for group in groups:
            tmp = group.a.text
            tmp = self.__rm_spaces(tmp)
            self.__rm_spaces(tmp)
            response.append(tmp)
        return response

    def __naviToGroup(self, group: str):
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
                logging.error("AttributeError in _naviToGroup(), comparison")
        return None


    def __naviToGroupChanges(self, group: str):
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

    def __checkTHead(self, point) -> bool:
        """
        Private method for checking THead, return bool value
        """
        try:
            self.lock.acquire()
            if point.thead.th.h4.text != None:
                return True
        
        except:
            return False
        
        finally:
            self.lock.release()

    
    def getChangesByDay(self, group) -> list:
        """
        Method to get today changes
        ---------------------------
        Params:
            -- group = string wit correct name of group like it type on the site 
        
        ---------------------------
        Returns:
            matrix like this -> [
                                 [lesson_num1, replace-from1, replace-to1, updated-at1],
                                 [lesson_num2, replace-from2, replace-to2, updated-at2],
                                 ...]
        """
        
        try:
            tmp = self.__naviToGroupChanges(group)
        except:
            logging.error("Exception in __naviToGroup")

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



    def getSheduleByDay(self, group, target_day) -> list:
        """
        Method to get the shedule for day by group 
        ---------------------- 
        Params:     
            -- $day = string with correct name of group, like it typed on the site 
            -- $targetDay = number of the day week, starts by 1 
        ---------------------- 
        Returns:
            matrix like this -> [[num1, name1, teacher1], [num2, name2, teacher2] ...]
        """
        
        bodies = resp = list()

        day_num = 0

        try:
            bodies = self.__naviToGroup(group).find_all("tr")
        except:
            logging.error("[Error] in calling __naviToGroup")

        for i in range(0, len(bodies) - 1):
        
            if day_num == target_day:
        
                while True: 
                    lesson = bodies[i].find_all("td")
                    test = self.__parse_lesson(lesson)
                    resp.append(test)
                    i+= 1
                    if i >= len(bodies) or self.__checkTHead(bodies[i]):
                        resp.pop(0)
                        return resp 
            else:
                if self.__checkTHead(bodies[i]):
                    day_num += 1

    def __parse_lesson(self, arr):
        dynamic = False
        num = None
        name = []
        teach = []

        if len(arr) >= 3:
            num = re.sub(" +", " ", arr[0].text)
            if len(arr[1]) > 1:
                dynamic = True

                # numerator (числитель)
                name.append("{0}".format(re.sub(" +", " ",
                        arr[1].find("div", class_="label label-danger").text)))

                teach.append("{0}".format(re.sub(" +", " ",
                        arr[2].find("div", class_="label label-danger").text)))

                # denominator (знаменатель)
                name.append("{0}".format(re.sub(" +", " ",
                        arr[1].find("div", class_="label label-info").text)))
                teach.append("{0}".format(re.sub(" +", " ",
                        arr[2].find("div", class_="label label-info").text)))

            else:
                name = re.sub(" +", " ", arr[1].text)
                teach = re.sub(" +", " ", arr[2].text)

        return types.Lesson(num, name, teach, dynamic)


    def getHeader(self, group, day) -> str:
        """
        Returns string with day of the week name
        ----------------------
        Params:
        group -- string with correct name of group, like it typed on the site
        day   -- number of the day week, starts by 1
        """
        
        # TODO: Make error raising
        try:
            return self.__naviToGroup(group).find_all("thead")[day-1].h4.text
        except: 
            return ""

    def __del__(self):
        self.updateDaemon.join()
