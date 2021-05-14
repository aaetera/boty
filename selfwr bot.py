import telepot
import time
import sqlite3
from pprint import pprint
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = ''
bot = telepot.Bot(TOKEN)
handler = sqlite3.connect('right orders.sqlite')
db = handler.cursor()
#db.execute('DROP TABLE IF EXISTS Orders')
#db.execute('CREATE TABLE Orders (no INTEGER, phone_number INTEGER, name TEXT, destination TEXT, menu TEXT, cost INTEGER)')

def ProceedOrder(offset_, order, chat_id):
    bot.sendMessage(chat_id, 'You entered:')
    string = 'No.' + str(order[0]) + '\nPhone number: ' + str(order[1]) + '\nName: ' + str(order[2]) + '\nDestination: ' + str(order[3]) + '\nMenu: '+ str(order[4]) + '\nCost: ' + str(order[5])
    string1 = '\nIf you want to change something, choose that type or copy message above and resend it with correct info. If you want to save order, press Save button. '
    bot.sendMessage(chat_id, string, reply_markup=inline_save)
    bot.sendMessage(chat_id, string1)
    while 1:
        res = bot.getUpdates(offset=offset_)
        if len(res) < 1:
            pass
        else:
            offset_ = res[0]['update_id'] + 1
            cur_msg = res[0].get('message')
            cur_callback = res[0].get('callback_query')
            if cur_msg:
                text_of_msg = cur_msg.get('text')
                if text_of_msg.startswith('No.'):
                    lis = text_of_msg.split(':')
                    line1 = lis[1].split('\n')
                    line2 = lis[2].split('\n')
                    line3 = lis[3].split('\n')
                    line4 = lis[4].split('\n')
                    order[5] = lis[5]
                    order[1] = line1[0]
                    order[2] = line2[0]
                    order[3] = line3[0]
                    order[4] = line4[0]
                    break
                elif text_of_msg:
                    index = 0
                    while index < len(order):
                        if order[index] == 'null':
                            order[index] = text_of_msg
                else:
                    bot.sendMessage(chat_id, "Don't send this shit again")
            elif cur_callback:
                data = cur_callback['data']
                if data == 'save':
                    break
                if data == 'number':
                    order[1] = 'null'
                    bot.sendMessage(chat_id, 'Enter new number:')
                if data == 'name':
                    order[2] = 'null'
                    bot.sendMessage(chat_id, 'Enter new name:')
                if data == 'menu':
                    order[4] = 'null'
                    bot.sendMessage(chat_id, 'Enter new menu:')
                if data == 'destination':
                    order[3] = 'null'
                    bot.sendMessage(chat_id, 'Enter new destination:')
                if data == 'cost':
                    order[5] = 'null'
                    bot.sendMessage(chat_id, 'Enter new cost:')
            else:
                pass#WIP
    return (offset_, order, chat_id)

def AddOrder(offset_, chat_id):
    bot.sendMessage(chat_id, 'Enter any kind of data(like phone number, name, destination or menu):', reply_markup=remove_markup)
    query = 1
    order = list()
    msg_id = list()
    msg_id.append(0)
    msg_id.append(0)
    msg_id.append(0)
    msg_id.append(0)
    msg_id.append(0)
    msg_id.append(0)
    finded = list()
    order.append('null')
    order.append('null')
    order.append('null')
    order.append('null')
    order.append('null')
    order.append('null')
    finded_number = 'nul'
    finded_name = 'nul'
    finded_destination = 'nul'
    while 1:
        res = bot.getUpdates(offset=offset_)
        if len(res) == 0:
            pass
        else:
            offset_ = res[0]['update_id'] + 1
            cur_msg = res[0].get('message')
            cur_callback = res[0].get('callback_query')
            cur_edited = res[0].get('edited_message')
            
            
            if cur_msg:
                chat_id = cur_msg['from']['id']
                text_o_msg = cur_msg['text']
                db.execute('SELECT * FROM Orders')
                row = db.fetchall()
                max_no = 1
                counter = 0
                if query == 1:
                    if not row:
                        bot.sendMessage(chat_id, 'Database is empty. Fill it up!\nYou entered: ' + text_o_msg + '\nChoose what it is:', reply_markup=inline_chose_data)
                        order[0] = max_no
                        if str(text_o_msg).startswith('0'):
                            text_o_msg = '38' + text_o_msg
                        kind_of_data = (text_o_msg, cur_msg['message_id'])
                    else:
                        max_no = row[-1][0] + 1
                        order[0] = max_no
                        if str(text_o_msg).startswith('0'):
                            text_o_msg = '38' + text_o_msg
                        for tupl in row:
                            index = 0
                            while index < 4:
                                if str(tupl[index]) == str(text_o_msg) and str(text_o_msg) != '--':
                                    finded.append(counter)
                                index += 1
                            counter += 1
                        len_of_finded = len(finded)
                        if len_of_finded != 0:
                            string = ''
                            bot.sendMessage(chat_id, 'We found a match!')
                            #while
                            string += 'Record No.' + str(row[finded[0]][0]) + '\nPhone number: ' + str(row[finded[0]][1]) + '\nName: ' + str(row[finded[0]][2]) + '\nDestination: ' + str(row[finded[0]][3]) + '\n'
                            string += '\nDo you want to use this one?'
                            kind_of_data = (text_o_msg, cur_msg['message_id'])
                            finded_number = row[finded[0]][1]
                            finded_name = row[finded[0]][2]
                            finded_destination = row[finded[0]][3]
                            #index += 1
                            bot.sendMessage(chat_id, string, reply_markup=inline_yes_no)
                        else:
                            kind_of_data = (text_o_msg, cur_msg['message_id'])
                            bot.sendMessage(chat_id, "We haven't found any match." + 'You entered: ' + str(kind_of_data[0]) + "\nChoose its type:", reply_markup=inline_chose_data)
                elif query == 2:
                    order[1] = text_o_msg
                    msg_id[1] = cur_msg['message_id']
                    sometimehelp = int(order[1])
                    print('1')
                    if not str(sometimehelp).startswith('380'):
                        print('2')
                        order[1] = '380' + str(sometimehelp)
                        print('3') 
                    if order[2] == 'null':
                        print('5')
                        bot.sendMessage(chat_id, 'Enter name:')
                        print("6")
                        query = 3
                    else:
                        bot.sendMessage(chat_id, 'Enter destination:')
                        query = 4
                elif query == 3:
                    if order[2] == 'null':
                        order[2] = text_o_msg
                        msg_id[2] = cur_msg['message_id']
                    if order[3] == 'null':
                        bot.sendMessage(chat_id, 'Enter destination:')
                        query = 4
                    else:
                        bot.sendMessage(chat_id, 'Enter menu:')
                        query = 5
                elif query == 4:
                    if order[3] == 'null':
                        order[3] = text_o_msg
                        msg_id[3] = cur_msg['message_id']
                    if order[4] == 'null':
                        bot.sendMessage(chat_id, 'Enter menu:')
                        query = 5
                    else:
                        bot.sendMessage(chat_id, 'Enter cost:')
                        query = 6
                elif query == 5:
                    if order[4] == 'null':
                        order[4] = text_o_msg
                        msg_id[4] = cur_msg['message_id']
                    if order[5] == 'null':
                        bot.sendMessage(chat_id, 'Enter cost:')
                        query = 6
                    else:
                        bot.sendMessage(chat_id, "Order successfully created")
                        break
                elif query == 6:
                    if order[5] == 'null':
                        order[5] = text_o_msg
                        msg_id[5] = cur_msg['message_id']
                    bot.sendMessage(chat_id, 'Order successfully created')
                    break

            elif cur_callback:
                msg_data = cur_callback['data']
                chat_id = cur_callback['from']['id']
                if msg_data == 'number':
                    order[1] = kind_of_data[0]
                    msg_id[1] = kind_of_data[1]
                    bot.sendMessage(chat_id, 'Enter name:')
                    query = 3
                if msg_data == 'name':
                    order[2] = kind_of_data[0]
                    msg_id[2] = kind_of_data[1]
                    bot.sendMessage(chat_id, 'Enter phone number:')
                    query = 2
                if msg_data == 'menu':
                    order[4] = kind_of_data[0]
                    msg_id[4] = kind_of_data[1]
                    bot.sendMessage(chat_id, 'Enter phone number:')
                    query = 2
                if msg_data == 'destination':
                    order[3] = kind_of_data[0]
                    msg_id[3] = kind_of_data[1]
                    bot.sendMessage(chat_id, 'Enter phone number: ')
                    query = 2
                if msg_data == 'no':
                    bot.sendMessage(chat_id, 'You entered: ' + str(kind_of_data[0]) + '\nChoose its type:', reply_markup=inline_chose_data)
                if msg_data == 'yes':
                    bot.sendMessage(chat_id, 'Enter menu:')
                    order[1] = finded_number
                    order[2] = finded_name
                    order[3] = finded_destination
                    query = 5
            
            
            elif cur_edited:
                pass
            else : pass

    print("ORDER : ", order)
    return (offset_, order, chat_id)

def OrderFile(chat_id):
    ordersfile = open('orders.txt', 'w')
    db.execute('SELECT * FROM Orders')
    row = db.fetchall()
    for tupl in row:
        string = '==================================='
        string += '\nNo.' + str(tupl[0]) + '\nPhone number: ' + str(tupl[1]) + '\nName: ' + str(tupl[2]) + '\nDestination: ' + str(tupl[3])
        string += '\nMenu: ' + str(tupl[4]) + '\nCost: ' + str(tupl[5]) + '\n'
        ordersfile.write(string)
    ordersfile.close()


remove_markup = ReplyKeyboardRemove()
markup_main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Add order')], [KeyboardButton(text="View orders"), KeyboardButton(text="Don't touch!")], [KeyboardButton(text='Quit')]])
inline_yes_no = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Yes', callback_data='yes'), InlineKeyboardButton(text='No', callback_data='no')],
               ])
inline_chose_data = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Phone number', callback_data='number'), InlineKeyboardButton(text='Name', callback_data='name')],
                   [InlineKeyboardButton(text='Destination', callback_data='destination'), InlineKeyboardButton(text='Menu', callback_data='menu')]
               ])
inline_save = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Phone number', callback_data='number'), InlineKeyboardButton(text='Name', callback_data='name')],
                   [InlineKeyboardButton(text='Menu', callback_data='menu'), InlineKeyboardButton(text='Destination', callback_data='destination')],
                   [InlineKeyboardButton(text='Cost', callback_data='cost'), InlineKeyboardButton(text='Save', callback_data='save')]
               ])
offset_ = 0
while 1:
    time.sleep(1)
    response = bot.getUpdates(offset=offset_)
    #current_msg = response[0].get('message')
    if len(response) == 0:
        print('\nWaitin for correct input')
    else:
        current_msg = response[0].get('message')
        pprint(current_msg)
        if not current_msg:
            pass
        else:
            offset_ = response[0]['update_id'] + 1
            current_msg = response[0]['message']
            chat_id = current_msg['from']['id']
            pprint(current_msg)
            msg_text = current_msg.get('text')
            if not msg_text:
                bot.sendMessage(chat_id, "Don't send this shit again pls")
            else:
                if msg_text == '/start':
                    bot.sendMessage(chat_id, 'This Bot is created by xXx_FuCk3r228_xXx a.k.a @pivostoner. Use custom keyboard to access main menu.', reply_markup=markup_main_menu)
                    bot.sendPhoto(chat_id, 'AgACAgIAAxkBAAIC3WANjc3JnJbG2WiddYXZK8eFjVrpAAIksjEb6HJpSEXV3ng1Hot_5bKUly4AAwEAAwIAA20AAyQKBgABHgQ')
                elif msg_text == 'Add order':
                    tupl = AddOrder(offset_, chat_id)
                    offset_ = tupl[0]
                    order = tupl[1]
                    chat_id = tupl[2]
                    print('\n\n\n\nORDER: ', order)
                    if len(order) < 5:
                        bot.sendMessage(chat_id, 'Error. Send screenshots to @pivostoner')
                    else:
                        tupl = ProceedOrder(offset_, order, chat_id)
                        offset_ = tupl[0]
                        order = tupl[1]
                        chat_id = tupl[2]                
                        db.execute('INSERT INTO Orders (no, phone_number, name, destination, menu, cost) VALUES (?, ?, ?, ?, ?, ?)', (int(order[0]), int(order[1]), order[2], order[3], order[4], int(order[5])))
                        bot.sendMessage(chat_id, 'Order added successfully', reply_markup=markup_main_menu)
                        handler.commit()
                elif msg_text == 'View orders':
                    bot.sendMessage(chat_id, 'Current orders file')
                    OrderFile(chat_id)
                    ordersfile = open('orders.txt', 'r')
                    bot.sendDocument(chat_id, ordersfile, reply_markup=markup_main_menu)
                else:
                    bot.sendMessage(chat_id, 'Choose action from custom keyboard', reply_markup=markup_main_menu)
