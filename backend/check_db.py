import sqlite3

connection = sqlite3.connect("database/dev.db")

tables = connection.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Tables:", tables)

users = connection.execute(
    "SELECT user_id, email FROM users"
).fetchall()

print("Users:", users)

revoked_tokens = connection.execute(
    "SELECT token_id, revoked_at FROM revoked_tokens"
).fetchall()

print("Revoked tokens:", revoked_tokens)

connection.close()