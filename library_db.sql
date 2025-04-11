CREATE DATABASE library_db;
USE library_db;
-- Create admin table
CREATE TABLE Admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(100)
);

-- Create member table
CREATE TABLE Member (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(100)
);
ALTER TABLE Member ADD COLUMN email VARCHAR(255);

CREATE TABLE Book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publisher VARCHAR(255),
    quantity INT
);
ALTER TABLE Book
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST,
ADD COLUMN title VARCHAR(255) NOT NULL,
ADD COLUMN author VARCHAR(255) NOT NULL,
ADD COLUMN publisher VARCHAR(255) NOT NULL,
ADD COLUMN quantity INT NOT NULL;

CREATE TABLE Member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255),
    password VARCHAR(255)
);
CREATE TABLE Admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);
CREATE TABLE Vendor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    contact VARCHAR(100)
);

CREATE TABLE Reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    member_id INT,
    reservation_date DATE,
    FOREIGN KEY (book_id) REFERENCES Book(id),
    FOREIGN KEY (member_id) REFERENCES Member(id)
);
CREATE TABLE Fine (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    amount DECIMAL(10, 2),
    reason TEXT,
    FOREIGN KEY (member_id) REFERENCES Member(id)
);
ALTER TABLE Fine ADD COLUMN date_assessed DATE;



-- Add dummy data
INSERT INTO Admin (username, password) VALUES ('admin', 'admin123');
INSERT INTO Member (username, password) VALUES ('user1', 'user123');

CREATE TABLE Author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Publisher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE Employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);



INSERT INTO Author (name) VALUES ('J.K. Rowling'), ('George Orwell'), ('Agatha Christie');

INSERT INTO Publisher (name) VALUES ('Penguin Books'), ('HarperCollins'), ('Oxford University Press');

INSERT INTO Employee (username, email, password)
VALUES 
('employee1', 'employee1@example.com', 'employee123'),
('employee2', 'employee2@example.com', 'employee123');
