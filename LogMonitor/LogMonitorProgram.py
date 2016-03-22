__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkMessageBox, os
from Tkinter import *
from Window import *
from ObserveFrame import *
from OptionFrame import *
from LogMonitor import *
from LogFile import *
from Settings import *
from SettingsManager import *

"""
CLASS NAME:     LogMonitorProgram

PURPOSE:        1. Initialize GUI of Log Monitor program
                2. Load settings for this program
                3. Also start Log Monitor thread
                4. While window closing, it saves user settings too.
"""
class LogMonitorProgram(Window):
    def __init__(self, parent, title, width, height, windowPosition = None, iconName = None, resizeStyle = None, bgColor = None, theme = "clam"):
        Window.__init__(self, parent, title, width, height, windowPosition, iconName, resizeStyle, bgColor, theme)

        self.parent = parent
        self.initUI()

    """
    METHOD NAME:    initUI
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        Initialize user interface for main Log Monitor program
    """
    def initUI(self):
        self.pack(fill = BOTH, expand = 1)

        notebook = Notebook(master = self)
        notebook.pack(fill = BOTH, expand = 1)

        self.observeFrame = ObserveFrame(parent = notebook)
        self.observeFrame.pack(fill = BOTH, expand = 1)

        self.initializeSettings()        # Load settings and run Log Monitor thread     

        optionFrame = OptionFrame(parent = notebook, settings = self.currentSettings, frame = self.observeFrame)
        optionFrame.pack(fill = BOTH, expand = 1)

        notebook.add(child = self.observeFrame, text = "Observe")
        notebook.add(child = optionFrame,       text = "Option" )

        # Event
        self.parent.protocol("WM_DELETE_WINDOW", self.onWindowClosing)
        
    """
    METHOD NAME:    initializeSettings
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        1. Check for settings file.
                    2. If, there isn't any settings file then create a settings file
                    3. Otherwise load settings file.
                    4. Now, run Log Monitor
    """
    def initializeSettings(self):
        self.currentSettings = None
        self.settingsManager = SettingsManager()
        
        if (os.path.isfile(self.settingsManager.HomeDirectory + self.settingsManager.SettingsFileName)):
            self.currentSettings = self.settingsManager.LoadSettings()
        else:
            self.settingsManager.SaveSettings(Settings())
            self.currentSettings = Settings()

        if (self.currentSettings != None):
            self.runLogMonitorEngine()
        

    """
    METHOD NAME:    runLogMonitorEngine
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        1. Read from settings file
                    2. Run Log Monitor core program according to settings in a thread
    """
    def runLogMonitorEngine(self):
        print("\nLOG MONITOR:\t")

        currentLogFiles = []
        
        self.observeFrame.LogFilesTreeView.insert(parent = "", index = "end", iid = "parent_directory", text = LogFile.LOG_PATH, open = TRUE)

        if (self.currentSettings.SHOW_KERNEL_LOG):
            currentLogFiles.append(LogFile("kern.log", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "kern.log", text = "kern.log", open = TRUE)

        if (self.currentSettings.SHOW_SYSTEM_LOG):
            currentLogFiles.append(LogFile("syslog", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "syslog", text = "syslog", open = TRUE)

        if (self.currentSettings.SHOW_AUTHENTICATION_LOG):
            currentLogFiles.append(LogFile("auth.log", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "auth.log", text = "auth.log", open = TRUE)

        if (self.currentSettings.SHOW_DEBIAN_PACKAGE_LOG):
            currentLogFiles.append(LogFile("dpkg.log", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "dpkg.log", text = "dpkg.log", open = TRUE)

        self.logMonitor = LogMonitor()
        self.logMonitor.SetValue(logFiles = currentLogFiles)
        print(str(self.logMonitor) + "\n")
        self.logMonitor.start()

    """
    METHOD NAME:    onWindowClosing
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        1. Show a confirmation box to confirm about program exit
                    2. If, user response is positive, then save current user settingsto file
                    3. Stop Log Monitor thread
                    4. Quit this application
    """
    def onWindowClosing(self):
        response = tkMessageBox.askquestion(master = self, title = "Exit", message = "Quit... already?", detail = "Are you sure you want to quit?", type = "yesno")

        if (response == "yes"):
            self.settingsManager.SaveSettings(self.currentSettings)
            print("[i] MESSAGE: Settings saved")
            print(self.currentSettings)
            self.logMonitor.Stop = True
            print("[i] MESSAGE: Log Monitor GUI is terminating now.")
            self.quit()
