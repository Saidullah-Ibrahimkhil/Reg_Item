from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import ttkbootstrap as tb
from feedback import Feedback
from model import Item
import os
class Backup:
    def __init__(self):
        self.select_folder = filedialog.askdirectory(title='Backup Folder')
        if self.select_folder:
            backup_path = os.path.join(self.select_folder,'backup.db')
            backup = Item()
            f_result = backup.export_database(backup_path)
            self.feedback(f_result)

    
    def feedback(self, feedback_result):
        # shows feedback as a dialog box
        if feedback_result:
            add_feedback = 'success'
        else: 
            add_feedback = 'failure'
        feedback = Feedback(feedback=add_feedback, operation='backup')

        
