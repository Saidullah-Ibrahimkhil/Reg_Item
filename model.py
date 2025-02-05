# connect to sqlite3 and reg_item database
import db_connection as connection
import sqlite3
from datetime import datetime

class Item:
    # this class will be responsible for data and database operations
    def query_execute(self, query, user_data):
        # execute queries based on user input data
        cursor = connection.connect()
        if cursor.execute(query,user_data):
            connection.commit()
            connection.close()
            return True
        connection.close()
        return False
    
    def read(self):
        # select data items data from database
        select_query = 'SELECT \
                        id,\
                        device_name, \
                        device_serial, \
                        location, \
                        submitter_person, \
                        submitter_contact, \
                        submit_date, \
                        deliverer_person, \
                        delivery_date \
                        FROM items order by delivery_date DESC Nulls first, submit_date DESC'
        cursor = connection.connect()
        items = cursor.execute(select_query).fetchall()
        connection.close()
        return items
    
    def create(self, item_data):
        # insert items data into database
        # item_date should be in tuple form
        create_query = 'INSERT INTO items \
                (device_name, device_serial, location, submitter_person, submitter_contact, submit_date, deliverer_person, delivery_date) \
                VALUES(?,?,?,?,?,?,?,?)'
        return self.query_execute(create_query, item_data)
    
    def update(self, update_data):
        # update data into database
        # update data should be in dictionary
        update_query= 'UPDATE items SET \
                device_name = :device_name, \
                device_serial=:device_serial, \
                location = :location, \
                submitter_person = :submitter_person, \
                submitter_contact = :submitter_contact, \
                submit_date = :submit_date, \
                deliverer_person = :deliverer_person, \
                delivery_date = :delivery_date \
                WHERE id = :id'
        return self.query_execute(update_query, update_data)
    
    def delete(self, id):
        # delete tha passed data from items
        #input data should be integer
        delete_query = 'DELETE FROM items WHERE id= :id'
        return self.query_execute(delete_query, {'id': id})
    
    def search_data(self, search_text, search_criterion):
        if search_criterion == 'submit_date' or search_criterion == 'delivery_date':
            search_text = search_text.split('-')
            if len(search_text) == 3:
                search_text = datetime(int(search_text[0]), int(search_text[1]), int(search_text[2]))
        select_query = f'SELECT \
                        id,\
                        device_name, \
                        device_serial, \
                        location, \
                        submitter_person, \
                        submitter_contact, \
                        submit_date, \
                        deliverer_person, \
                        delivery_date \
                        FROM items where {search_criterion} like "%{search_text}%" order by delivery_date DESC Nulls first, submit_date DESC'
        cursor = connection.connect()
        items = cursor.execute(select_query).fetchall()
        connection.close()
        return items
    
    def export_database(self, backup_path):
        # backup from database
        try:
            source_connection = sqlite3.connect(connection.resource_path('reg_item.db'))
            backup_connection = sqlite3.connect(connection.resource_path(backup_path))
            with backup_connection:
                source_connection.backup(backup_connection)
            
            backup_connection.close()
            source_connection.close()
            
            return True
        
        except Exception as e:
            return False
    def import_database(self, selected_file):
        try:
            source_connection = sqlite3.connect(connection.resource_path('reg_item.db'))
            imported_file = sqlite3.connect(connection.resource_path(selected_file))
            select_query = 'SELECT \
                        id,\
                        device_name, \
                        device_serial, \
                        location, \
                        submitter_person, \
                        submitter_contact, \
                        submit_date, \
                        deliverer_person, \
                        delivery_date \
                        FROM items'
            
            items = imported_file.execute(select_query).fetchall()
            for item in items:
                insert_query = 'INSERT OR REPLACE INTO items (\
                                    id, \
                                    device_name,\
                                    device_serial,\
                                    location,\
                                    submitter_person,\
                                    submitter_contact,\
                                    submit_date,\
                                    deliverer_person,\
                                    delivery_date\
                                    ) values(?,?,?,?,?,?,?,?,?)'
                source_connection.execute(insert_query, item)
            source_connection.commit()
            source_connection.close()
            imported_file.close()
            return True
        except Exception as e:
            return False

