import sqlite3

conn = sqlite3.connect("database/secure_ai_vault.db")

cursor = conn.cursor()

cursor.execute(
"""
ALTER TABLE users
ADD COLUMN context_window INTEGER DEFAULT 2048
"""
)

cursor.execute(
"""
ALTER TABLE users
ADD COLUMN max_response_length INTEGER DEFAULT 1000
"""
)

cursor.execute(
"""
ALTER TABLE users
ADD COLUMN streaming_enabled BOOLEAN DEFAULT 1
"""
)

cursor.execute(
"""
ALTER TABLE users
ADD COLUMN reasoning_enabled BOOLEAN DEFAULT 0
"""
)

conn.commit()
conn.close()

print("Migration Complete")