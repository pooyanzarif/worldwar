#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop
from world import tworld
from objects import *
from configuration import *
import urllib3
import os
import json
#-----------------------------------------------------------------------------------------------------------------------
fa={}
force_reply = {'force_reply': True}
nt_force_reply = telepot.namedtuple.ForceReply(**force_reply)
COMMANDS= MENU+WEAPONS
#-----------------------------------------------------------------------------------------------------------------------
# this function send video of war to the user
def sendvideo(user_id):
    p = open(video_directory+'bh.gif', 'rb')
    bot.sendVideo(user_id,p,caption=SCENE_OF_YOUR_WAR)

#-----------------------------------------------------------------------------------------------------------------------
# This function send welcome message to the user
def welcome(user_id, inviter=0):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BTN_CREATE_VILLAGE, callback_data='create=%s'%(inviter) )], #callback_data = command
    ])
    p = open(picture_directory+'worldwar.jpg', 'rb')
    bot.sendPhoto(user_id,p,caption=TITLE)
    sendMessage(user_id, WELCOME_STORY%(inviter), reply_markup=keyboard)

#-----------------------------------------------------------------------------------------------------------------------
# This function creates village and is used one and at the time you join the game
def create(user_id,username='',first_name='',last_name='', inviter=0):

    if world.is_exist(user_id)!=False:  # village has already created!
        sendMessage(user_id, ALREADY_CREATED)
        return False
    result= world.create_village(user_id,username,first_name,last_name, inviter)
    # world.update_all()
    if result:
        p = open(picture_directory + 'village.jpg', 'rb')
        sendMessage(user_id, VILLAGE_CREATED)
        bot.sendPhoto(user_id, p, caption=VILLAGE_CREATED)
        sendMessage(user_id, SENARIO, reply_markup={'keyboard': main_menu(0)})
        print("%s %s %s created successfully!!!"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),first_name,last_name))
        if inviter!=0:
            invite_message = INVITER_INFORM%(first_name,last_name)
            sendMessage(inviter,invite_message)
            sendMessage(ADMIN_USER_ID,invite_message)
        return True
    else:
        print( "%s %s Failed to create!!!!"%(first_name,last_name))
        sendMessage(user_id, u"failed to create!")
        return False

#-----------------------------------------------------------------------------------------------------------------------
# This function shows the main menu of the game
def main_menu(parent=0):
    menu = list(filter(lambda x: x['parent']==parent, MENU))
    menu = list(map(lambda x:x['title'], menu))
    return [menu[:3], menu[3:6], menu[6:9],menu[9:]]

#-----------------------------------------------------------------------------------------------------------------------
# This function shows the inline menu of the game
def command_menu_inline(command):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=DOIT, callback_data='do'+command)]
     ])
    return keyboard

#-----------------------------------------------------------------------------------------------------------------------
# This functions sends admin reply menu to user
def admin_reply_inline(user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ [InlineKeyboardButton(text=MESSAGE, callback_data='doadminreply:' + str(user_id))]  ])
    return keyboard
#-----------------------------------------------------------------------------------------------------------------------
# This function sends attack result menu to user
def attack_rersult_menu_inline(enemy_user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=MESSAGE, callback_data='dopoke:'+str(enemy_user_id))]
    ])
    return keyboard

#-----------------------------------------------------------------------------------------------------------------------
# This function sends attack menu to user
def profile_menu_inline(enemy_user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=MESSAGE, callback_data='dopoke:'+str(enemy_user_id))],
        [InlineKeyboardButton(text=ATTACK, callback_data='doattack:'+str(enemy_user_id))]
    ])
    return keyboard
#-----------------------------------------------------------------------------------------------------------------------
#This function sends expecses to user
def expens(command):
    cost=COSTS.get(command)
    result=EXPENSE+":\n"
    if cost:
        result+= u"{0}{1}:{8}\n{2}{3}:{9}\n{4}{5}:{10}\n{6}{7}:{11}\n".format(GOLDICON,GOLD,WOODICON,WOOD,FOODICON,FOOD,TIMEICON,TIME,cost['gold'],cost['wood'],cost['food'],cost['time'])
    return result
#-----------------------------------------------------------------------------------------------------------------------
# This function sends inline menu to user
def weapon_menu_inline(user_id):
    st = ''
    v = world.find_village(user_id)
    menu = v.menu_weapons()
    for m in menu:
        title = u"{0:<10s}  {1}:{4:>4d}  {2}:{5:>4d}  {3}:{6:>4d}".format(m['title'],GOLDICON,WOODICON,FOODICON,m['cost'].get('gold',0),m['cost'].get('wood',0),m['cost'].get('food',0))
        st += "[InlineKeyboardButton(text='%s', callback_data='%s')]," % (title, 'WEAPON='+str(m['wid']))
    keyboard = "InlineKeyboardMarkup(inline_keyboard=[%s])" % (st)
    return eval(keyboard)

#-----------------------------------------------------------------------------------------------------------------------
# This function sends sell menu to user
def sell_menu_inline():
    menu=[{'text':SELL_WOOD,'callback':'SELL=wood'}, {'text':SELL_FOOD,'callback':'SELL=food'}]
    st=''
    for m in menu:
        st += "[InlineKeyboardButton(text='%s', callback_data='%s')]," % (m['text'], m['callback'])
    keyboard = "InlineKeyboardMarkup(inline_keyboard=[%s])" % (st)
    return eval(keyboard)

#-----------------------------------------------------------------------------------------------------------------------
# This function sends weapons menu to user
def weapon_menu(user_id):
    v = world.find_village(user_id)
    m = v.menu_weapons()
    menu = map(lambda x: x['name'], m)
    menu.append('back')
    return [menu[:3], menu[3:6], menu[6:9],menu[9:]]
#-----------------------------------------------------------------------------------------------------------------------
#This function sends Race menu to user
def race_menu_inline():
    st=''
    for race in RACE:
        st += "[InlineKeyboardButton(text='%s', callback_data='%s')]," % (race, 'RACE='+race)
    keyboard = "InlineKeyboardMarkup(inline_keyboard=[%s])" % (st)
    return eval(keyboard)
#-----------------------------------------------------------------------------------------------------------------------
# This function sends messages back to user
def sendMessage(chat_id, text,
                    parse_mode=None, disable_web_page_preview=None,
                    disable_notification=None, reply_to_message_id=None, reply_markup=None):
    if text!='':
        try:
            bot.sendMessage(chat_id, text,
                    parse_mode, disable_web_page_preview,
                    disable_notification, reply_to_message_id, reply_markup)
        except:
            print("Error in sending message to %d"%(chat_id))

#-----------------------------------------------------------------------------------------------------------------------
# This function saves Telegram user's photos in photo directory.
def get_user_photos(user_id):
    try:
        profile = bot.getUserProfilePhotos(user_id)
        photos = profile['photos']
        for photo in photos:
            id = photo[0]['file_id']
            file_name = "%s/photos/%s-%s.jpeg"%(home_directory,user_id,id)
            if not os.path.exists(file_name):
                file_info = bot.getFile(id)
                url = "http://api.telegram.org/file/bot{0}/{1}".format(TOKEN, file_info['file_path'])
                f = open( "%s/photos/%s-%s.jpeg"%(home_directory,user_id,id), 'wb')
                f.write(urllib3.urlopen(url).read())
                f.close()
    except:
        print("Unable to get profile picture!")
#-----------------------------------------------------------------------------------------------------------------------
#  This function receives commands from users via telegram and pars them and execute the commands
def on_chat_message(msg):
    content_type, chat_type, user_id, msg_date, msg_id = telepot.glance(msg, long=True)
    command = msg.get('text')
    if command == None:
        return
    try:
        commandlist=list(filter(lambda x:x['title']==command,COMMANDS))
        if commandlist:
            command = commandlist[0]['name']
    except:
        print("command is not in COMMANDS")

    if (command[:6]!='/start') and (command[:7]!='/create'):
        try:
            v = world.find_village(user_id)
        except LookupError as e:
            un = msg['from'].get('username')
            fn = msg['from'].get('first_name')
            ln = msg['from'].get('last_name')
            create(user_id,un,fn,ln)
            return

        if v!=False:
            try:
                print(u"%s %s %s: %s"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),v.first_name,v.last_name,command))
            except:
                print("Error in command")
        else:
            print("No command! I switched to independent start!")
            command = '/start=0'

    menu = main_menu()
    inline_menu= command_menu_inline(command)
    if command == u'worker':
        result=expens(command)
        sendMessage(user_id,result,reply_to_message_id=msg_id,reply_markup=inline_menu)
    elif command==u'home':
        result = expens(command)
        sendMessage(user_id,result,reply_to_message_id=msg_id, reply_markup=inline_menu)
    elif command == u'farm':
        result= expens(command)
        sendMessage(user_id, result,reply_to_message_id=msg_id, reply_markup=inline_menu)
    elif command == u'weapon':
        menu = weapon_menu_inline(user_id)
        sendMessage(user_id,SELECT_WEAPON, reply_markup=menu)
    elif command == u'sell':
        menu = sell_menu_inline()
        sendMessage(user_id,SELECT_GOODS, reply_markup=menu)
    elif command == u'suggestprofile':
        # result=world.suggest_opponent(user_id)    #function move from world class to village class
        result=v.suggest_opponent()  #function suggestion opponent execute in village class
        sendMessage(user_id, result, reply_markup={'keyboard': menu})
    elif command[:8]==u'/profile':       # must be delete
        try:
            enemy_id = command[8:]
            enemy_id = KEY - int(enemy_id)
            enemy=world.find_village(enemy_id)
            sendMessage(user_id, "Village: " + enemy.name, reply_markup=profile_menu_inline(enemy_id))
        except Exception as e :
             print("TYPE: ",type(e))
             print( "ARGS: ",e.args)
             print("Error in attack!")
             # sendMessage(user_id,"Error in attack!" , reply_markup={'keyboard': menu})
    elif command == u'invite':
        print()
        sendMessage(user_id, INVITE % (BOT_LINK,user_id))
        sendMessage(user_id, INVITE2,reply_markup={'keyboard': menu})
    elif command == u'status':
        result = v.status()
        sendMessage(user_id, result, reply_markup={'keyboard': menu})
        # get_user_photos(user_id)
    elif command == u'top10':
        result = world.top10(user_id)
        sendMessage(user_id, result, reply_markup={'keyboard': menu})
    elif command == u'back':
        result = v.status()  # for going home I show status
        sendMessage(user_id, result, reply_markup={'keyboard': main_menu(0)})
    elif command==u'change_village_name':
        fa[user_id] = (STATE_RENAME,0)  # pending for village name
        sendMessage(user_id, ENTER_YOUR_VILLAGE_NAME, reply_markup=nt_force_reply)
    elif command==u'contactus':
        fa[user_id] = (STATE_CONTACTUS,0)  # pending for Admin message
        print("FA:" , fa[user_id])
        sendMessage(user_id, SEND_YOUR_MESSAGE, reply_markup=nt_force_reply)

    elif command[:6] == "/start":
        try:
            print("I clicked Start")
            inviter = int(command[7:])
        except:
            print("error in getting inviter:",command[7:])
            inviter= 0
        print("%s %d invited %d"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),inviter,user_id))
        welcome(user_id, inviter)

    elif command[:7] == '/create':
        try:
            inviter = int(command[8:])
        except:
            inviter= 0
        un= msg['from'].get('username')
        fn=msg['from'].get('first_name')
        ln= msg['from'].get('last_name')
        if create(user_id,un,fn,ln, inviter):
            menu = race_menu_inline()
            sendMessage(user_id, ENTER_RACE, reply_markup=menu)
    elif command=='management':
        menu=main_menu(9)
        sendMessage(user_id,MANAGEMENT_PANNEL, reply_markup={'keyboard': menu})
    else:
        try:
            if fa.get(user_id)[0]==STATE_RENAME:    # text is name of village
                un = msg['from'].get('username')
                fn = msg['from'].get('first_name')
                ln = msg['from'].get('last_name')
                v.rename(command,un,fn,ln)
                del fa[user_id]
                sendMessage(user_id,VILLAGE_RENAMED ,reply_markup={'keyboard': main_menu(0)})

            elif fa.get(user_id)[0]==STATE_CONTACTUS:   # text is a message for admin
                print("message for admin from %s %s"%(v.first_name,v.last_name))
                del fa[user_id]
                world.log_message(user_id,ADMIN_USER_ID, command,1)
                message = "message form %s %s (%s)\n%s"%(v.first_name, v.last_name ,v.name, command)
                # sendMessage(ADMIN_USER_ID,message)
                sendMessage(ADMIN_USER_ID,message,reply_markup=admin_reply_inline(user_id))
                sendMessage(user_id, MESSAGE_SENT,reply_markup={'keyboard': main_menu(0)})

            elif fa.get(user_id)[0]==STATE_POKE:    #text is a poke message
                audience_id = fa[user_id][1]
                del fa[user_id]
                world.log_message(user_id,audience_id,command)
                st="%s"+HAS_SENT_MESSAGE+": \n %s\n%s"%(v.name,"-"*60,command)
                sendMessage(user_id,MESSAGE_SENT, reply_markup={'keyboard':main_menu(0)})
                sendMessage(audience_id, st, reply_markup=profile_menu_inline(user_id))
            elif fa.get(user_id)[0] == STATE_POKE_ADMIN:  # text is a Admin Reply
                audience_id = fa[user_id][1]
                del fa[user_id]
                world.log_message(user_id, audience_id, command)
                st = "%s "+HAS_SENT_MESSAGE+": \n %s\n%s" % ("ADMIN", "-" * 60, command)
                sendMessage(user_id, MESSAGE_SENT, reply_markup={'keyboard': main_menu(0)})
                sendMessage(audience_id, st, reply_markup=profile_menu_inline(user_id))
            else:
                result = v.status() # if text is not command or message status run
                sendMessage(user_id,result,reply_markup={'keyboard': main_menu(0)})
        except:
            result = v.status()  # if text is not command or message status run
            sendMessage(user_id, result, reply_markup={'keyboard': main_menu(0)})
    return

#-----------------------------------------------------------------------------------------------------------------------
#  This function receives inline commands from users via telegram and pars them and execute the commands
def on_callback_query(msg):
    query_id, user_id, query_data = telepot.glance(msg, flavor='callback_query')
    command = query_data
    try:
         v= world.find_village(user_id)
    except LookupError as e:
        print(e.args)
        un = msg['from'].get('username')
        fn = msg['from'].get('first_name')
        ln = msg['from'].get('last_name')
        print(un,fn,ln)
        exit(0)
        # create(user_id,use)
    if command[:6]=='WEAPON':
        wid=int(command[7:])
        if wid==6:
            bot.answerCallbackQuery(query_id, text=WEAPON_IS_NOT_FOR_SELL)
        else:
            result=v.weapon_making(wid)
            bot.answerCallbackQuery(query_id, text=MESSAGES[result])
    elif command[:4]=='SELL':
        goods=command[5:]
        result=v.sell(goods,100)
        bot.answerCallbackQuery(query_id, text=result)
    elif command=='doworker':
        result = v.worker_preparation()
        sendMessage(user_id, MESSAGES[result])
    elif command=='dofarm':
        result = v.farm_preparation()
        sendMessage(user_id, MESSAGES[result])
    elif command =='dohome':
        result = v.home_building()
        sendMessage(user_id,MESSAGES[result])
    elif command[:8]=='doattack':
        try:
            if v.tired != 0:
                sendMessage(user_id, TIRED)
            else:
                enemy_id=int(command[9:])
                enemy=world.find_village(enemy_id)
                print("%s %s attacked %s %s"%(v.first_name,v.last_name,enemy.first_name, enemy.last_name))
                result = v.attack(enemy)
                sendMessage(user_id, result[0], reply_markup={'keyboard': main_menu(0)})
                sendMessage(enemy.userid, result[1])
        except Exception as e :
            print(str(e))
            print("Error in attack!")
            sendMessage(user_id,"Error in attack!" , reply_markup={'keyboard': main_menu(0)})
    elif command[:12] == 'doadminreply':
        audience_id = int(command[13:])
        fa[user_id] = (STATE_POKE_ADMIN, audience_id)
        sendMessage(user_id, SEND_YOUR_MESSAGE , reply_markup=nt_force_reply)
    elif command[:6] == 'dopoke':
        try:
            audience_id = int(command[7:])
            fa[user_id] = (STATE_POKE,audience_id)  # pending to Poke enemy
            sendMessage(user_id, SEND_YOUR_MESSAGE, reply_markup=nt_force_reply)
        except:
            print("Error in poking!")
    elif command[:6] == "create":
        try:
            inviter=int(command[7:])
        except:
            inviter = 0

        un = msg['from'].get('username')
        fn = msg['from'].get('first_name')
        ln = msg['from'].get('last_name')
        if create(user_id,un,fn,ln, inviter):
            menu = race_menu_inline()
            sendMessage(user_id, ENTER_RACE, reply_markup=menu)
    elif command[:4] == 'RACE':
        race = command[5:]
        v.set_race(race)
        fa[user_id] = (STATE_RENAME,0)  # pending for village name
        sendMessage(user_id,ENTER_YOUR_VILLAGE_NAME, reply_markup= nt_force_reply )

#-----------------------------------------------------------------------------------------------------------------------
# There is an admin console web application which is run by Flask.(Located admin directory). All admin commands stores in database
#  and this function check the commands and applies them. then removes them. This function will removed for next updates. We send commands via tcp protocol instead.
def admin_commands():
    world.db.execute("select * from admincommands;")
    records = world.db.fetchall()
    if records:
        world.db.execute("TRUNCATE TABLE admincommands;")
    world.db.close()
    for record in records:
        try:
            command = json.loads(record['command'])
            if (command.get('vid', -1) == -1):
                return False
            v = world.find_by_vid(int(command.get('vid')))
            if v == None:
                return False
            if command.get('message', '') != '':
                sendMessage(v.userid, command.get('message'))
                # world.cursor.execute("delete from admincommands where id = %d;" % (id))
            if command.get('name', '') != '':
                v.name = command.get('name')
            if command.get('race', '') != '':
                v.race = command.get('race')
            if command.get('gold', 0) != 0:
                v.gold = world.load_or_increament(v.gold, command.get('gold', '+0'))
            if command.get('food', 0) != 0:
                v.food = world.load_or_increament(v.food, command.get('food', '+0'))
            if command.get('wood', 0) != 0:
                v.wood = world.load_or_increament(v.wood, command.get('wood', '+0'))
            if command.get('score', 0) != 0:
                v.score = world.load_or_increament(v.score, command.get('score', '+0'))
            if command.get('era', 0) != 0:
                v.era = command.get('era', 0)
            if command.get('home', 0) != 0:
                v.home = world.load_or_increament(v.home, command.get('home', '+0'))
            if command.get('worker', 0) != 0:
                v.worker = world.load_or_increament(v.worker, command.get('worker', '+0'))
            if command.get('farm', 0) != 0:
                v.farm_capasity = world.load_or_increament(v.farm_capasity, command.get('farm', '+0'))
            if command.get('first_name', '') != '':
                v.first_name = command.get('first_name', '')
            if command.get('last_name', '') != '':
                v.last_name = command.get('last_name', '')
            if command.get('shield', 'off') == 'on':
                v.shield = SHIELD_TIME
            if command.get('fast', 0) != 0:
                v.fast = world.load_or_increament(v.fast,command.get('fast',0))
            if command.get('weapon', '') != '':
                weapons = command.get('weapon').split(',')
                for weapon in weapons:
                    (w, c) = weapon.split('-')
                    v.weapon_add_byadmin(int(w), int(c))
        except:
            continue
    return True
#-----------------------------------------------------------------------------------------------------------------------
#  This function is run in each time slice and chack all villages. if village has an operation to do in the operation propetty,
# decrease operation time and if operation time becomes zero , executes the operation.

def check_operation():
        for user in world.users:
            v=user['village']
            if v.tired>0:
                v.tired-=1
            if v.shield>0:
                v.shield-=1
            if v.operation=='':
                continue

            v.operation_time -= 1
            if v.operation_time <= 0:
                if v.operation=='worker':
                    result = v. worker_preparation(1)
                elif v.operation=='farm':
                    result = v.farm_preparation(1)
                elif v.operation == 'home':
                    result = v. home_building(1)
                elif v.operation=='workshop':
                    result = v.workshop_preparation(1)
                elif v.operation[:6]=='weapon':
                    wid=int(v.operation[7:])
                    result = v.weapon_making(wid,1)
                elif v.operation[:6]=='attack':
                    enemyid = int(v.operation[7:])
                    enemy = world.find_village(enemyid)
                    if enemy==False:
                        continue
                    result =  v.attack(enemy,1)
                    v.operation = ''
                    v.operation_time=0
                    sendMessage(v.userid, result[0], reply_markup=attack_rersult_menu_inline(enemy.userid))
                    # if randint(1,10) == 1:
                    #     print "video Sent"
                    #     sendvideo(v.userid)
                    sendMessage(enemy.userid, result[1], reply_markup=attack_rersult_menu_inline(v.userid))
                    continue
                try:
                    sendMessage(v.userid, MESSAGES[result])
                except:
                    pass
                v.operation=''

#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    if USE_PROXY:
        try:

            telepot.api._pools = {
                'default': urllib3.ProxyManager(proxy_url=PROXY_URL, num_pools=3, maxsize=10, retries=False, timeout=30),
            }
            telepot.api._onetime_pool_spec = (
            urllib3.ProxyManager, dict(proxy_url=PROXY_URL, num_pools=1, maxsize=1, retries=False, timeout=30))
        except Exception as e:
            print("ARGS: ", e.args)
            print("Unable to connect to Proxy!")
            exit(-1)


    home_directory = os.getcwd()
    picture_directory = home_directory + "/pictures/"
    video_directory = home_directory + "/videos/"
    # TOKEN is needed to connect to Telegram. but since it is private, It should not come in the project.
    # create a text file, save it as 'token.txt', and write your own telegram bot token on the first line, link of your bot one second line and your Telegram userid on the third line.
    try:
        f = open("token.txt", 'r')
        TOKEN = f.readline().rstrip()
        BOT_LINK = f.readline().rstrip()
        ADMIN_USER_ID = f.readline().rstrip()
        f.close()
    except OSError as e:
        print("""I did not find token.txt file. Please execute the following operations:
              1. create a text file.
              2. On the first line write Your Telegram bot Token (Your token is someting like this: 289549791:AAHIM1_57kqGmbvLHp0E0RLqgPe5krkcawW)
              3. On the second line write your telegram bot link. (ex: https://telegram.me/xxxx_bot)
              4. On the second line write your Telegram Userid.(This id will become admin) Yor userid is a number like this:  87251219
              5. Save it as 'token.txt'.
              Good bye! """)
        exit(1)


    bot = telepot.Bot(TOKEN)

    # We create one instance of world which contains villages
    world = tworld(DBCONFIG)

    MessageLoop(bot,{'chat': on_chat_message,'callback_query': on_callback_query}).run_as_thread()
    print('Listening ...')

    timeslice=0     # This is a counter that increase in while loop. the value is in range of 0-6. if becomes zero run functions
    if DEBUG_MODE:
        SleepTime=1

    while 1:
        time.sleep(SleepTime)
        timeslice=(timeslice+1)%6
        if DEBUG_MODE or timeslice==0:
            if timeslice==0:
                check_operation()
                admin_commands()



