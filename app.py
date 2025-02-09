from tkinter import *
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame 
from PIL import Image, ImageTk
from model import Item
from add_item import AddItem
from update_item import UpdateItem
from delete import DeleteItem
from database_backup import Backup
from import_backup import ImportBackup
import os
import sys

class App(tb.Window):
    
    # Main window of application 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        screen_with = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.app_with = int(screen_with*0.80)
        self.app_height = int(screen_height*0.75)
        self.geometry(f'{self.app_with}x{self.app_height}+{(screen_with-self.app_with)//2}+{(screen_height-self.app_height)//2}')
        self.title('Device Registeration')
        self.resizable(False,False)
        self.columnconfigure(0, weight=1)
        # menu
        self.create_menu()
        # place header
        header = Header(callback=self.search_data)

        header_frame = tb.Frame(self)
        header_frame.grid(row=1, column=0, sticky='ew', pady=(3,8))
        for i in range(11):
            header_frame.columnconfigure(i, weight=1)
        
        tb.Label(header_frame,text='No#', font=('Trebuchet MS', 8,'bold'), width=4, bootstyle='primary.inverse', padding=3).grid(row = 0, column=0, sticky='w',padx=(0,8))
        headers = ['Device Name','Device Serial','Location','Submit Name','Countact', 'Sumbitter Date', 'Deliverer Name', 'Delivery Date']
        for col, header in enumerate(headers, 1):
            tb.Label(header_frame,text=header, font=('Trebuchet MS', 8,'bold'),width=16, anchor='w', padding=3, bootstyle='primary.inverse').grid(row = 0, column=col, padx=(0,10))
        tb.Label(header_frame,text='Action', font=('Trebuchet MS', 8,'bold'),width=17, anchor='center', padding=3, bootstyle='primary.inverse').grid(row = 0, column=9, columnspan=2, padx=(0,10))


        # items details
        self.items = Item()
        self.items = self.items.read()
        self.items_details = Content(items=self.items, autohide = True, bootstyle = 'rounded', height = self.app_height*0.85)

    def create_menu(self):
        # create menu to add new item, export data, import data
        menubar = Menu(self)
        m_menu = Menu(menubar, tearoff=0)
        m_menu.add_command(label='New', command=self.open_top_level)
        m_menu.add_command(label='Import Backup', command=self.open_import_backup)
        m_menu.add_command(label='Backup', command=Backup)
        m_menu.add_separator()
        m_menu.add_command(label='Close', command=self.quit)
        menubar.add_cascade(label="☰",menu=m_menu)
        self.config(menu=menubar)  
    
    def open_top_level(self):
        # open add new item window
        AddItem(self.update_app)
    def open_import_backup(self):
        ImportBackup(self.update_app)
    def update_app(self):
        # update content frame
        self.items_details.destroy()
        self.items = Item()
        self.items = self.items.read()
        self.items_details = Content(self.items)
    def search_data(self, search_data):
        self.items_details.destroy()
        self.items_details = Content(items=search_data)
    
class Header(tb.Frame):
    # place header that contain search-box and add-button
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, pady=(3,5), sticky='ew')
        self.callback = callback
        # column configuration
        self.columnconfigure(0, weight=1)
        # search part
        self.create_search()
        
        # create search options
    def create_search(self):
        search_frame = tb.Frame(self)
        search_frame.grid(row=0, column=0, sticky='e')
        # search-box can accept only serial number
        self.search_box = tb.Entry(search_frame, bootstyle = 'primary', width=50)
        self.search_box.grid(row=0, column=0, sticky='e')
        # search catagroy box
        self.criteria = ['Device Name', 'Device Serial', 'Location', 'Submit Date','Submitter Name', 'Submitter Contact', 'Deliverer Name', 'Delivery Date']
        self.search_creteria = tb.Combobox(search_frame, values=self.criteria, bootstyle='primary')
        self.search_creteria.grid(row=0, column=1, padx=1)
        self.search_creteria.current(0)
        # search-button
        search_button = tb.Button(search_frame, text='Search', bootstyle = 'primary', command=self.search)
        search_button.grid(row=0, column=2, padx=2)

    def search(self):
        # pass user search data to database
        search_text = self.search_box.get()
        search_criterion = self.search_creteria.get()
        if search_criterion in self.criteria:
            search_criterion = search_criterion.split()
            search_criterion = ['person' if (search_criterion[0] =='Submitter' or search_criterion[0]=='Deliverer') and cri =='Name' else cri.lower()  for cri in search_criterion]
            search_criterion = '_'.join(search_criterion)
            searched_item = Item()
            result = searched_item.search_data(search_text, search_criterion)
        else: result = list()
        self.callback(result)
        # backbutton
        self.back_btn = tb.Button(self, text='Back', bootstyle='primary', command=self.back)
        self.back_btn.grid(row=0, column=0, sticky='w', padx=3)

    # backbutton 
    def back(self):
        all_items = Item()
        all_items = all_items.read()
        self.back_btn.destroy()
        self.callback(all_items)
class Content(ScrolledFrame):
    # add details of items in main window
    def __init__(self, items,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=2, column=0, sticky='enws', padx=3)
        self.columnconfigure(0, weight=1)
        # create items
        self.items = items
        self.show_items(self.items)
    
    def show_items(self, item_details):
        # show all items in main whindo
        if len(item_details) ==0:
            tb.Label(self, text='Sorry, No data is available...!', bootstyle = 'dark').grid(row=0, column=0, padx=20, pady=50)
        for num, item_detail in enumerate(item_details, 1):
            self.show_single_item(num, item_detail)

    def show_single_item(self, num, item_detail):
        # show single item_detail in items list
        item_frame = tb.Frame(self)
        item_frame.grid(row=num, column=0, sticky='ew', pady=4)
        for i in range(11):
            item_frame.columnconfigure(i, weight=1)
        tb.Label(item_frame,text=str(num)+' - ', font=('Trebuchet MS', 8),width=4).grid(row = 0, column=0, sticky='w')
        for col ,detail in enumerate(item_detail,1):
            if detail is not None:
                detail = detail.title() if col > 2 else detail
            if col ==1:
                continue
            if col ==7 or col == 9:
                if detail is not None:
                    detail = detail.split()[0]
                else:
                    detail =''
            tb.Label(item_frame, text=detail, font=('Trebuchet MS', 8), width=16).grid(row=0, column=col-1, sticky='w')
        # update button
        update_icon = self.load_icon(r'assets\update.png')
        update_btn = tb.Button(item_frame, text='Update', image=update_icon, bootstyle = 'default.outline', command=lambda: self.open_top_level(item_detail))
        update_btn.grid(row=0, column=9, padx=5, sticky='w')
        update_btn.image = update_icon
        # Delete butotn
        delete_icon = self.load_icon(r'assets\delete.png')
        delete_btn = tb.Button(item_frame, text='X', image=delete_icon, bootstyle = 'danger.outline', command=lambda: self.open_delete(item_detail[0]))
        delete_btn.grid(row=0, column=10, padx=5, sticky='w')
        delete_btn.image = delete_icon
    
    def open_top_level(self, item_data):
        # open update window
        UpdateItem(item_data,self.update_app)

    def update_app(self):
        # update content frame
        self.clear_frame()
        self.items = Item()
        self.items = self.items.read()
        self.show_items(self.items)
    
    
    def load_icon(self, image_icon):
        # load icon for button
        image = Image.open(image_icon)
        image = image.resize((12,12))
        icon = ImageTk.PhotoImage(image)
        return icon
    
    def clear_frame(self):
        # clears all content of the main frame
        for widget in self.winfo_children():
            widget.destroy()  # Destroy all child widgets

    def open_delete(self, item_id):
        DeleteItem(item_id=item_id, callback=self.update_app)
    

if __name__ == '__main__':
    
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    root = App(themename='flatly')
    root.iconbitmap(bitmap=resource_path('assets\\img.ico'))
    root.mainloop()