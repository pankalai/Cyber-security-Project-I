import sqlite3
import os

# Creates agents.sqlite
# TMC has issues with binary files, so we will go around by creating it locally from the text dump.


db_script = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    ,first_name varchar(30) NOT NULL
    ,last_name varchar(30) NOT NULL
	,username varchar(30) NOT NULL
	,password varchar(30) NOT NULL
	,credit_card varchar(250) NOT NULL
	,admin boolean NOT NULL
);
INSERT INTO users (first_name,last_name,username,password,credit_card,admin) 
VALUES 
('sam','smith','sam','sam12','12345',False),
('tom','smith','tom','tom12','56789',False);


CREATE TABLE notes (
	user_id INTEGER NOT NULL
	,note varchar(200)
);
INSERT INTO notes (user_id, note)
VALUES 
(1,'note1'),
(2,'note2');

COMMIT;
"""


def create():
	db = 'db.sqlite'

	if os.path.exists(db):
		print(db + ' already exists')
	else:
		conn = sqlite3.connect(db)
		conn.cursor().executescript(db_script)
		conn.commit()
