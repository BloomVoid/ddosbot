import sqlite3

# Connect to the SQLite database
database = sqlite3.connect("Bloom.sqlite")
cursor = database.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT,
#         first_name TEXT,
#         second_name TEXT,
#         bio TEXT,
#         number TEXT,
#         contact_first_name TEXT,
#         contact_phone_number TEXT,
#         started INTEGER DEFAULT 0
#     )
# ''')

async def add_user(cursor, message, contact):
    cursor.execute("SELECT id FROM users WHERE id=?", (message.chat.id,))
    user = cursor.fetchone()
    if not user:
        first_name = contact.first_name if contact else None
        phone_number = contact.phone_number if contact else None
        cursor.execute("INSERT INTO users (id, username, first_name, second_name, bio, number, contact_first_name, contact_phone_number) VALUES (?,?,?,?,?,?,?,?)",
                       (message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name,
                        message.chat.bio, '', first_name, phone_number))
        cursor.connection.commit()

# Function to add a number to the user
def add_number(user_id, first_name, number):
    cursor.execute('''
        UPDATE users SET number=?, contact_first_name=?, contact_phone_number=? WHERE id=?
    ''', (number, first_name, number, user_id))
    database.commit()
