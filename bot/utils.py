import bot.core as core
import bot.db
import bot.markup as markup
import bot.user as user
import telebot
import mptParser.mptShedule
import datetime
import logging


#----------
# Init some vars
#----------
mpt = mptParser.mptShedule.mptPage()
users = bot.db.load()


#----------
# Main funcs
# for message
# answering
#----------
def recognize_user(id_):
    for user in users:
        return user
    return False

def is_msg_answer(message):
    user = recognize_user(message.from_user.id)
    if user and len(user.group) < 2:
        return True
    return False

def wait_group_choose(msg):
    core.tg_bot.send_message(msg.chat.id, "Выберите группу: ",
                            reply_markup=markup.group_choose_keyboard(mpt, msg.text))

def group_choosed(msg):
    core.tg_bot.send_message(msg.chat.id, "Отлично! Группа выбрана и сохранена",
                            reply_markup=telebot.types.ReplyKeyboardRemove())

def shedule_date(msg):
    logging.debug("Shedule handling date")
    core.tg_bot.send_message(msg.chat.id, "Выберите на какой срок: ", 
                            reply_markup=markup.choose_shedule_date())

def shedule_handler(call):
    logging.debug("Shedule end handler")
    text = ""
    cur_user = recognize_user(call.from_user.id)

    if cur_user: 
        
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
                    text += f"[{i[0]}] {i[1]}, {i[2]}\n"
            else:
                text += "На сегодня предметов не найдено!"
            core.tg_bot.send_message(call.message.chat.id, text=text)

        else:
            core.tg_bot.answer_callback_query(call.id, "Расписание на неделю")
            for d in range(1, 6):
                shedule_tree = mpt.getSheduleByDay(cur_user.group, d)

                if shedule_tree != None:
                    text += f"Day: {d}\n"
                    text += f"---------------\n"
                    
                    for i in shedule_tree:
                        text +=f"[{i[0]} {i[1]}, {i[2]}]\n"
                else:
                    text += "Предметы не найдены!"
                core.tg_bot.send_message(cur_user.group, text=text)

    else:
        core.tg_bot.send_message(call.message.chat.id, 
                                "Сперва необходимо выполнить  \"/start\" и выбрать группу")


def changes_handler(msg):
    logging.debug("Changes handler") 
    cur_user = recognize_user(msg.from_user.id)
    text = ""
    
    if cur_user:
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
