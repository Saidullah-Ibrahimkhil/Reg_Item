import sqlite3
import os
import sys
#make sure the database is connect
def connect():
    # create connection
    global connection
    connection = sqlite3.connect(resource_path('reg_item.db'))
    cursor = connection.cursor()
    return cursor

def commit():
    # make sure changes have been don
    connection.commit()

def close():
    # close the connectin
    connection.close()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# testing
# connect()