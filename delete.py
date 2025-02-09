from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb
from datetime import datetime
from model import Item
from feedback import Feedback

class DeleteItem(tb.Toplevel):
    # Delete data from database
    def __init__(self, callback, item_id,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.item_id = item_id
            self.callback = callback
            self.title('Delete Item')
            self.columnconfigure(0,weight=1)
            screen_with = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            win_width = int(screen_with*0.24)
            win_height = int(screen_height*0.16)
            self.geometry(f'{win_width}x{win_height}+{(screen_with-win_width)//2}+{(screen_height-win_height)//2}')
            self.resizable(False, False)
            self.create_widget()
    
    def create_widget(self):
          tb.Label(self, text='Are you sure...?\nData will be deleted permenantly.').grid(row=0, column=0, sticky='w', padx=30, pady=(20,20))
          action_btn = tb.Frame(self)
          action_btn.grid(row=1, column=0, sticky='e', padx=10)
          yes_btn = tb.Button(action_btn, text='Yes', bootstyle='info', command=self.delete_item)
          yes_btn.grid(row=0, column=0,padx=5)
          yes_btn = tb.Button(action_btn, text='Cancel', bootstyle='info', command=self.destroy)
          yes_btn.grid(row=0, column=1,padx=5)

    def delete_item(self):
          item = Item()
          f_result = item.delete(self.item_id)
          self.destroy()
          self.feedback(f_result)
          self.callback()

    def feedback(self, feedback_result):
        # shows feedback as a dialog box
        if feedback_result:
            add_feedback = 'success'
        else: 
            add_feedback = 'failure'
        feedback = Feedback(feedback=add_feedback, operation='delete')
    