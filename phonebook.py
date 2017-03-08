import sqlite3

class Phonebook():
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor() 
                                                
        self.cur.execute("CREATE TABLE pb_contact(contact_id INTEGER PRIMARY KEY, \
                                                  contact_name TEXT)")
        self.cur.execute("CREATE TABLE pb_number(number_id INTEGER PRIMARY KEY, \
                                                 number_string TEXT, \
                                                 contact_name TEXT, \
                                                 FOREIGN KEY(contact_name) \
                                                     REFERENCES pb_contact(contact_id))")
    def add_contact(self, contact_name):
        if contact_name in self.check_contact():
            print("CONTACT: {} is already in phonebook".format(contact_name))
            return False
        contact_sql_string = "INSERT INTO pb_contact(contact_name) VALUES ('{}')".format(contact_name)
        self.cur.execute(contact_sql_string)
        print("Succesfully added CONTACT: {}".format(contact_name))

    def show_contact(self):
        self.cur.execute("SELECT * FROM pb_contact")
        print(self.cur.fetchall())
        
    def check_contact(self):
        self.cur.execute("SELECT * FROM pb_contact")
        contact_list = self.cur.fetchall()
        contact_names = [i[1] for i in contact_list]
        return contact_names
        
    def add_number(self, number_string, contact_name):
        if number_string in self.check_number():
            print("NUMBER: {} is already in phonebook".format(number_string))
            return False
        elif contact_name not in self.check_contact():
            print("There is no CONTACT: {} in phonebook".format(contact_name),
                  "\nNumber was not added to phonebook",
                  "\nPossible CONTACTS are: {}".format(self.check_contact()))
            return False
        number_sql_string = "INSERT INTO pb_number VALUES (null, '{}', '{}')".format(number_string, contact_name)
        self.cur.execute(number_sql_string)
        print("Succesfully added NUMBER: {} to CONTACT: {}".format(number_string, contact_name))
    
    def check_number(self):
        self.cur.execute("SELECT * FROM pb_number")
        number_list = self.cur.fetchall()
        number_strings = [i[1] for i in number_list]
        return number_strings
                        
    def show_number(self):    
        self.cur.execute("SELECT * FROM pb_number")
        print(self.cur.fetchall())       

pb = Phonebook()
pb.add_contact("Freddie Mercury")
pb.add_contact("Freddie Mercury")
pb.show_contact()
pb.add_number("12123412", "Jon Snow")
pb.add_number("600900900", "Freddie Mercury")
pb.add_number("600900900", "Jon Snow")
pb.show_number()
pb.show_contact()
