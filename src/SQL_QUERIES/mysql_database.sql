CREATE DATABASE dao_mysql;

USE dao_mysql;

SELECT * FROM users;
SELECT * FROM permissions;

DROP TABLE permissions;
DROP TABLE users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    write_permission BOOLEAN,
    read_permission BOOLEAN,
    delete_permission BOOLEAN,
    post_permission BOOLEAN,
    export_permission BOOLEAN,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);