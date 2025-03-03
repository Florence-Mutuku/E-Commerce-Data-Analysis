# %%
import os

sql_script = """ 
-- 1. Create the database
CREATE DATABASE IF NOT EXISTS ecommerce_db;

-- 2. Switch to the database
USE ecommerce_db;

-- 3. Create the products table
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(255),
    product_name VARCHAR(255),
    category TEXT,
    discounted_price DECIMAL(10, 2),
    actual_price DECIMAL(10, 2),
    discount_percentage DECIMAL(5, 2),
    rating DECIMAL(3, 2),
    rating_count INT,
    about_product TEXT,
    user_id VARCHAR(255),
    user_name VARCHAR(255),
    review_id VARCHAR(255),
    review_title TEXT,
    review_content TEXT,
    img_link TEXT,
    product_link TEXT
);

-- 4. Load the amazon.csv data (replace '/path/to/amazon.csv' with the actual path)
LOAD DATA INFILE '/path/to/amazon.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_name, category, @discounted_price, @actual_price, @discount_percentage, @rating, @rating_count, about_product, user_id, user_name, review_id, review_title, review_content, img_link, product_link)
SET discounted_price = NULLIF(REPLACE(@discounted_price, '₹', ''), ''),
    actual_price = NULLIF(REPLACE(REPLACE(@actual_price, '₹', ''), ',', ''), ''),
    discount_percentage = NULLIF(REPLACE(@discount_percentage, '%', ''), ''),
    rating = NULLIF(@rating, ''),
    rating_count = NULLIF(REPLACE(@rating_count, ',', ''), '');
"""

file_path = "ecommerce_setup.sql"

try:
    with open(file_path, "w", encoding="utf-8") as sql_file:
        sql_file.write(sql_script)
    print(f"SQL script saved to {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

# Example of how to get user input for the file path (optional, but recommended)
csv_file_path = input("Enter the full path to your amazon.csv file: ")

# Replace placeholder in the SQL script
with open(file_path, "r", encoding="utf-8") as file:
    sql_content = file.read()

updated_sql_content = sql_content.replace("'/path/to/amazon.csv'", f"'{csv_file_path}'")

with open(file_path, "w", encoding="utf-8") as file:
    file.write(updated_sql_content)

print(f"SQL script updated with your amazon.csv path.")

print("Remember to execute the SQL script using a MySQL client.")


