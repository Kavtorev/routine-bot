# telegram-bot
Bot that facilitates student's life.
## Idea and Purpose
Waking up every morning I've noticed that I have a morning ritual.
I go to the site of my University to check whether I have classes or not, I look at the weather forecast (is it a rainy day or what is the coldest temperature for today) and finally I look at the public transport schedule. 

So, I came up with an idea: "**Why don't to create something that could do all those things instead of me?**".

## Description
Basically, bot possess 4 functions:
* Weather:
  * shows current weather in the city where I study
  * informs whether there is rain today
  * shows the coldest temperature for today
  
* Classes for today:
  Shows 

## Technologies
* Python modules:
  * selenium
  * requests
  * mysql-connector
* SQL
* [OpenWeatherAPI](https://openweathermap.org/api)
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

## Requirements
Python 3.6 or later. 

All requirements you can find in 'requirements.txt'.

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
      
   "last_update": "2020-01-19",
   "missed_clss": 0
}   
```
* Details about current weather (current_weather.json). Sample of a server's respond you can find here: [Sample](https://openweathermap.org/current)
* 5 day / 3 hour forecast (weather_forecast.json). [Sample](https://openweathermap.org/forecast5)


