import redis
import logging
import mptParser.types as types
import mptParser.schedule as schedule

# class Wrapper:
#     def __init__(self, _instance):
#         self.instance = _instance
#         self.rd = redis.Redis()
    
#     def get_all(self):
#         for dir in types.Directions:
#             # print(f"{dir}: {self.instance.get_groups_by_dir(dir)}")
#             for group in self.instance.get_groups_by_dir(dir):
#                 day_sched = self.instance.get_schedule_by_day(group, 5)
#                 print(f"{dir} - {group}: ")
#                 for lesson in day_sched:
#                     self.rd.lpush(group, lesson.to_json())
                

#                 print(self.rd.lrange(group, 0, self.rd.llen(group)))

class Wrapper(schedule.mptPage):

    def __init__(self):
        # super.__init__()
        self.rd = redis.Redis()
        self.update()
    
    def update(self):
        try:
            super().update()
        except:
            logging.error("Can't connect to mpt.ru")
            return

        for dir in types.Directions:
            for group in super().get_groups_by_dir(dir):
                day_sched = super().get_schedule_by_day(group, 6)
                for lesson in day_sched:
                    self.rd.lpush(group, lesson.to_json())
        self.week_num = super().get_week_count()


    def get_week_count(self): return self.week_num 


    def get_schedule_by_day(self, group, target_day):
        sched = self.rd.lrange(group, 0, self.rd.llen(group))
        for lesson in sched:
            # print(lesson)
            # print("-----------------------------")
            types.Lesson.from_json(lesson).show()
            
    
    def __del__(self): pass
