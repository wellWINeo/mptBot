from telebot import types

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



#def group_choose_keyboard(direction):
        

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



