--Create database/schema event_scheduler

CREATE DATABASE IF NOT EXISTS event_scheduler;

--Use the event_scheduler(schema)
USE event_scheduler;

-- Create the 'users' table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,   -- Unique identifier for each user
    first_name VARCHAR(50) NOT NULL,          -- User's first name
    last_name VARCHAR(50) NOT NULL,           -- User's last name
    email_address VARCHAR(100) NOT NULL UNIQUE,    -- User's email address
    username VARCHAR(50) NOT NULL UNIQUE,     -- User's chosen username
    password VARCHAR(255) NOT NULL,           -- User's password (should be hashed)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of user creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Timestamp of last update
);

-- Create the 'events' table
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each event
    user_id INT NOT NULL,                     -- ID of the user who created the event
    event_name VARCHAR(100) NOT NULL,         -- Name of the event
    event_date DATE NOT NULL,                 -- Date of the event
    event_time TIME,                          -- Time of the event
    description TEXT,                         -- Description of the event
    location VARCHAR(255),                    -- Location of the event
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of event creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp of last update
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE -- Link to 'users' table
);