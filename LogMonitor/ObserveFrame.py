__author__ = 'zunayed-hassan'

#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
from ttk     import *
from LogFile import *

"""
CLASS NAME:     ObserveFrame

PURPOSE:        Show GUI of ObserveFrame tab contents
"""
class ObserveFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, master = parent)

        self.initUI()

    def initUI(self):
        observePanedWindow = PanedWindow(master = self, orient = VERTICAL)
        observePanedWindow.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

        logViewLabelFrame    = Labelframe(master = observePanedWindow, text = "Log View")
        detailViewLabelFrame = Labelframe(master = observePanedWindow, text = "Detail"  )

        observePanedWindow.add(child = logViewLabelFrame)
        observePanedWindow.add(child = detailViewLabelFrame)

        logViewFrame = Frame(master = logViewLabelFrame)
        logViewFrame.pack(fill = BOTH, side = TOP, expand = 1)

        self.LogFilesTreeView = Treeview(master = logViewFrame, columns = ("date_time", "user", "notification"))
        self.LogFilesTreeView.column("date_time", width = 100, anchor = "center")
        self.LogFilesTreeView.heading("date_time", text = "Date Time")
        self.LogFilesTreeView.column("user", width = 100, anchor = "center")
        self.LogFilesTreeView.heading("user", text = "User")
        self.LogFilesTreeView.heading("notification", text = "Notification")
        self.LogFilesTreeView.pack(fill = BOTH, side = LEFT, expand = 1)

        self.logFilesTreeViewVScrollbar = Scrollbar(master = logViewFrame, orient = VERTICAL, command = self.LogFilesTreeView.yview)
        self.LogFilesTreeView.configure(yscrollcommand = self.logFilesTreeViewVScrollbar.set)
        self.logFilesTreeViewVScrollbar.pack(fill = BOTH, side = LEFT, expand = 0)

        detailViewFrame1 = Frame(master = detailViewLabelFrame)
        detailViewFrame1.pack(fill = BOTH, expand = 0)

        detailViewFrame2 = Frame(master = detailViewLabelFrame)
        detailViewFrame2.pack(fill = BOTH, expand = 0)

        dateTimeLabel = Label(master = detailViewFrame1, text = "Date Time: ", font = "sans 10 bold", width = 9)
        dateTimeLabel.grid(column = 0, row = 0)

        self.dateTimeDetailData = StringVar()

        dateTimeDetailLabel = Label(master = detailViewFrame1, textvariable = self.dateTimeDetailData, font = "sans 10", width = 20)
        dateTimeDetailLabel.grid(column = 1, row = 0)

        userLabel = Label(master = detailViewFrame1, text = "User: ", font = "sans 10 bold", width = 9)
        userLabel.grid(column = 0, row = 1)

        self.userDetailData = StringVar()

        userDetailLabel = Label(master = detailViewFrame1, textvariable = self.userDetailData, font = "sans 10", width = 20)
        userDetailLabel.grid(column = 1, row = 1)

        messageLabel = Label(master = detailViewFrame1, text = "Message:", font = "sans 10 bold", width = 9)
        messageLabel.grid(column = 0, row = 2)

        self.messageDetailText = Text(master = detailViewFrame2)
        self.messageDetailText.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

        # Event
        self.LogFilesTreeView.bind("<<TreeviewSelect>>", self.onLogFilesTreeViewSelectionChanged)
        self.messageDetailText.bind("<Button-3>", self.onMessageDetailTextStandardContextMenu, add = "")


    """
    EVENT NAME:     onLogFilesTreeViewSelectionChanged

    PURPOSE:        If user selected an item (notification) from tree view, show details
                    about that notification
    """
    def onLogFilesTreeViewSelectionChanged(self, event):
        try:
            selectedItem = self.LogFilesTreeView.selection()[0]
            values = self.LogFilesTreeView.item(selectedItem, "values")

            self.dateTimeDetailData.set(values[0])
            self.userDetailData.set(values[1])
            self.messageDetailText.delete("1.0", END)
            self.messageDetailText.insert(INSERT, values[2])

        except:
            print("[!] WARNING: You have selected an empty item from tree view.\n")

    """
    EVENT NAME:     onMessageDetailTextStandardContextMenu

    PURPOSE:        Show context menu about for messageDetailText, so that, user can copy text
                    of the message details
    """
    def onMessageDetailTextStandardContextMenu(self, e):
        # Right click context menu for all Tk Entry and Text widgets
        try:
            def rClick_Copy(e, apnd=0):
                e.widget.event_generate("<Control-c>")

            e.widget.focus()

            nclst = [
                   ("Copy   Ctrl+C",  lambda e = e: rClick_Copy(e))
            ]

            rmenu = Menu(None, tearoff = 0, takefocus = 0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label = txt, command = cmd)

            rmenu.tk_popup(e.x_root + 40, e.y_root + 10, entry = "0")

        except TclError:
            print "[!] ERROR: Context menu, something wrong"
            pass

        return

