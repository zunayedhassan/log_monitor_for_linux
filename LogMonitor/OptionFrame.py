__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkMessageBox
from Tkinter import *
from ttk import *
from Settings import *
from SettingsManager import *
from LogMonitor import *
from LogFile import *

"""
CLASS NAME:         OptionFrame

PURPOSE:            Show GUI of OptionFrame tab contents
"""
class OptionFrame(Frame):
    def __init__(self, parent, settings, frame):
        Frame.__init__(self, master = parent)

        self.currentSettings = settings
        self.observeFrame    = frame
        self.initUI()

    """
    METHOD NAME:    initUI
    PARAMETER:      None
    RETURN:         None

    PURPOSE:        Initialize user interface for OptionFrame
    """
    def initUI(self):
        self.ShowKernelLog         = BooleanVar(value = self.currentSettings.SHOW_KERNEL_LOG)
        self.ShowSystemLog         = BooleanVar(value = self.currentSettings.SHOW_SYSTEM_LOG)
        self.ShowAuthenticationLog = BooleanVar(value = self.currentSettings.SHOW_AUTHENTICATION_LOG)
        self.ShowDebianPackageLog  = BooleanVar(value = self.currentSettings.SHOW_DEBIAN_PACKAGE_LOG)   
        
        chooseLogFileLabelFrame = LabelFrame(master = self, text = "Choose Log File")
        chooseLogFileLabelFrame.pack(fill = BOTH, side = TOP, expand = 1, padx = 20, pady = 20)
        
        kernelLogCheckButton = Checkbutton(master = chooseLogFileLabelFrame, text = "kern.log: USB device connect/disconnect", variable = self.ShowKernelLog, command = self.onKernelLogCheckButtonClicked)
        kernelLogCheckButton.pack(fill = None, expand = 0, side = TOP, anchor = W, padx = 20, pady = 5)

        systemLogCheckButton = Checkbutton(master = chooseLogFileLabelFrame, text = "syslog: HDD and USB device mount/unmount", variable = self.ShowSystemLog, command = self.onSystemLogCheckButtonclicked)
        systemLogCheckButton.pack(fill = None, expand = 0, side = TOP, anchor = W, padx = 20, pady = 5)
        
        authenticatLogCheckButton = Checkbutton(master = chooseLogFileLabelFrame, text = "auth.log: root user's command", variable = self.ShowAuthenticationLog, command = self.onAuthenticationLogCheckButtonClicked)
        authenticatLogCheckButton.pack(fill = None, expand = 0, side = TOP, anchor = W, padx = 20, pady = 5)

        dpkgLogCheckButton = Checkbutton(master = chooseLogFileLabelFrame, text = "dpkg.log: Software install/uninstall", variable = self.ShowDebianPackageLog, command = self.onDpkgLogCheckButtonClicked)
        dpkgLogCheckButton.pack(fill = None, expand = 0, side = TOP, anchor = W, padx = 20, pady = 5)
        

        bottomFrame = Frame(master = self)
        bottomFrame.pack(fill = None, side = BOTTOM, expand = 0)

        aboutButton = Button(master = bottomFrame, text = "About", command = self.onAboutButtonClicked)
        aboutButton.pack(fill = None, expand = 1, padx = 5, pady = 5)

    """
    EVENT NAME:     onKernelLogCheckButtonClicked, onSystemLogCheckButtonclicked, onAuthenticationLogCheckButtonClicked, onDpkgLogCheckButtonClicked

    PURPOSE:        Based on which option checked manage which log file will notify to user
    """
    def onKernelLogCheckButtonClicked(self):
        if (not self.ShowKernelLog.get()):
            self.currentSettings.SHOW_KERNEL_LOG = False
            self.removeItemFromLogFileList("kern.log")
            self.observeFrame.LogFilesTreeView.delete("kern.log")
            print(self.currentSettings)
        else:
            self.currentSettings.SHOW_KERNEL_LOG = True
            LogMonitor.LOG_FILES.append(LogFile("kern.log", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "kern.log", text = "kern.log", open = TRUE)
            print(self.currentSettings)

    def onSystemLogCheckButtonclicked(self):
        if (not self.ShowSystemLog.get()):
            self.currentSettings.SHOW_SYSTEM_LOG = False
            self.removeItemFromLogFileList("syslog")
            self.observeFrame.LogFilesTreeView.delete("syslog")
            print(self.currentSettings)
        else:
            self.currentSettings.SHOW_SYSTEM_LOG = True
            LogMonitor.LOG_FILES.append(LogFile("syslog", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "syslog", text = "syslog", open = TRUE)
            print(self.currentSettings)

    def onAuthenticationLogCheckButtonClicked(self):
        if (not self.ShowAuthenticationLog.get()):
            self.currentSettings.SHOW_AUTHENTICATION_LOG = False
            self.removeItemFromLogFileList("auth.log")
            self.observeFrame.LogFilesTreeView.delete("auth.log")
            print(self.currentSettings)
        else:
            self.currentSettings.SHOW_AUTHENTICATION_LOG = True
            LogMonitor.LOG_FILES.append(LogFile("auth.log", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "auth.log", text = "auth.log", open = TRUE)
            print(self.currentSettings)

    def onDpkgLogCheckButtonClicked(self):
        if (not self.ShowDebianPackageLog.get()):
            self.currentSettings.SHOW_DEBIAN_PACKAGE_LOG = False
            self.removeItemFromLogFileList("dpkg.log")
            self.observeFrame.LogFilesTreeView.delete("dpkg.log")
            print(self.currentSettings)
        else:
            self.currentSettings.SHOW_DEBIAN_PACKAGE_LOG = True
            LogMonitor.LOG_FILES.append(LogFile("dpkg.log", self.observeFrame))
            self.observeFrame.LogFilesTreeView.insert(parent = "parent_directory", index = "end", iid = "dpkg.log", text = "dpkg.log", open = TRUE)
            print(self.currentSettings)


    """
    EVENT NAME:     onAboutButtonClicked

    PURPOSE:        Show information about Log Monitor program
    """
    def onAboutButtonClicked(self):
        tkMessageBox.showinfo(master = self, title = "About", message = "Log Monitor (1.0.1)", detail = "\nby Mohammod Zunayed Hassan\nEmail: zunayed-hassan@live.com")


    """
    METHOD NAME:    removeItemFromLogFileList
    PARAMETER:      string logFileName
    RETURN:         None

    PURPOSE:        If LogMonitor.LOG_FILES contains particuler file that we are looking for,
                    remove that item from that list.
    """
    def removeItemFromLogFileList(self, logFileName):
        for logFile in LogMonitor.LOG_FILES:
                if (logFile.FileName == logFileName):
                    LogMonitor.LOG_FILES.remove(logFile)

