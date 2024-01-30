import random
import sqlite3

from faker import Faker

faker_instance = Faker()

# Prompt the user for the number of users to generate
num_users = int(input("Enter the number of user profiles to generate: "))

# Prompt to empty the database.
overwrite_choice = input("Do you want to drop existing data? (yes/no): ").lower()

# Create the mock i/o connect to write output.
connection = sqlite3.connect('mock_data.db')

# Pencile the data to the connection.
cursor = connection.cursor()

# Check if the user wants to overwrite the database.
if overwrite_choice == 'yes':
    cursor.execute('DROP TABLE IF EXISTS user_profiles')
    cursor.execute('DROP TABLE IF EXISTS gaming_genres')
    connection.commit()

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

# Random virginia zip codes.
virginia_zip_codes = [
    "22030", "22150", "22201", "22301", "22901",
    "23005", "23111", "23220", "23320", "23456",
    "23505", "23601", "24060", "24141", "24502"
]

# Just some random radius values someone may select for what range their searching within.
virginia_zip_code_radius = [ 10, 25, 50, 100, 200 ]

for _ in range(num_users):
    username = faker_instance.user_name()
    email = faker_instance.email()
    age = faker_instance.random_int(min=18, max=60)
    gaming_genre_id = faker_instance.random_int(min=1, max=len(gaming_genres))
    zip_code = random.choice(virginia_zip_codes)
    zip_code_radius = random.choice(virginia_zip_code_radius)
    
    cursor.execute('''
        INSERT INTO user_profiles (username, email, age, gaming_genre_id, zip_code, zip_code_radius)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, email, age, gaming_genre_id, zip_code, zip_code_radius))

# Commit the DB changes.
connection.commit()

# Close the connection.
connection.close()

# Display a message indicating the process is complete
print(f"{num_users} user profiles generated and committed to the database.")