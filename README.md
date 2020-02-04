# routine bot
Bot that facilitates student's life.
## Idea and Purpose
Waking up every morning I've noticed that I have a morning ritual.
I go to the site of my University to check whether I have classes or not, I look at the weather forecast (is it a rainy day or what is the coldest temperature for today) and finally I look at the public transport schedule. 

So, I came up with an idea: "**Why don't to create something that could do all those things instead of me?**".

## Description

Project was implemented in Python using "selenium", "requests" and "mysql-connector" modules. I used Web-scraping and some APIs([OpenWeatherAPI](https://openweathermap.org/api), [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) ). As far as 'Virtual Campus" of my university doesn't possess an API I had to use Web-scraping partly. The bot is functioning in [Telegram messanger](https://telegram.org/).

Bot possess 4 functions:
* **Weather**:
  * shows current weather in the city where I study
  * informs whether there is rain today
  * shows the coldest temperature for today
  
  
* **Classes for today**:
  * informs user if he is late for any classes
  * if user has classes shows details
  * if classes user is late for all classes - informs


* **Upcoming classes**:

  Just shows info about classes for the current week and partly for the next one.


* **Plan your route** (**uncompleted**)

  That function plans user's route to the university basing on time his classes start, it takes into account if user is      late for some of his classes and adoptes to changings. Also, "Plan your route" function invokes (Weather, Classes for today) decribed above and generally sends three messages (Routes, Classes, Weather). Planning of routes depends on whether there are classes or not, if not or user is late for all classes - function won't plan a route.
  
![Sample1](https://github.com/Kavtorev/telegram-bot/blob/master/screens/weather.png) ![Sample2](https://github.com/Kavtorev/telegram-bot/blob/master/screens/classes%20for%20today.png) ![Sample3](https://github.com/Kavtorev/telegram-bot/blob/master/screens/upcoming%20classes.png) ![Sample4](https://github.com/Kavtorev/telegram-bot/blob/master/screens/routes.png)

### Authentication

To use the bot, user should enter the "secret word", after he does and the word is valid script creates "user_id".json file to store data (see **Data Models** below) and adds user to a database ([SQL code](https://github.com/Kavtorev/telegram-bot/tree/master/src/sql){:target="_blank"}).

![Sample](https://github.com/Kavtorev/telegram-bot/blob/master/screens/valid%20secret%20code.png)

Then user should enter LOGIN and PASSWORD from "Virtual Campus" to allow '[webdriver](https://www.guru99.com/introduction-webdriver-comparison-selenium-rc.html)' to scrape a web-page and to grab necessary data.

![Sample1](https://github.com/Kavtorev/telegram-bot/blob/master/screens/login.png) ![Sample1](https://github.com/Kavtorev/telegram-bot/blob/master/screens/password.png)

### Menus
![Sample1](https://github.com/Kavtorev/telegram-bot/blob/master/screens/menus2.png) ![Sample1](https://github.com/Kavtorev/telegram-bot/blob/master/screens/menus1.png)

### Commands

**/start** - to open ReplyMarkUp (Main menu with available functions) and get description of how you can use offered options.

## Data models
This bot will store:
* Information about classes of users and their transport schedule time:

An Example:
```json
{
  "classes": [
        {
          "2020-01-20": [
              {
                  "subject": "Programowanie obiektowe ",
                  "start": "8:15",
                  "finish": "9:00",
                  "duration": "1h00m",
                  "type_of_class": "Wyk"
              },
              {
                  "subject": "Programowanie obiektowe ",
                  "start": "9:00",
                  "finish": "9:45",
                  "duration": "1h00m",
                  "type_of_class": "Lab"
              }
            ]
        }
      ],
      
   "routes": [
        {
            "Leave in": "16:46",
            "Departure Time": "16:50",
            "Arrival Time": "17:22",
            "Travel Line": "4"
        }
      ],
   "classes_update": "2020-02-04",
   "transport_update": "2020-02-04",
   "missed_clss": 0
}   
```
* Details about current weather (current_weather.json). Sample of a server's respond you can find here: [Sample](https://openweathermap.org/current)
* 5 day / 3 hour forecast (weather_forecast.json). [Sample](https://openweathermap.org/forecast5)


