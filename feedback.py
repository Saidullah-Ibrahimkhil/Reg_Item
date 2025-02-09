from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb

class Feedback(tb.Toplevel):
    # shows feedback for an specific operation
    def __init__(self, feedback, operation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(f'{feedback.title()}')
        screen_with = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_width = int(screen_with *0.25)
        win_height = int(screen_height*0.20)
        self.geometry(f'{win_width}x{win_height}+{(screen_with-win_width)//2}+{(screen_height-win_height)//2}')
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        # display message
        self.set_message(feedback, operation)
        # response of the feedback
        self.response = False
        self.set_response()
    

    def set_message(self, feed, oper):
        # set message for dialog box
        if feed == 'success':
            tb.Label(self,text=f'You have successfully {oper} the data...!').grid(row=0, column=0, padx=20, pady=40, sticky='w')
        elif feed == 'failure':
            tb.Label(self, 
                     text=f'Sorry, something went wrong try again...!', 
                     bootstyle = f'danger'
                    ).grid(row=0, column=0, padx=20, sticky='w', pady=40)
            
    
    def set_response(self):
        # response container
        response_frame = tb.Frame(self)
        response_frame.grid(row=1, column=0, sticky='e', padx=15)
        # response buttons
        ok_btn = tb.Button(response_frame, text='OK', command=self.destroy)
        ok_btn.grid(row=0, column=0, padx=5)
        cancel_btn = tb.Button(response_frame, text='Cancel',  command=self.destroy)
        cancel_btn.grid(row=0, column=1, padx=5)
        
    

