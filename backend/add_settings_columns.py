import sqlite3

conn = sqlite3.connect(
    "database/secure_ai_vault.db"
)

cursor = conn.cursor()

queries = [

    """
    ALTER TABLE users
    ADD COLUMN context_window INTEGER DEFAULT 2048
    """,

    """
    ALTER TABLE users
    ADD COLUMN max_response_length INTEGER DEFAULT 1000
    """,

    """
    ALTER TABLE users
    ADD COLUMN streaming_enabled BOOLEAN DEFAULT 1
    """,

    """
    ALTER TABLE users
    ADD COLUMN reasoning_enabled BOOLEAN DEFAULT 0
    """
]

for query in queries:

    try:

        cursor.execute(query)

        print("Added column successfully")

    except Exception as e:

        print("Skipped:", e)

conn.commit()

conn.close()

print("Database update complete")