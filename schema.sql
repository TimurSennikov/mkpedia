DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users ( 
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin BOOL DEFAULT 0,

    profile_description TEXT,
    commit_n NUMBER
);

CREATE TABLE IF NOT EXISTS queue (
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
    title TEXT UNIQUE NOT NULL,
    data TEXT NOT NULL,
    made_by TEXT NOT NULL
);

INSERT INTO users VALUES("root", "toor", 1, "Рут-пользователь, мега-крут.", 0)
