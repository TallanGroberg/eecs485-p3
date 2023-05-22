PRAGMA foreign_keys = ON;

CREATE TABLE users (
    username TEXT PRIMARY KEY CHECK(length(username) <= 20),
    fullname TEXT CHECK(length(fullname) <= 40),
    email TEXT CHECK(length(email) <= 40),
    filename TEXT CHECK(length(filename) <= 64),
    password TEXT CHECK(length(password) <= 256),
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    postid INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT CHECK(length(filename) <= 64),
    owner TEXT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE following (
    username1 TEXT,
    username2 TEXT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(username1, username2),
    FOREIGN KEY(username1) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY(username2) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE comments (
    commentid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT,
    postid INTEGER,
    text TEXT CHECK(length(text) <= 1024),
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY(postid) REFERENCES posts(postid) ON DELETE CASCADE
);

CREATE TABLE likes (
    likeid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT,
    postid INTEGER,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY(postid) REFERENCES posts(postid) ON DELETE CASCADE
);
