import os, sys
import datetime
import telebot
from bot_config import DATA
import psutil
from psutil._common import bytes2human

dat = DATA()
status = 0
bot = telebot.TeleBot(dat.TOKEN, parse_mode=None)

def main():
    temps = psutil.sensors_temperatures()
    for name, entries in temps.items():
        for entry in entries:
            if entry.current > 40:
                bot.send_message(dat.CHAT_ID, f"Температура превышена!\nТекущая температура CPU {entry.current} C")
                status = 1
            if entry.current < 39:
                status = 0


if __name__ == '__main__':
    main()
    bot.polling()