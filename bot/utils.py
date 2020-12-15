import bot.core as core
import bot.markup as markup
import bot.user as users
import datetime
import logging
import mptParser.mptShedule
import telebot
import time

#----------
# Init some vars
#----------
mpt = mptParser.mptShedule.mptPage()


#----------
# Main funcs
# for message
# answering
#----------

def wait_group_choose(msg, groups):
    core.tg_bot.send_message(msg.chat.id, "Выберите группу: ",
                            reply_markup=markup.item_chooser_keyboard(mpt, groups))

def group_choosed(msg):
    core.tg_bot.send_message(msg.chat.id, "Отлично! Группа выбрана и сохранена",
                            reply_markup=telebot.types.ReplyKeyboardRemove())

def shedule_date(msg):
    logging.debug("Shedule handling date")
    core.tg_bot.send_message(msg.chat.id, "Выберите на какой срок: ", 
                            reply_markup=markup.choose_shedule_date())

def shedule_handler(call):
    logging.debug("Shedule end handler")

    cur_user = core.db.get_user(call.from_user.id)
    
    week_num = mpt.getWeekCount()
    text = f"{week_num}: "
   
    if cur_user != None:
        if call.data != "cb_week":
            
            if call.data == "cb_today":
                core.tg_bot.answer_callback_query(call.id, "Расписание на сегодня")
                day_num = datetime.datetime.today()
            elif call.data == "cb_tomorrow":
                core.tg_bot.answer_callback_query(call.id, "Расписание на завтра")
                day_num = datetime.datetime.today() + datetime.timedelta(days=1)
            
            shedule_tree = mpt.getSheduleByDay(cur_user.group, day_num.isoweekday())
            text += f"{mpt.getHeader(cur_user.group, day_num.isoweekday())}\n{day_num.date()} \n"
            text += "------------" + "\n"

            if shedule_tree != None:
                for i in shedule_tree:
                    if len(i[1]) == 1:
                        text += f"[{i[0][0]}] {i[1][0]}, {i[2][0]}\n"
                    else:
                        text += f"[{i[0][0]}] {i[1][0]}/{i[1][1]}, {i[2][0]}/" \
                                f"{i[2][1]}\n"

            else:
                text += "Предметов не найдено!"
            core.tg_bot.send_message(call.message.chat.id, text=text)

        else:
            core.tg_bot.answer_callback_query(call.id, "Расписание на неделю")
            core.tg_bot.send_message(call.message.chat.id, "Номер недели - " \
                                                        f"{mpt.getWeekCount()}")
            for d in range(1, 6):
                shedule_tree = mpt.getSheduleByDay(cur_user.group, d)

                if shedule_tree != None:
                    text = f"{mpt.getHeader(cur_user.group, d)}\n"
                    text += f"---------------\n"
                    
                    for i in shedule_tree:
                        if len(i[1]) == 1:
                            text += f"[{i[0][0]}] {i[1][0]}, {i[2][0]}\n"
                        else:
                            text += f"[{i[0][0]}] {i[1][0]}/{i[1][1]}, {i[2][0]}/" \
                                    f"{i[2][1]}\n"

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
        changes_tree = mpt.getChangesByDay(cur_user.group)
        
        if len(changes_tree) != 0:
            text += f"Группа: {cur_user.group}\n"

            for lesson in changes_tree:
                text += f"[{lesson[0]}]\n"
                text += f"  Заменяется: {lesson[1]}\n"
                text += f"  На что: {lesson[2]}\n"
                text += f"  Добавлено: {lesson[3]}\n"
                text += "---\n"
        else:
            text += f"На сегодня замен для групы {cur_user.group} не найдено!"
    else:
        text += "Сперва необходимо выполнить  \"/start\" и выбрать группу"
    
    core.tg_bot.send_message(msg.chat.id, text=text)
