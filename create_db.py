import sqlite3

from faker import Faker

faker_instance = Faker()

# Create the mock i/o connect to write output.
connection = sqlite3.connect('mock_data.db')

# Pencile the data to the connection.
cursor = connection.cursor()

# Primary user profile table - contains fields relevant to the user.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        age INTEGER,
        zip_code INTEGER,
        zip_code_radius INTEGER,
        gaming_genre_id INTEGER,
        FOREIGN KEY (gaming_genre_id) REFERENCES gaming_genres(id)
    )
''')

# FK table that represents the genres available.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gaming_genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

# Mock gaming genres not available with Faker.
gaming_genres = ['RPG', 'Fantasy', 'FPS', 'SciFi', 'Strategy', 'Puzzle']

for genre in gaming_genres:
    cursor.execute('''
        INSERT INTO gaming_genres (name)
        VALUES (?)
    ''', (genre,))

# Commit the DB changes.
connection.commit()

# Close the connection.
connection.close()