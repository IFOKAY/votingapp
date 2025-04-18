-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS voting_app;

-- Use the database
USE voting_app;

-- Create the users table if it doesn't already exist
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Create the votes table if it doesn't already exist
CREATE TABLE IF NOT EXISTS votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    team VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Optional: Insert some initial data for testing
INSERT INTO users (username, password) VALUES ('testuser1', 'password1');
INSERT INTO users (username, password) VALUES ('testuser2', 'password2');

-- Optional: Insert some vote data for testing
INSERT INTO votes (user_id, team) VALUES (1, 'Team A');
INSERT INTO votes (user_id, team) VALUES (2, 'Team B');
