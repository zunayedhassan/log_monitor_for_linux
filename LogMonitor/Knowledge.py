__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CLASS NAME:     Knowledge

PURPOSE:        To hold information of filltered message collected
                from log files.
"""

class Knowledge:
    Interests = {
        "USB Disconnect"      : 0,
        "USB Connect"         : 1,
        "HDD Mount"           : 2,
        "HDD Unmount"         : 3,
        "User Login"          : 4,
        "User Logout"         : 5,
        "Software Install"    : 6,
        "Software Uninstall"  : 7
    }

    def __init__(self, interest, dateTime, user):
        self.Summery  = []
        self.DateTime = dateTime
        self.User     = user
        self.Interest = interest

    def __str__(self):
        text = ""

        for data in self.Summery:
            text += (data + " ")

        return (text)
