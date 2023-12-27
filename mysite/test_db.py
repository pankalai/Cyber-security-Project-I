import sqlite3
import os

# Creates agents.sqlite
# TMC has issues with binary files, so we will go around by creating it locally from the text dump.

db = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(200),
	admin boolean
);
INSERT INTO Users (name,admin) VALUES('user1',False);
INSERT INTO Users (name,admin) VALUES('user2',True);
COMMIT;
"""

if os.path.exists('users.sqlite'):
	print('users.sqlite already exists')
else:
	conn = sqlite3.connect('users.sqlite')
	conn.cursor().executescript(db)
	conn.commit()
