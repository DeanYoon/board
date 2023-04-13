import sqlite3

conn = sqlite3.connect('notice_board.db')
cursor = conn.cursor()

# create posts table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        created_at TEXT,
        views INTEGER,
        user_id INTEGER,
        board_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(board_id) REFERENCES boards(id)
    )
''')

# Example data to insert
new_post = ('My new post', 'This is the content of my new post.', '2022-04-03 12:00:00', 0, 1, 1)

# Insert the data into the table
cursor.execute('INSERT INTO posts (title, content, created_at, views, user_id, board_id) VALUES (?, ?, ?, ?, ?, ?)', new_post)
conn.commit()

# Close the connection
conn.close()
