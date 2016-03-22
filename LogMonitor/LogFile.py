__author__ = 'zunayed-hassan'
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, datetime, time
from Message import *
from Knowledge import *


"""
CLASS NAME:     LogFile

PURPOSE:        1.  To monitor a log file
                2.  If any changes happened collect those changes
                3.  Convert those changed lines to messages by extracting date-time, user
                    and notification
                4.  Filter those messages, so we may know what happened
                5.  Notify to user
"""
class LogFile:
    LOG_PATH                    = "/var/log/"

    def __init__(self, fileName, guiFrame = None):
        self.FileName                     = fileName
        self.lastFileModificationDateTime = None
        self.guiFrame 			  = guiFrame

        try:
            self.lastFileModificationDateTime = datetime.datetime.fromtimestamp(os.path.getmtime(self.LOG_PATH + self.FileName))
        except:
            print("[!] ERROR: \'" + self.FileName + "\' not found.")

        self.lastFileLines = len(self.getLinesFromFile(self.LOG_PATH + self.FileName))

    """
    METHOD NAME:    getLinesFromFile
    PARAMETER:      string filenameWithPath
    RETURN:         list<string> lines

    PURPOSE:        1. Open a file
                    2. Read lines from file
                    3. Close that file
                    4. Return lines as list of string
    """
    def getLinesFromFile(self, filenameWithPath):
        file = None

        try:
            file = open(filenameWithPath, "r")
        except:
            print("[!] ERROR: \'" + filenameWithPath + "\' not found.")

        lines = file.readlines()
        file.close()

        return lines

    """
    METHOD NAME:    getChangedLines
    PARAMETER:      int previousLines, list<string> currentSetOfLines
    RETURN:         list<string> changes

    PURPOSE:        1. Comapre with last lines of file with newly changed lines of file.
                    2. Extract changed lines from that file.
                    3. Return those changed lines.
    """
    def getChangedLines(self, previousLines, currentSetOfLines):
        changes = []

        for index in range(previousLines, len(currentSetOfLines)):
            changes.append(currentSetOfLines[index])

        return changes

    """
    METHOD NAME:    getParticularIndexOfInterest
    PARAMETER:      list<Knowledge> knowledgeBase, (int) interest
    RETURN:         int index

    PURPOSE:        1. Search through knowledge base for our given interest
                       (USB Connect/Disconnect, Software install/uninstall,
                       ... etc).

                    2. If we found our interest, then return that index of
                       interest.
    """
    def getParticularIndexOfInterest(self, knowledgeBase, interest):
        index = None

        for currentIndex in range(len(knowledgeBase)):
            if (interest == knowledgeBase[currentIndex].Interest):
                index = currentIndex
                break

        return index

    """
    METHOD NAME:    getInsideOfMessage
    PARAMETER:      string message, string separator, string keyword, int end
    RETURN:         string result

    PURPOSE:        1.  Search for unknown portion from a string that only can be
                        identified by a given keyword.

                    2.  If found, return that unknown portion with given  keyword
                        as a string.
    """
    def getInsideOfMessage(self, message, separator, keyword, end = None):
        words = message.split(separator)

        lookFromIndex = None

        for currentIndex in range(len(words)):
            if (keyword in words[currentIndex]):
                lookFromIndex = currentIndex
                break

        lookToIndex = None

        if (end == None):
            lookToIndex = len(words)        
        else:
            lookToIndex = lookFromIndex + end

        result = ""

        for currentIndex in range(lookFromIndex, lookToIndex):
            result += (words[currentIndex] + " ")

        return result

    """
    METHOD NAME:    filterMessages
    PARAMETER:      list<string> logs
    RETURN:         None

    PURPOSE:        1.  Create message object from changed lines from log files.
    
                    2.  For every messages, try to find what event happened.
                    
                    3.  If get sign of anything  familier  happened,  create  a
                        knowledge object and append that to knowledge base.
                        
                    4.  After reading through every messages,  if  enough signs
                        found from knowledge object from knowledge base  notify
                        that to user.
    """
    def filterMessages(self, logs):
        knowledgeBase = []
            
        for log in logs:
            message = Message(Message.LogFileType[self.FileName], log)
            
            # USB disconnect
            if ("USB disconnect" in message.Message):
                usbDisconnectionKnowledge = Knowledge(interest = Knowledge.Interests["USB Disconnect"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                usbDisconnectionKnowledge.Summery.append("USB device disconnected")
                knowledgeBase.append(usbDisconnectionKnowledge)

            # USB connect
            elif ("New USB device found" in message.Message):
                usbConnectionKnowledge = Knowledge(interest = Knowledge.Interests["USB Connect"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                usbConnectionKnowledge.Summery.append("USB device connected.")
                knowledgeBase.append(usbConnectionKnowledge)

            elif ((("Product: USB OPTICAL MOUSE" in message.Message) and (not "Product: USB OPTICAL MOUSE as" in message.Message)) or ("Product: Mass Storage" in message.Message)):
                index = self.getParticularIndexOfInterest(knowledgeBase = knowledgeBase, interest = Knowledge.Interests["USB Connect"])

                if (index != None):
                    if ("Product: USB OPTICAL MOUSE" in message.Message):
                        knowledgeBase[index].Summery.append("Product: USB OPTICAL MOUSE.")
                    elif ("Product: Mass Storage" in message.Message):
                        knowledgeBase[index].Summery.append("Product: Mass Storage Device.")

            elif ("Manufacturer:" in message.Message):
                searchResult = self.getInsideOfMessage(message = message.Message, separator = " ", keyword = "Manufacturer:")
                index = self.getParticularIndexOfInterest(knowledgeBase, Knowledge.Interests["USB Connect"])

                if (index != None):
                    knowledgeBase[index].Summery.append(searchResult.replace(">", ""))

            # HDD unmount
            elif ("Unmounting /dev/sda" in message.Message):
                hddUnmountKnowledge = Knowledge(interest = Knowledge.Interests["HDD Unmount"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                hddUnmountKnowledge.Summery.append("HDD " + message.Message)
                knowledgeBase.append(hddUnmountKnowledge)

            elif ("Unmounted /dev/sda" in message.Message):
                index = self.getParticularIndexOfInterest(knowledgeBase = knowledgeBase, interest = Knowledge.Interests["HDD Unmount"])

                if (index != None):
                    knowledgeBase[index].Summery.append(" and successfully unmounted")

            # HDD Mount
            elif (("Mounted /dev/sda" in message.Message) and (not "on behalf of uid" in message.Message)):
                hddMountKnowledge = Knowledge(interest = Knowledge.Interests["HDD Mount"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                hddMountKnowledge.Summery.append("HDD " + message.Message)
                knowledgeBase.append(hddMountKnowledge)

            # User Login
            elif (("PWD=" in message.Message) and ("USER=" in message.Message) and ("COMMAND=" in message.Message)):
                userLoginKnowledge = Knowledge(interest = Knowledge.Interests["User Login"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                searchResult = self.getInsideOfMessage(message = message.Message, separator = " ", keyword = "PWD=")
                userLoginKnowledge.Summery.append("User logged in. Details: " + searchResult)
                knowledgeBase.append(userLoginKnowledge)

            elif ("session opened for user" in message.Message):
                index = self.getParticularIndexOfInterest(knowledgeBase = knowledgeBase, interest = Knowledge.Interests["User Login"])

                if (index != None):
                    knowledgeBase[index].Summery.append(" (confirmed)")

            # User Logout
            elif ("session closed for user" in message.Message):
                userLogoutKnowledge = Knowledge(interest = Knowledge.Interests["User Logout"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                searchResult = self.getInsideOfMessage(message = message.Message, separator = " ", keyword = "closed")
                userLogoutKnowledge.Summery.append("User logged out and session " + searchResult)
                knowledgeBase.append(userLogoutKnowledge)

            # Software install
            elif (("startup archives unpack" in message.Message) or ("startup archives install" in message.Message)):
                softwareInstallKnowledge = Knowledge(interest = Knowledge.Interests["Software Install"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                softwareInstallKnowledge.Summery.append("Software: ")
                knowledgeBase.append(softwareInstallKnowledge)

            elif ("status half-installed " in message.Message):
                index = self.getParticularIndexOfInterest(knowledgeBase = knowledgeBase, interest = Knowledge.Interests["Software Install"])

                if ((index != None) and (not "installed" in knowledgeBase[index].Summery[len(knowledgeBase[index].Summery) - 1])):
                    knowledgeBase[index].Summery.append(message.Message.split("status half-installed ")[1] + " installed")

            elif ("remove " in message.Message):
                index = self.getParticularIndexOfInterest(knowledgeBase = knowledgeBase, interest = Knowledge.Interests["Software Uninstall"])

                if (index != None):
                    knowledgeBase[index].Summery.append(message.Message.split("remove ")[1] + " uninstalled")

            # Software uninstall
            elif ("startup packages remove" in message.Message):
                softwareUninstallKnowledge = Knowledge(interest = Knowledge.Interests["Software Uninstall"], dateTime = (message.Date + ", " + message.Time), user = message.LoginName)
                softwareUninstallKnowledge.Summery.append("Software: ")
                knowledgeBase.append(softwareUninstallKnowledge)

            elif ("status not-installed" in message.Message):
                index = self.getParticularIndexOfInterest(knowledgeBase = knowledgeBase, interest = Knowledge.Interests["Software Uninstall"])

                if (index != None):
                    knowledgeBase[index].Summery.append(message.Message.split("status not-installed ")[1] + " uninstalled")

        for knowledge in knowledgeBase:
            if (knowledge.Interest == Knowledge.Interests["USB Disconnect"]):
                self.printLog(knowledge)

            elif ((knowledge.Interest == Knowledge.Interests["USB Connect"]) and (len(knowledge.Summery) >= 3)):
                isAllRight = False

                for data in knowledge.Summery:
                    if (("USB device connected" in data) or ("Product: USB OPTICAL MOUSE" in data) or ("Product: Mass Storage Device" in data) or ("Manufacturer:" in data)):
                        isAllRight = True
                    else:
                        isAllRight = False
                        break

                if (isAllRight):
                    self.printLog(knowledge)

            elif ((knowledge.Interest == Knowledge.Interests["HDD Unmount"]) and (len(knowledge.Summery) >= 2) and ("unmounted" in knowledge.Summery[1])):
                self.printLog(knowledge)

            elif (knowledge.Interest == Knowledge.Interests["HDD Mount"]):
                self.printLog(knowledge)

            elif ((knowledge.Interest == Knowledge.Interests["User Login"]) and (len(knowledge.Summery) >= 2) and ("confirmed" in knowledge.Summery[1])):
                self.printLog(knowledge)

            elif ((knowledge.Interest == Knowledge.Interests["User Logout"]) and ("session closed for user" in knowledge.Summery[0])):
                self.printLog(knowledge)

            elif ((knowledge.Interest == Knowledge.Interests["Software Install"]) and (len(knowledge.Summery) >= 2) and ("installed" in knowledge.Summery[1])):
                self.printLog(knowledge)

            elif ((knowledge.Interest == Knowledge.Interests["Software Uninstall"]) and (len(knowledge.Summery) >= 2) and ("uninstalled" in knowledge.Summery[1])):
                self.printLog(knowledge)

        del knowledgeBase
        

    """
    METHOD NAME:    printLog
    PARAMETER:      Knowledge knowledge
    RETURN:         None

    PURPOSE:        Notify to user about event
    """
    def printLog(self, knowledge):
        # Notify in a console line interface
        print(self.FileName + ":\t" + str(knowledge) + " at " + knowledge.DateTime + " by " + knowledge.User + "\n")

        messageType = None

        # Notify in GUI
        if (self.guiFrame != None):
            if (knowledge.Interest == Knowledge.Interests["USB Disconnect"]):
                messageType = "USB Disconnect"
            elif (knowledge.Interest == Knowledge.Interests["USB Connect"]):
                messageType = "USB Connect"
            elif (knowledge.Interest == Knowledge.Interests["HDD Mount"]):
                messageType = "HDD Mount"
            elif (knowledge.Interest == Knowledge.Interests["HDD Unmount"]):
                messageType = "HDD Unmount"
            elif (knowledge.Interest == Knowledge.Interests["User Login"]):
                messageType = "User Login"
            elif (knowledge.Interest == Knowledge.Interests["User Logout"]):
                messageType = "User Logout"
            elif (knowledge.Interest == Knowledge.Interests["Software Install"]):
                messageType = "Software Install"
            elif (knowledge.Interest == Knowledge.Interests["Software Uninstall"]):
                messageType = "Software Uninstall"

	    self.guiFrame.LogFilesTreeView.insert(parent = self.FileName, index = "end", text = messageType, values = (knowledge.DateTime, knowledge.User, str(knowledge)))


    """
    METHOD NAME:    Notify
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        1.  Keep track of file modification changes time
                    2.  If anything changes collect those changed portion and filter
                        those changed lines for finding event
    """
    def Notify(self):
        file = None

        try:
            file = open(
                name = self.LOG_PATH + self.FileName,
                mode = "r"
            )
        except:
            print("[!] ERROR: \'" + file.name + "\' not found.")

        # Getting last modification time (float).
        fileModificationTime =  os.path.getmtime(self.LOG_PATH + self.FileName)

        # Converting last modification time (float) as date time (string) format
        currentFileModificationDateTime = datetime.datetime.fromtimestamp(fileModificationTime)

        # If last file modification date time is not as same as current file modification date time
        if (self.lastFileModificationDateTime != currentFileModificationDateTime):
            # Compare file, get changed lines, process output and print them
            logs = self.getChangedLines(self.lastFileLines, self.getLinesFromFile(self.LOG_PATH + self.FileName))

            self.filterMessages(logs)

            # NOTE: For debugging purpose only
            """
            print("---------------[ " + self.FileName + " ]---------------\n")

            for log in logs:
                message = Message(Message.LogFileType[self.FileName], log)
                print(message)

            print("---------------[ " + self.FileName + " ]---------------\n")
            """

            # Preparing for the next cycle of this loop
            self.lastFileLines = len(self.getLinesFromFile(self.LOG_PATH + self.FileName))
            self.lastFileModificationDateTime = currentFileModificationDateTime

        # Closing the file
        file.close()
        del file

    def __str__(self):
        return self.FileName

