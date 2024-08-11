-- A script that prepares a MySQL server for the project
-- creates a project testing database: hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- creating new user: hbnb_test with all privileges on the db hbnb_test_db
-- new user password: hbnb_test_pwd if it dosen't exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- granting the SELECT privilege for the user hbnb_test on the db performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
-- granting all privileges to the new user on hbnb_test_db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
