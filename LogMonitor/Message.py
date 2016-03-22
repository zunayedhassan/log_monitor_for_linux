__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

"""
CLASS NAME:     Message

PURPOSE:        Hold information about changed line that extracted from log file.
                This information includes date-time, user and notification information.
"""
class Message:
    LogFileType = {
        "kern.log" : 0,
        "syslog"   : 1,
        "dpkg.log" : 2,
        "auth.log" : 3
    }

    def __init__(self, logFileType, log):
        separator       = " "
        (separationRange, monthIndex, dateIndex, timeIndex, loginNameIndex, messageIndex) = (0, None, None, None, None, None)

        if ((logFileType == Message.LogFileType["kern.log"]) or (logFileType == Message.LogFileType["syslog"]) or (logFileType == Message.LogFileType["auth.log"])):
            if (len(str((datetime.datetime.now()).date()).split("-")[2]) == 1):
                (separationRange, monthIndex, dateIndex, timeIndex, loginNameIndex, messageIndex) = (5, 0, 2, 3, 4, 5)
            else:
                (separationRange, monthIndex, dateIndex, timeIndex, loginNameIndex, messageIndex) = (5, 0, 1, 2, 3, 5)

        elif (logFileType == Message.LogFileType["dpkg.log"]):
            (separationRange, monthIndex, dateIndex, timeIndex, loginNameIndex, messageIndex) = (2, 0, None, 1, None, 2)

        self.LogInfo     = log.split(separator, separationRange)
        self.Date        = self.getValue(monthIndex) + " " + self.getValue(dateIndex)
        self.Time        = self.getValue(timeIndex)
        self.LoginName   = self.getValue(loginNameIndex)
        self.Message     = self.getValue(messageIndex)

    """
    METHOD NAME:    getValue
    PARAMETER:      int index
    RETURN:         string

    PURPOSE:        To identify date-time, user and message from a string of line,
                    we separate string by space (" "). As a result we got a list
                    of string. This function helps us to find which one is date-time
                    or which one is user or message from that string of line
                    
    """
    def getValue(self, index):
        if (index != None):
            return self.LogInfo[index]
        else:
            return ""

    def __str__(self):
        return ("LOGIN NAME:\t" + self.LoginName + "\nDATE TIME:\t" + self.Date + ", " + self.Time + "\nMESSAGE:\t" + self.Message)
