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
            return True
        contact_sql_string = "INSERT INTO pb_contact(contact_name) VALUES ('{}')".format(contact_name)
        self.cur.execute(contact_sql_string)
        print("Succesfully added CONTACT: {}".format(contact_name))
        return False

    def show_contact(self):
        self.cur.execute("SELECT * FROM pb_contact")
        print(self.cur.fetchall())
        
    def check_contact(self):
        self.cur.execute("SELECT * FROM pb_contact")
        contact_list = self.cur.fetchall()
        contact_names = [i[1] for i in contact_list]
        return contact_names
		
    def delete_contact(self, contact_name, delete_message = True):
        if contact_name not in self.check_contact():
            print("There is no such CONTACT: {} in phonebook".format(contact_name))
            return False
        self.cur.execute("SELECT number_string FROM pb_number WHERE contact_name='{}'".format(contact_name))
        number_strings = self.cur.fetchall()
        for i in range(len(number_strings)):
            self.delete_number(number_strings[i][0], delete_contact = True)
        self.cur.execute("DELETE FROM pb_contact WHERE contact_name='{}'".format(contact_name))
        if delete_message is True:
            print("Succesfully deleted CONTACT '{}' and all its numbers".format(contact_name))
        return False
        
    def update_contact(self, old_contact_name, new_contact_name):
        if old_contact_name not in self.check_contact():
            print("There is no such CONTACT: {} in phonebook".format(old_contact_name))
            return False
        if new_contact_name in self.check_contact():
            print("CONTACT: {} is already in phonebook".format(new_contact_name))
            return False
        self.cur.execute("UPDATE pb_contact SET contact_name='{}' WHERE contact_name='{}'".format(new_contact_name, old_contact_name))
        self.cur.execute("SELECT number_string FROM pb_number WHERE contact_name='{}'".format(old_contact_name))
        number_strings = self.cur.fetchall()
        for i in range(len(number_strings)):
            self.reasign_number(number_strings[i][0], new_contact_name, edit_contact = True)
        print("Succesfully updated CONTACT: {} to {}".format(old_contact_name, new_contact_name))		
        return False

    def add_number(self, number_string, contact_name):
        if number_string in self.check_number():
            print("NUMBER: {} is already in phonebook".format(number_string))
            return False
        elif contact_name not in self.check_contact():
            print("There is no such CONTACT: {} in phonebook".format(contact_name),
                  "\nNumber was not added to phonebook",
                  "\nPossible CONTACTS are: {}".format(self.check_contact()))
            return False
        number_sql_string = "INSERT INTO pb_number VALUES (null, '{}', '{}')".format(number_string, contact_name)
        self.cur.execute(number_sql_string)
        print("Succesfully added NUMBER: {} to CONTACT: {}".format(number_string, contact_name))
        return False
    
    def check_number(self):
        self.cur.execute("SELECT * FROM pb_number")
        number_list = self.cur.fetchall()
        number_strings = [i[1] for i in number_list]
        return number_strings
        
    def contact_with_no_number(self, contact_name):
        self.cur.execute("SELECT number_string FROM pb_number WHERE contact_name='{}'".format(contact_name))
        number_list = self.cur.fetchall()
        if len(number_list) == 0:
            return True
        else:
            return False
                        
    def show_number(self):    
        self.cur.execute("SELECT * FROM pb_number")
        print(self.cur.fetchall())

    def delete_number(self, number_string, delete_contact = False):
        if number_string not in self.check_number():
            print("There is no such NUMBER: {} in phonebook".format(number_string))
            return False
        self.cur.execute("SELECT contact_name FROM pb_number WHERE number_string='{}'".format(number_string))
        contact_name = self.cur.fetchone()[0]
        self.cur.execute("SELECT * FROM pb_number WHERE contact_name='{}'".format(contact_name))
        number_list = self.cur.fetchall()
        if (len(number_list) == 1) and (delete_contact is False):
            print("NUMBER: '{}' is the only number of CONTACT: '{}'. It can not be deleted. You should first delete CONTACT '{}' instead".format(number_string, contact_name, contact_name))
            return False
        self.cur.execute("DELETE FROM pb_number WHERE number_string='{}'".format(number_string))
        if delete_contact is False:
            print("Succesfully deleted NUMBER: '{}'".format(number_string))
        return False

    def update_number(self, old_number_string, new_number_string):
        if old_number_string not in self.check_number():
            print("There is no such NUMBER: {} in phonebook".format(old_number_string))
            return False
        if new_number_string in self.check_number():
            print("NUMBER: {} is already in phonebook".format(new_number_string))
            return False
        self.cur.execute("UPDATE pb_number SET number_string='{}' WHERE number_string='{}'".format(new_number_string, old_number_string))
        print("Succesfully updated NUMBER: {} to {}".format(old_number_string, new_number_string))
        return False

    def reasign_number(self, number_string, contact_name, edit_contact = False):
        if number_string not in self.check_number():
            print("There is no such NUMBER: {} in phonebook".format(number_string))
            return False        
        elif contact_name not in self.check_contact():
            print("There is no such CONTACT: {} in phonebook".format(contact_name))
            return False
        self.cur.execute("SELECT * FROM pb_number WHERE contact_name='{}'".format(contact_name))
        number_list = self.cur.fetchall()
        if (len(number_list) == 1):
            print("NUMBER: '{}' is the only number of CONTACT: '{}'. It can not be reasigned. You should first delete CONTACT '{}' instead".format(number_string, contact_name, contact_name))
            return False
        self.cur.execute("UPDATE pb_number SET contact_name='{}' WHERE number_string='{}'".format(contact_name, number_string))
        if edit_contact is False:
            print("Succesfully reasigned NUMBER: {} to CONTACT: {}".format(number_string, contact_name))
        return False

    def show_phonebook(self):
        print("\nPHONEBOOK STARTS BELOW")
        contact_names = self.check_contact()
        for i in range(len(contact_names)):
            self.cur.execute("SELECT number_string FROM pb_number WHERE contact_name='{}'".format(contact_names[i]))
            number_strings = self.cur.fetchall()
            for j in range(len(number_strings)):
                if j == 0:
                    print("\n" + contact_names[i] + (" " * 3) + number_strings[j][0])
                else:
                    print(" " * len(contact_names[i]) + (" " * 3) + number_strings[j][0])
        print("\nPHONEBOOK ENDS HERE")
        return False

pb = Phonebook()

print("\nExemplary phonebook will be created for project presentation purposes only.\n\
Terminal outputs below are results of written functions execution.\n")
pb.add_contact("Freddie Mercury")
pb.add_contact("Jon Snow")
pb.add_contact("James Bond")
pb.add_number("600-900-900", "Freddie Mercury")
pb.add_number("800-300-400", "Freddie Mercury")
pb.add_number("85-230-72", "Jon Snow")
pb.add_number("405-200-999", "James Bond")
pb.add_number("72-601-88", "James Bond")
pb.add_number("326-400-105", "James Bond")

def menu():
    print("\n-------------------------------------")
    print("Command line menu of PHONEBOOK")
    print("Please, input the specified number and press enter to choose an option:")	   
    print("\n\
    0 - Show phonebook\n\
    1 - Add new contact and its number to phonebook\n\
    2 - Add new number and assign it to contact\n\
    3 - Delete contact and all its numbers\n\
    4 - Delete number\n\
    5 - Update contact into new contact name\n\
    6 - Update number into new one\n\
    7 - Reasign existing number into different contact\n\
    8 - Exit phonebook application\n")
    selection = input("Choose an option: ")
    print("-------------------------------------")
    return selection

def selection_event(pb, sel):
    if sel == "0":
        stop = pb.show_phonebook()
        return stop
    elif sel == "1":
        contact_name = input("\nContact name: ")
        stop = pb.add_contact(contact_name)
        if stop is True:
            return False
        number_string = input("Phone number: ")
        stop = pb.add_number(number_string, contact_name)
        if pb.contact_with_no_number(contact_name) is True:
            print("CONTACT {} added above was deleted due to phone number error".format(contact_name))        
            pb.delete_contact(contact_name, delete_message = False)
        return stop
    elif sel == "2":
        number_string = input("\nPhone number: ")
        contact_name = input("Contact name: ")
        stop = pb.add_number(number_string, contact_name)
        return stop
    elif sel == "3":
        contact_name = input("\nContact name: ")
        stop = pb.delete_contact(contact_name)
        return stop
    elif sel == "4":
        number_string = input("\nPhone number: ")
        stop = pb.delete_number(number_string)
        return stop
    elif sel == "5":
        old_contact_name = input("\nOld contact name: ")
        new_contact_name = input("New contact name: ")
        stop = pb.update_contact(old_contact_name, new_contact_name)
        return stop
    elif sel == "6":
        old_number_string = input("\nOld phone number: ")
        new_number_string = input("New phone number: ")
        stop = pb.update_number(old_number_string, new_number_string)
        return stop
    elif sel == "7":
        number_string = input("\nPhone number: ")
        contact_name = input("New contact name: ")
        stop = pb.reasign_number(number_string, contact_name)
        return stop
    elif sel == "8":
        print("\nBye!\n")
        return True

stop = False
while stop is False:     
    sel = menu()
    stop = selection_event(pb, sel)
