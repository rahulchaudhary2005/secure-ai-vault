import sqlite3

conn = sqlite3.connect(
    "database/secure_ai_vault.db"
)

cursor = conn.cursor()

columns = [

    "ALTER TABLE users ADD COLUMN context_window INTEGER DEFAULT 2048",

    "ALTER TABLE users ADD COLUMN max_response_length INTEGER DEFAULT 1000",

    "ALTER TABLE users ADD COLUMN streaming_enabled BOOLEAN DEFAULT 1",

    "ALTER TABLE users ADD COLUMN reasoning_enabled BOOLEAN DEFAULT 0"
]

for query in columns:

    try:
        cursor.execute(query)
        print("Added")
    except Exception as e:
        print(e)

conn.commit()
conn.close()

print("Done")