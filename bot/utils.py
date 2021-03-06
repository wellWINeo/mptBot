import bot.core as core
import bot.markup as markup
import bot.user as users
import datetime
import logging
import mptParser.schedule
import mptParser.types as types
import telebot
import time

# ----------
# Init some vars
# ----------
mpt = mptParser.schedule.mptPage()


# ----------
# Main funcs
# for message
# answering
# ----------

def week_odd_handler(week_num: mptParser.types.WeekNum) -> str:
    if week_num == types.WeekNum.NotFound: return "Неизвестно"
    elif week_num == types.WeekNum.Znam: return "Знаменатель"
    elif week_num == types.WeekNum.Chisl: return "Числитель" 

def wait_group_choose(msg, groups):
    core.tg_bot.send_message(msg.chat.id, "Выберите группу: ",
                            reply_markup=markup.item_chooser_keyboard(mpt, groups))


def group_choosed(msg):
    core.tg_bot.send_message(msg.chat.id, "Отлично! Группа выбрана и сохранена",
                            reply_markup=telebot.types.ReplyKeyboardRemove())


def schedule_date(msg):
    logging.debug("Schedule handling date")
    core.tg_bot.send_message(msg.chat.id, "Выберите на какой срок: ",
                            reply_markup=markup.choose_schedule_date())


def schedule_handler(call):
    logging.debug("Schedule end handler")
    cur_user = core.db.get_user(call.from_user.id)
    text = f"{week_odd_handler(mpt.get_week_count())}: "
   
    if cur_user != None:
        if call.data != "cb_week":
            
            if call.data == "cb_today":
                core.tg_bot.answer_callback_query(call.id, "Расписание на сегодня")
                day_num = datetime.datetime.today()

            elif call.data == "cb_tomorrow":
                if 0 <= datetime.datetime.now().time().hour <= 4:
                    core.tg_bot.send_message(call.message.chat.id, 
                                            "Предупреждение: уже за полночь, возможно "\
                                            "ты хотел просмотреть расписание на Сегодня?")

                core.tg_bot.answer_callback_query(call.id, "Расписание на завтра")
                day_num = datetime.datetime.today() + datetime.timedelta(days=1)
            
            day_schedule = mpt.get_schedule_by_day(cur_user.group, day_num.isoweekday())
            text += f"{mpt.get_header(cur_user.group, day_num.isoweekday())}\n{day_num.date()} \n"
            text += "------------" + "\n"

            if len(day_schedule) != 0:
                for i in day_schedule:
                    if i.is_dynamic:
                        # output format:
                        #               [num] lesson-name, teacher (Ч) \n
                        #                     lesson-name, teacher (З) \n
                        text += f"[{i.num}] {i.name[0]}, {i.teacher[0]} (Ч)\n"
                        text += f"{i.name[1]}, {i.teacher[1]} (З)\n"
                    else:
                        text += f"[{i.num}] {i.name}, {i.teacher}\n"
            else:
                text += "Предметов не найдено!"
            core.tg_bot.send_message(call.message.chat.id, text=text)

        else:
            core.tg_bot.answer_callback_query(call.id, "Расписание на неделю")
            core.tg_bot.send_message(call.message.chat.id, "Номер недели - "\
                                    f"{week_odd_handler(mpt.get_week_count())}")
            for d in range(1, 7):
                day_schedule = mpt.get_schedule_by_day(cur_user.group, d)

                if len(day_schedule) != 0:
                    text = f"{mpt.get_header(cur_user.group, d)}\n"
                    text += f"---------------\n"


                    for i in day_schedule:
                        if i.is_dynamic:
                            # output format:
                            #               [num] lesson-name, teacher (Ч) \n
                            #                     lesson-name, teacher (З) \n
                            text += f"[{i.num}] {i.name[0]}, {i.teacher[0]} (Ч)\n"
                            text += f"{i.name[1]}, {i.teacher[1]} (З)\n"
                        else:
                            text += f"[{i.num}] {i.name}, {i.teacher}\n"

                else:
                    text += "Предметы не найдены!"
                core.tg_bot.send_message(call.message.chat.id, text=text)
                time.sleep(0.25)
    
        if cur_user.status == users.status.ANON:
            core.db.del_user(cur_user.user_id)
        
        elif cur_user.status == users.status.ANOTHER:
            cur_user.status = users.status.COMPLETE
            cur_user.group = cur_user.comm
            cur_user.comm = str()
    
    else:
        core.tg_bot.send_message(call.message.chat.id, "Сперва необходимо " \
                                                       "выполнить  \"/start\" " \
                                                       "и выбрать группу")


def changes_handler(msg):
    logging.debug("Changes handler") 
    cur_user = core.db.get_user(msg.from_user.id)
    text = ""
    
    if cur_user != None:
        day_changes = mpt.get_changes(cur_user.group)
        
        if len(day_changes) != 0:
            text += f"Группа: {cur_user.group}\n"

            for ch in day_changes:
                text += f"[{ch.num}]\n"
                text += f"  Заменяется: {ch.replace_from}\n"
                text += f"  На что: {ch.replace_to}\n"
                text += f"  Добавлено: {ch.time}\n"
                text += "---\n"
        else:
            text += f"На сегодня замен для группы {cur_user.group} не найдено!"
    else:
        text += "Сперва необходимо выполнить  \"/start\" и выбрать группу"
    
    core.tg_bot.send_message(msg.chat.id, text=text)
