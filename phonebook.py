import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE pb_group(group_id INTEGER PRIMARY KEY, group_name TEXT)")
cursor.execute("INSERT INTO pb_group(group_name) VALUES ('Family')")
cursor.execute("INSERT INTO pb_group(group_name) VALUES ('Friends')")
cursor.execute("INSERT INTO pb_group(group_name) VALUES ('Others')")
cursor.execute("SELECT * FROM pb_group")
print(cursor.fetchall())

cursor.execute("CREATE TABLE pb_contact(contact_id INTEGER PRIMARY KEY, contact_name TEXT, group_name TEXT, FOREIGN KEY(group_name) REFERENCES pb_group(group_id))")
cursor.execute("INSERT INTO pb_contact VALUES (null, 'Customer Service', 'Others')")
cursor.execute("INSERT INTO pb_contact VALUES (null, 'Taxi Duck', null)")
cursor.execute("SELECT * FROM pb_contact")
print(cursor.fetchall())

cursor.execute("CREATE TABLE pb_number(number_id INTEGER PRIMARY KEY, number_string INT, contact_name TEXT, FOREIGN KEY(contact_name) REFERENCES pb_contact(contact_id))")
cursor.execute("INSERT INTO pb_number VALUES (null, '625-800-688', 'Customer Service')")
cursor.execute("INSERT INTO pb_number VALUES (null, '714-295-123', 'Customer Service')")
cursor.execute("SELECT * FROM pb_number WHERE contact_name='Customer Service'")
print(cursor.fetchall())

cursor.close()