# World War



[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

World war is a strategic text-based game based on Telegram bot. In this game you found your village, prepare an army and attack your enemies and by conquering them to become a super power of the world. Try to keep yourself in top 10 super powers.

  
# Senario:
You have 100 gold coins, 100 woods, 100 foods, by default. You are supposed to create workers to work for you. Then by creating farms you can increase amount of food which is vital for your soldiers. In addition you can sell your food and earn gold.
To be safe from your enemy, make an army as soon as possible. With the help of menu you are capable to access the weapons.
At first you can have only access to swords. Not only by introduce this game to your friends your weapon menu will be opened for you but also you will get 100 gold coins. It is important to know that the values of coins in this game is more valuable than other games.
Try to attack your neighbors and conquer that in order to gain a lot of scores and what’s more get lots of booties (Gold, Food, and Wood). The more you attack the more your army get skillful and you increase your chance to conquer the next war.
Try to become to a super power in the world.
By clicking to top10 button, you will see top10 superpowers.

  ### Installation

  - install python 3.8
  - install mysql
  - run 'CREATE DATABASE.sql'
  - install dependencies
  - modify configuration.py
  - create a 'token.txt' file

### How to create TOKEN.txt
- Create a text file.
- On the first line write Your Telegram bot Token (Your token is someting like this:
 289549791:AAHIM1_57kqGmbvLHp0E0RLqgPe5krkcawW)
- On the second line write your telegram bot link. (eg: https://telegram.me/xxxx_bot)
- On the second line write your Telegram Userid.(This id will become admin) Yor userid is a number like this:  87251219
- Save it as 'token.txt'.

### run
```sh
$ python3 telegram.py
```

To install the game:
  - install python 3.8
  - install mysql
  - run 'CREATE DATABASE.sql'
  - install dependencies
  - create a 'token.txt' file

### Tech

In this game we have used

* [] - Telepot module
* [] - Mysql
* [] - Python 3.8
* [] - Telegram
###  For the next commit we are going to use:
* [.js] - FLASK
* [.js] - Jinja2
* [] - BluePrint
* [] - Gentelella


### Configuration
Before run the game configure configuration.py file
database parameters:
 Parameter | Value |
| ------ | ------ |
| host | YOUR HOST |
| username  | DATABASE USER |
| password | YOUR PASSWORD |
| database | YOUR DATABASE NAME |

For production environments, go to configuration.py and   Set DEBUG_MODE to False
Parameter | Value |
| ------ | ------ |
| DEBUG_MODE | False |
Telegram has been filtered in some countries. If so set the proxy in configuration.py

| Parameter | Value |
| ------ | ------ |
| USE_PROXY | True |
| PROXY_URL =  | IP:Port (eg: http://127.0.0.1:8118) |


