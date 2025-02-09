from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ttkbootstrap as tb
from feedback import Feedback
from model import Item
import os

class ImportBackup:
    # import backup databse data
    def __init__(self, callback):
        self.callback = callback
        self.select_file = filedialog.askopenfilename(title='Select backup file', filetypes=[('SQLite Database','*.db')])
        if self.select_file:
            backup = Item()
            f_result = backup.import_database(self.select_file)
            self.feedback(f_result)
            self.callback()
    
    def feedback(self, feedback_result):
        # shows feedback as a dialog box
        if feedback_result:
            add_feedback = 'success'
        else: 
            add_feedback = 'failure'
        feedback = Feedback(feedback=add_feedback, operation='backup')