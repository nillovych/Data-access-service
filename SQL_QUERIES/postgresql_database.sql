CREATE DATABASE dao_postgres;

SELECT * FROM users;
SELECT * FROM permissions;

DROP TABLE permissions;
DROP TABLE users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    write_permission BOOLEAN,
    read_permission BOOLEAN,
    delete_permission BOOLEAN,
    post_permission BOOLEAN,
    export_permission BOOLEAN
);