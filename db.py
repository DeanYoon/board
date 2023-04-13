import sqlite3

# Connect to the database file (creates it if it doesn't exist)
conn = sqlite3.connect('notice_board.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create users table
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')

# create posts table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        created_at TEXT,
        views INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(board_id) REFERENCES boards(id)
    )
''')

# # create comments table
# cursor.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, post_id INTEGER, user_id INTEGER, content TEXT, created_at TEXT, likes INTEGER)')
# # create boards table
# cursor.execute('CREATE TABLE IF NOT EXISTS boards (id INTEGER PRIMARY KEY, name TEXT)')

# # Insert a row into the table
# #cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('Alice', 'ajkdbaskjdnsakndsakjndlaskjnd'))



# # Insert example data into the users table
# cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('Alice', 'ajkdbaskjdnsakndsakjndlaskjnd'))
# cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('Bob', 'bdkjbfkjbekjbck'))

# # Insert example data into the boards table
# cursor.execute('INSERT INTO boards (name) VALUES (?)', ('Programming',))
# cursor.execute('INSERT INTO boards (name) VALUES (?)', ('Music',))

# Insert example data into the posts table
cursor.execute('INSERT INTO posts (title, content, user_id,  created_at, views, board_id) VALUES (?, ?, ?, ?, ?, ?)',
               ('My First Post', 'This is the content of my first post.', 1,  '2022-04-01 12:00:00', 10, 1))
cursor.execute('INSERT INTO posts (title, content, user_id,  created_at, views, board_id) VALUES (?, ?, ?, ?, ?, ?)',
               ('My Second Post', 'This is the content of my second post.', 2,  '2022-04-02 10:00:00', 5, 2))

# Insert example data into the comments table
# cursor.execute('INSERT INTO comments (post_id, user_id, content, created_at, likes) VALUES (?, ?, ?, ?, ?)',
#                (1, 2, 'Great post!', '2022-04-01 13:00:00', 2))
# cursor.execute('INSERT INTO comments (post_id, user_id, content, created_at, likes) VALUES (?, ?, ?, ?, ?)',
#                (1, 1, 'Thanks for sharing!', '2022-04-01 14:00:00', 5))



# Commit the changes
conn.commit()

# Query the table and print the results
# cursor.execute('SELECT * FROM users')
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

# Close the connection
conn.close()
