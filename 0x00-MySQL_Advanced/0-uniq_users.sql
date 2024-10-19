-- Creating a 'users' table if it doesn't already exist
-- Attributes: 
-- id - integer, non-null, auto-increment, and primary key
-- email - a string (up to 255 chars), non-null, and must be unique
-- name - a string (up to 255 chars), optional
-- The script won't fail if the table is already present, suitable for use in any database.

CREATE TABLE IF NOT EXISTS users (
       id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
       email VARCHAR(255) NOT NULL UNIQUE,
       name VARCHAR(255)
);
