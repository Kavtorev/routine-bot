import telebot
from telebot import types
import mysql.connector
import json
import time
from datetime import datetime
from text_constants import (you_are_welcome, missed_all, no_classes, main_keyboard_description, 
                            authentication_description, please_wait_notification, 
                            authentication_trouble, no_upcoming_classes, bad_login)
from secrets import (telegram_bot_token, DATABASE_PASSWD, secret_word)
from settings import (json_properties, func_emojis, msg_emojis, kbrd_emojis)
from classes import (Base, User, Transport, Schedule, Weather)
from selenium.common.exceptions import NoSuchElementException

queue = {}
in_process = False
driver = Base.init_driver()
schedule = Schedule()
database = mysql.connector.connect(
    host="localhost",
    user="user_name",
    passwd=DATABASE_PASSWD,
    db="name of your databases"
)
cursor = database.cursor()
bot = telebot.TeleBot(telegram_bot_token)


def set_up_login_and_password_keyboard(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton(kbrd_emojis['login'])
    itembtn2 = types.KeyboardButton(kbrd_emojis['password'])
    itembtn3 = types.KeyboardButton(kbrd_emojis['later'])
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, authentication_description, reply_markup=markup)

markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(func_emojis['sun'])
itembtn2 = types.KeyboardButton(func_emojis['book'])
itembtn3 = types.KeyboardButton(func_emojis['classes'])
itembtn4 = types.KeyboardButton(func_emojis['log_and_pass'])
itembtn5 = types.KeyboardButton(func_emojis['plan'])
markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

markup_log_passwd = types.ReplyKeyboardMarkup(row_width=1)
markup_log_passwd.add(itembtn4)


def hide_main_keyboard(chat_id):
    """
    Hides 'main keyboard' to avoid spamming.
    It appears after user's request will be processed.
    Imports: 'please_wait_notification'
    """
    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, please_wait_notification ,reply_markup = markup)

"""
Functions:

A.'send_message_about_all_classes'
B.'send_message_about_classes_Iam_late_for'
C.'send_message_about_todays_classes'
D.'send_message_about_possible_routes'
E.'send_weather_forecast'

are getting ready strings to send them to the bot
        
"""
def send_message_about_all_classes(message, classes):
    
    string_to_send = ""
    for date in classes:
        for key, value in date.items():
            string_to_send = f"Date: {key}\n{Base.get_week_day(key)}\n---------------------\n"
            for class_ in value:
                for key_i, value_i in class_.items():
                    string_to_send += f"{key_i.title()}: {value_i}\n"
                string_to_send += "---------------------\n"
                
        bot.reply_to(message, string_to_send, reply_markup = markup)

    

def send_message_about_classes_Iam_late_for(message, classes):
    string_to_send = "You are late for:\n"
    for class_ in classes:
        string_to_send += f"	{class_['subject']} ({class_['start']})\n"
    # bot.send_message(message.chat.id, string_to_send)
    bot.reply_to(message, string_to_send, reply_markup = markup)


def send_message_about_todays_classes(message, classes):
    string_to_send = "Classes for today\n---------------------\n"
    for class_ in classes:
        for key, value in class_.items():
            string_to_send += f"{key.title()}: {value}\n"
        string_to_send += "\n"
    # bot.send_message(message.chat.id, string_to_send)
    bot.reply_to(message, string_to_send, reply_markup = markup)


def send_message_about_possible_routes(message, routes):
    string_to_send = "Possible routes\n---------------------\n"
    for route in routes:
        for key, item in route.items():
            string_to_send += f"{key.title()}: {item}\n"
        string_to_send += "\n---------------------\n"
    # bot.send_message(message.chat.id, string_to_send)
    bot.reply_to(message, string_to_send, reply_markup = markup)


def send_weather_forecast(message, weather):
    string_to_send = "Current Weather:\n" + \
                     f"--------------------------------------------\n" + \
                     f"Temperature: {weather.current_temp}\n" + \
                     f"Description: {weather.description}\n" + \
                     f"--------------------------------------------\n" + \
                     f"The coldest for today: {weather.the_coldest}\n" + \
                     f"--------------------------------------------\n" + \
                     f"Rain? {weather.rain}\n" + \
                     f"--------------------------------------------"
    # bot.send_message(message.chat.id, string_to_send)
    bot.reply_to(message, string_to_send, reply_markup = markup)

def registered_user(message):

    """
    Function queries "uid" (user id) from database 
        and checks whether user is registered or not

    Returns: boolean
    """

    query = "select uid from students;"
    cursor.execute(query)
    result = cursor.fetchall()
    if (message.from_user.id,) in result:
        return True
    return False


def add_to_database(user_info):
    """
    Function adds a new user to database if right 'secret word' was entered
    """
    user_info = (user_info.id, user_info.first_name, user_info.last_name, user_info.username)
    query = "insert into students(uid, first_name, last_name, user_name) values(%s, %s, %s, %s);"
    try:
        cursor.execute(query, user_info)
        database.commit()

        print(f"{' '.join(list(map(str, user_info)))} was registered at {datetime.now().time()}")

    except Exception as e:
        print("Error: ", e)


def get_user_login_and_password(user_id):
    cursor.execute(f"SELECT login, password FROM students WHERE uid = {user_id}")
    return [i for i in cursor.fetchall()[0]]

def generate_user_object(user_id):
    l_p = get_user_login_and_password(user_id)
    user = User(l_p[0], l_p[1], user_id)
    return user

"""
Basic queue functions:
    A.'in_queue'
    B.'empty'
    C.'next_query'
    D.'remove_done_query'
"""
def in_queue(message, users_query):
    return users_query[message] in queue.values()

def empty():
    return len(queue) == 0

def next_query():
    key = list(queue.keys())[0]
    return key

def remove_done_query():
    key = list(queue.keys())[0]
    del queue[key]

@bot.message_handler(commands=['start'], func=lambda message: not (registered_user(message)))
def introduce_bot(message):
    bot.send_message(message.chat.id, msg_emojis['not_registered'])


# /start registered
@bot.message_handler(commands=['start'], func=lambda message: registered_user(message))
def introduce_bot(message):
    bot.reply_to(message, main_keyboard_description, reply_markup = markup)


# enter secret word
@bot.message_handler(func=lambda message: not (registered_user(message)))
def not_registered_user(message):
    if message.text == secret_word:
        add_to_database(message.from_user)
        Base.serialize(json_properties, message.from_user.id)

        print(f"'{message.from_user.id}.json' was created at {datetime.now().time()}")

        bot.send_message(message.chat.id, you_are_welcome)
        set_up_login_and_password_keyboard(message)
    else:
        bot.send_message(message.chat.id, msg_emojis['warning'])


# enter login
@bot.message_handler(func=lambda message: message.text == kbrd_emojis['login'])
def enter_login(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, kbrd_emojis['login'], reply_markup=markup)


# enter password
@bot.message_handler(func=lambda message: message.text == kbrd_emojis['password'])
def enter_password(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, kbrd_emojis['password'], reply_markup=markup)


# reply to 'login' message
@bot.message_handler(func=lambda message: message.reply_to_message != None
                            and message.reply_to_message.text == kbrd_emojis['login'])
def login_is_confirmed(message):
    try:
        cursor.execute(f"UPDATE students SET login = '{message.text}' WHERE uid = '{message.from_user.id}'")
        database.commit()
        bot.send_message(message.chat.id, msg_emojis['confirmed_log'])
        
        print(f"User: {message.from_user.first_name} {message.from_user.last_name} " + \
              f"(ID: {message.from_user.id}) set up LOGIN at {datetime.now().time()}")

    except mysql.connector.Error as error:
        print("Error:", error)
    set_up_login_and_password_keyboard(message)


# reply to 'password' message
@bot.message_handler(func=lambda message: message.reply_to_message != None
                                          and message.reply_to_message.text == kbrd_emojis['password'])
def password_is_confirmed(message):
    try:
        cursor.execute(f"UPDATE students SET password = '{message.text}' WHERE uid = '{message.from_user.id}'")
        database.commit()
        bot.send_message(message.chat.id, msg_emojis['confirmed_pass'])

        print(f"User: {message.from_user.first_name} {message.from_user.last_name} " + \
              f"(ID: {message.from_user.id}) set up PASSWORD at {datetime.now().time()}")

    except mysql.connector.Error as error:
        print("Error:", error)
    
    bot.send_message(message.chat.id, main_keyboard_description, reply_markup = markup)


# set_up_later
@bot.message_handler(func=lambda message: message.text == kbrd_emojis['later'] and registered_user(message))
def set_up_later(message):
    bot.reply_to(message, main_keyboard_description, reply_markup = markup)


# set up login and password
@bot.message_handler(func=lambda message: message.text == func_emojis['log_and_pass'] and registered_user(message))
def login_and_password(message):
    set_up_login_and_password_keyboard(message)

@bot.message_handler(func=lambda m: (m.text in func_emojis.values()) and registered_user(m))
def queue_adder(message):

    hide_main_keyboard(message.chat.id)
    
    try:
        global in_process
        
        users_query = {message : (message.from_user.id, message.text)}
        
        if not in_queue(message, users_query):
            queue.update(users_query)
            print(f"\nUser's query: {message.text} was added to the queue at {datetime.now().time()}")
        
        if not(in_process) and not empty():
            in_process = True
            processing(next_query())
        # else:
        #     bot.send_message(message.chat.id, b'\xF0\x9F\x92\xBD'.decode() + "Please, wait.")

    except Exception as e:
        print("Error: ", e)


def processing(message):
    global in_process
    raised = False
    processing = f"Processing for {message.from_user.first_name} {message.from_user.last_name} " +\
          f"ID({message.from_user.id}), QUERY: {message.text} "

    print(processing + f"STARTED at {datetime.now().time()}")
    """
        if everything is OK:
            if "Classes for today" or "Plan":
                "grab classes for today"
                if "there are any":
                    if "If user is late for some but there are still a few to visit":
                        "Inform about missed classes"
                    "Send message about classes for today..."

                    if "Plan was entered":
                        "Do some operations to create a route"
                elif "if missed all":
                    "Inform that all classes were missed"
                else:
                    "Inform that there are no classes for today"
            elif "Upcoming classes":
                "grab upcoming classes"
                if "there any":
                    "Send message about upcoming classes"
                else:
                    "Inform that there are no classes"
            else "Weather":
                "Show current weather in Wroclaw"
    """
    user = generate_user_object(message.from_user.id)
    try:
        if message.text != func_emojis['sun'] and message.text != func_emojis['classes']:
            # Blok #1
            classes = schedule.classes_to_visit(schedule.todays_date, driver, user.login,
                                                user.password, user.id)
            if classes:
                if schedule.missed_a_few:
                    send_message_about_classes_Iam_late_for(message, schedule.classes_you_are_late_for)
                send_message_about_todays_classes(message, classes)

                if message.text == func_emojis['plan']:
                    transport = Transport()
                    data = transport.get_transport_time(classes[0]['start'], transport.todays_date_1,
                                                        driver, user.id, len(schedule.classes_you_are_late_for))
                    send_message_about_possible_routes(message, data['routes'])
                    show_weather(message)

            elif schedule.missed_all:
                # bot.send_message(message.chat.id, missed_all)
                bot.reply_to(message, missed_all, reply_markup = markup)

            else:
                # bot.send_message(message.chat.id, no_classes)
                bot.reply_to(message, no_classes, reply_markup = markup)


        elif message.text == func_emojis['classes']:
            # Blok #2
            
            classes = schedule.get_list_of_all_classes(driver, user.login, user.password, user.id)
            if classes != []:
                send_message_about_all_classes(message, classes)
            
            else:
                # bot.send_message(message.chat.id, "You don't have any upcoming classes...")
                bot.reply_to(message, no_upcoming_classes, reply_markup = markup)

        else:
            # Block #3
            show_weather(message)

        print(processing + f"FINISHED at {datetime.now().time()}")
        
        remove_done_query()

        if not empty():
            processing(next_query())
        else:
            in_process = False

    except NoSuchElementException as e:
        print("\nNo such element...\n", "Message:", e)
        bot.reply_to(message, bad_login, reply_markup = markup_log_passwd)
        raised = True

    except Exception as e:
        raised = True
        print(e)
    
    finally:
        if raised:
            queue = {}
            in_process = False

def show_weather(message):
    weather = Weather()
    weather.get_weather_forecast()
    send_weather_forecast(message, weather)


bot.polling()
database.close()



















