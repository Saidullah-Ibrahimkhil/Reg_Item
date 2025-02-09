from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb
from datetime import datetime
from model import Item
from feedback import Feedback
import os
import sys


class AddItem(tb.Toplevel):
    # Show registeration form and add items to data base via model
    
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.title('Item New Item')
        screen_with = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_width = int(screen_with*0.28)
        win_height = int(screen_height*0.47)
        self.geometry(f'{win_width}x{win_height}+{(screen_with-win_width)//2}+{(screen_height-win_height)//2}')
        self.resizable(False, True)
        self.iconbitmap(default=self.resource_path('assets\\img.ico'))
        # create widiget
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.create_widget()


    def create_widget(self):
        # create widget for add new items
        # label
        tb.Label(self, text='Device Name', font=('Trebuchet MS', 8, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=(20,0))
        tb.Label(self, text='Device Serial', font=('Trebuchet MS', 8, 'bold')).grid(row=0, column=1, sticky='w', padx=10, pady=(20,0))
        # entry box
        self.device_name = tb.Entry(self, width=24, takefocus=1)
        self.device_name.grid(row=1, column=0, sticky='w', padx=10, pady=(0,10))
        self.device_name.focus()
        self.device_serial = tb.Entry(self, width=24)
        self.device_serial.grid(row=1, column=1, sticky='w', padx=10, pady=(0,10))
        #label 
        tb.Label(self, text='Location', font=('Trebuchet MS', 8, 'bold')).grid(row=2, column=0, sticky='w', padx=10)
        tb.Label(self, text='Submit Date', font=('Trebuchet MS', 8, 'bold')).grid(row=2, column=1, sticky='w', padx=10)
        # widget
        self.device_location = tb.Entry(self, width=24)
        self.device_location.grid(row=3, column=0, sticky='w', padx=10, pady=(0,10))
        self.submit_date = tb.DateEntry(self,firstweekday=5)
        self.submit_date.grid(row=3, column=1, sticky='w', padx=10, pady=(0,10))
        #label 
        tb.Label(self, text='Submitter Name', font=('Trebuchet MS', 8, 'bold')).grid(row=4, column=0, sticky='w', padx=10)
        tb.Label(self, text='Submitter Contact', font=('Trebuchet MS', 8, 'bold')).grid(row=4, column=1, sticky='w', padx=10)
        # entry box
        self.submitter_name = tb.Entry(self, width=24)
        self.submitter_name.grid(row=5, column=0, sticky='w', padx=10, pady=(0,10))
        self.submitter_contact = tb.Entry(self, width=24)
        self.submitter_contact.grid(row=5, column=1, sticky='w', padx=10, pady=(0,10))
        #label 
        tb.Label(self, text='Deliverer Name', font=('Trebuchet MS', 8, 'bold')).grid(row=6, column=0, sticky='w', padx=10)
        tb.Label(self, text='Delivery Date', font=('Trebuchet MS', 8, 'bold')).grid(row=6, column=1, sticky='w', padx=10)
        # widget
        self.deliverer_name = tb.Entry(self, width=24)
        self.deliverer_name.grid(row=7, column=0, sticky='w', padx=10, pady=(0,10))
        self.delivery_date = tb.DateEntry(self,firstweekday=5)
        self.delivery_date.grid(row=7, column=1, sticky='w', padx=10, pady=(0,10))
        self.delivery_date.entry.delete(0, END)
        # buttons
        buttons_frame = tb.Frame(self)
        buttons_frame.grid(row=9, column=1, sticky='e', pady=(15,0), padx=20)
        save_button = tb.Button(buttons_frame, text='Save', bootstyle = 'info', command=self.add_item)
        save_button.grid(row =0, column=0, padx=5)
        save_button = tb.Button(buttons_frame, text='Cancel', bootstyle = 'info', command=self.destroy)
        save_button.grid(row =0, column=1, padx=5)

    
    def add_item(self):
        # send data to database
        invalid_input = self.is_valid()
        self.invalid_frame_flag = False
        valid = True
        for invalid_data in invalid_input:
            if len(invalid_data) != 0:
                valid = False
                break
        if valid:
            item_data = (self.device_name.get(),
                        self.device_serial.get(),
                        self.device_location.get(),
                        self.submitter_name.get(),
                        self. submitter_contact.get(),
                        self.valid_date(self.submit_date.entry.get()),
                        self.deliverer_name.get(),
                        self.valid_date(self.delivery_date.entry.get())
                        )
            my_item =  Item()
            f_result = my_item.create(item_data=item_data)
            self.feedback(f_result)
            self.callback()
        else:
            self.invalid_frame = tb.Frame(self)
            self.invalid_frame.grid(row=8, column=0, columnspan=2)
            if len(invalid_input[0])  !=0:
                tb.Label(self.invalid_frame, text=f'Missing Inputs: '+self.show_error(invalid_input[0]),font=('Trebuchet MS', 8), bootstyle='danger').grid(row=0, column=0, sticky='w', padx=10)
            if len(invalid_input[1]) !=0:
                tb.Label(self.invalid_frame, text=f'Invalid Inputs: '+self.show_error(invalid_input[1]),font=('Trebuchet MS', 8), bootstyle='danger').grid(row=1, column=0, sticky='w', padx=10)
            self.invalid_frame_flag = True
    
    def show_error(self,error_data):
        message =''
        for i,error in enumerate(error_data):
            if i == len(error_data)-1:
                message += f'{error}'
            elif i == 2 or i == 5:
                message+=f'{error}\n'
            else:
                message += f'{error}, '
        return message
    
    def is_valid(self):
        missing_values = list()
        invalid_values = list()
        # check device name
        if self.device_name.get() == '':
            missing_values.append('Device Name')
        elif not self.device_name.get().isalnum():
            invalid_values.append('Invalid Name')
        # check device name
        if self.device_serial.get() == '':
            missing_values.append('Device Serial')
        elif not self.device_serial.get().isalnum():
            invalid_values.append('Invalid Serial')
        # check location 
        if self.device_location.get() == '':
            missing_values.append('Location')
        else:
            device_location = self.device_location.get().split()
            for location_part in device_location:
                if not location_part.isalnum():
                    invalid_values.append('Invalid Location')
        # check submit date
        if self.submit_date.entry.get() =='':
            missing_values.append('Submit Date')
        else:
            enter_date = self.submit_date.entry.get().split()
            for date_part in enter_date[0].split('/'):
                if not date_part.isnumeric():
                    invalid_values.append('Invalid Submit Date')
        # check submit date    
        if self.submitter_name.get() =='':
            missing_values.append('Submitter Name')
        for name_part in self.submitter_name.get().split():
            if not name_part.isalpha():
                invalid_values.append('Invalid Submitter Name')
        # check submitter contact
        if self.submitter_contact.get() =='':
            missing_values.append('Submitter Contact')
        elif not self.submitter_contact.get().isnumeric():
            invalid_values.append('Invalid Contact')
        # check deliverer_name
        if self.deliverer_name.get() !='':
            for name_part in self.deliverer_name.get().split():
                if not name_part.isalpha():
                    invalid_values.append('Invalid Deliverer Name')
        # check delivery date
        if self.delivery_date.entry.get() !='':
            enter_date = self.delivery_date.entry.get().split()
            for date_part in enter_date[0].split('/'):
                if not date_part.isnumeric():
                    invalid_values.append('Invalid Delivery Date')

        # return True if len(invalid_values) ==0 else False
        return (missing_values, invalid_values)


    def valid_date(self, str_date):
        # change string date to a valid datetime object
        if str_date != '':
            row_date = list(map(int, str_date.split('/')))
            valid_date = datetime(row_date[2], row_date[0], row_date[1])
            return valid_date
    
    def feedback(self, feedback_result):
        # shows feedback as a dialog box
        if feedback_result:
            add_feedback = 'success'
            self.clear_form()
        else: 
            add_feedback = 'failure'
        feedback = Feedback(feedback=add_feedback, operation='add')


    def clear_form(self):
        # clears form data after submission
        if self.invalid_frame_flag:
            self.invalid_frame.destroy()
        self.device_name.delete(0, END)
        self.device_serial.delete(0, END)
        self.device_location.delete(0, END)
        self.submit_date.entry.delete(0, END)
        self.submitter_name.delete(0, END)
        self.submitter_contact.delete(0, END)
        self.deliverer_name.delete(0, END)
        self.delivery_date.entry.delete(0, END)
        self.device_name.focus()
    
    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

