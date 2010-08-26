"""
   botconfig.py

   This class handles creating the config file (in json format) needed by the ircbot. 
   It also defines methods used to access config data easily.

"""

import json
import platform
import os

class BotConfig:

    def __init__(self):
        # if config doesn't exist, create a new config file
        if not os.path.exists(self.get_config_loc()):
            self.bot_data = {"user" : {"nickname" : "", "password" : ""}, "channels" : [], "log" : \
                    {"links" : "", "reactor" : ""}, "server" : {"host" : "", "port" : ""}}
            self.create_config()

        self.bot_data = json.load(open(self.get_config_loc(), "r"))

    def get_nick(self):
        return self.bot_data["user"]["nickname"]

    def get_pass(self):
        return self.bot_data["user"]["password"]

    def get_channels(self):
        # returns a list instead of a string
        return self.bot_data["channels"]

    def get_link_path(self):
        return self.bot_data["log"]["links"]

    def get_reactor_path(self):
        return self.bot_data["log"]["reactor"]

    def get_host(self):
        return self.bot_data["server"]["host"]

    def get_port(self):
        return self.bot_data["server"]["port"]

    def create_config(self):
        config = open(self.get_config_loc(), "w")
        self.bot_data["server"]["host"] = raw_input("Enter server (ie. irc.freenode.net): ")     
        self.bot_data["server"]["port"] = raw_input("Enter port (ie. 6667): ")
        self.bot_data["user"]["nickname"] = raw_input("Enter nickname to be used by bot: ")
        self.bot_data["user"]["password"] = raw_input("Enter password used to identify nick: ")
        self.bot_data["log"]["reactor"] = raw_input("Enter full path (incl. filename) of reactor log: ")
        self.bot_data["log"]["links"] = raw_input("Enter full path (incl. filename) for links collected: ")
        self.bot_data["channels"] = raw_input("Enter channels you want the bot to join: (ie. #python #c #java): ").split()

        # dump the json data to the config file with nice formatting
        json.dump(self.bot_data, config, sort_keys=True, indent=4)
        config.flush()
        config.close()

    def get_config_loc(self):
        if platform.system() == "Windows":
            return os.path.join(os.getenv("AppData"), "pybot.dat")
        else:
            return os.path.join(os.getenv("HOME"), ".pybot")
