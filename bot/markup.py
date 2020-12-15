from telebot import types

def item_chooser_keyboard(mpt, items):
    # groups = mpt.get_groups_by_dir(direction)
    markup = types.ReplyKeyboardMarkup(row_width=3)
    
    for i in range(0, len(items) - len(items) % 3, 3):
        markup.row(
                types.KeyboardButton(items[i]),
                types.KeyboardButton(items[i+1]),
                types.KeyboardButton(items[i+2]))
    mod = len(items) % 3

    if mod == 2:
        markup.row( 
            types.KeyboardButton(items[len(items)-2]),
            types.KeyboardButton(items[len(items)-1]))
    elif mod == 1:
        markup.row(types.KeyboardButton(items[len(items)-1]))
    
    return markup

def group_choose_keyboard(a, b):
    pass

def choose_shedule_date():
    markup = types.InlineKeyboardMarkup(row_width=3)

    markup.add(
            types.InlineKeyboardButton("На сегодня", callback_data="cb_today"),
            types.InlineKeyboardButton("На завтра", callback_data="cb_tomorrow"),
            types.InlineKeyboardButton("На неделю", callback_data="cb_week"))
    
    return markup


def direction_choose_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    
    # row 1
    button91 = types.KeyboardButton("09.02.01")
    button92 = types.KeyboardButton("09.02.02")
    
    # row 2
    button93 = types.KeyboardButton("09.02.03")
    button94 = types.KeyboardButton("09.02.04")
    
    # row 3
    button95 = types.KeyboardButton("09.02.05") 
    button96 = types.KeyboardButton("09.02.06")
    
    # row 4
    button97 = types.KeyboardButton("09.02.07")
    button13 = types.KeyboardButton("10.02.03")
    
    # row 5
    button15 = types.KeyboardButton("10.02.05")
    button41 = types.KeyboardButton("40.02.01")

    # row 6 
    button1st = types.KeyboardButton("Отделение первого курса")

    # building markup
    markup.row(button91, button92)
    markup.row(button93, button94)
    markup.row(button95, button96)
    markup.row(button97, button13)
    markup.row(button15, button41)
    markup.row(button1st)

    return markup
