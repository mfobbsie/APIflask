# Flask REST API with SQLAlchemy, Marshmallow, and MySQL
## Author
Mary Fobbs‑Guillory

## Table of Contents
Introduction

Features

Technologies Used

Database Structure

Installation

Running the Application

API Endpoints

Testing the API

Screenshots (Placeholders)

Collaborators

## Introduction
This project is a fully functional RESTful API built with Flask, SQLAlchemy, and Marshmallow. It manages Users, Orders, and Products, including a many‑to‑many relationship between orders and products. The API supports full CRUD operations, relational queries, and serialization using Marshmallow schemas.

The backend is powered by a MySQL database, and all endpoints were tested using Postman. MySQL Workbench was used to design, inspect, and validate the database tables and relationships.

This project demonstrates clean API design, relational modeling, schema validation, and structured backend development.

## Features
CRUD operations for Users, Products, and Orders

Many‑to‑many relationship between Orders and Products

One‑to‑many relationship between Users and Orders

Marshmallow validation and serialization

Error handling for invalid payloads

Helper utilities for updates, deletes, and session commits

Endpoints for linking products to orders

Custom join queries to return combined order‑product data

Health check endpoints

## Technologies Used
Flask – Web framework for building the API

Flask‑SQLAlchemy – ORM for database modeling

SQLAlchemy Declarative Base – Modern typed model definitions

Flask‑Marshmallow / Marshmallow – Serialization and validation

MySQL – Relational database

MySQL Workbench – Database visualization and management

Postman – API testing and request simulation

## Database Structure
The API uses three main tables:

Users

One‑to‑many relationship with Orders

Orders

Belongs to a User

Many‑to‑many relationship with Products

Products

Many‑to‑many relationship with Orders

A join table (order_product) links orders and products.

## Installation
1. Clone the repository
bash
git clone https://github.com/yourusername/your-repo-name
cd your-repo-name
2. Create a virtual environment
bash
python -m venv venv
3. Activate the environment
Mac/Linux

bash
source venv/bin/activate
Windows

bash
venv\Scripts\activate
4. Install dependencies
bash
pip install -r requirements.txt
5. Configure your MySQL connection
Update this line in the code with your credentials:

python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/flask_api_db'
6. Create the database
In MySQL Workbench:

sql
CREATE DATABASE flask_api_db;
Running the Application
bash
python app.py
The API will run at:

Code
http://localhost:5050
## API Endpoints
Users
POST /api/users – Create user

GET /api/users – Get all users

GET /api/users/<id> – Get user by ID

PUT /api/users/<id> – Update user

DELETE /api/users/<id> – Delete user

Products
POST /api/products – Create product

GET /api/products – Get all products

GET /api/products/<id> – Get product by ID

PUT /api/products/<id> – Update product

DELETE /api/products/<id> – Delete product

Orders
POST /api/orders – Create order

GET /api/orders – Get all orders

GET /api/orders/<id> – Get order by ID

PUT /api/orders/<id>/products – Add products to order

GET /api/orders/<id>/products – Get products in an order

DELETE /api/orders/<id> – Remove product from order

Order‑Product Join Data
GET /api/order-products – All order‑product links

GET /api/orders/<id>/order-products – Links for a specific order

Health Check
/

/health

## Testing the API
All endpoints were tested using Postman, including:

Creating and updating users

Adding products to orders

Validating error responses

Inspecting JSON payloads

Testing relational queries

MySQL Workbench was used to:

View and verify table creation

Inspect relationships

Confirm join table entries

Run manual SQL queries for debugging

## Screenshots 

Postman: Create User
<img width="927" height="665" alt="Screenshot 2026-03-04 at 10 26 14 AM" src="https://github.com/user-attachments/assets/e7bffe61-bf6f-4928-8459-3afa028e4cdd" />


Postman: Add Products 
<img width="925" height="651" alt="Screenshot 2026-03-04 at 10 23 32 AM" src="https://github.com/user-attachments/assets/e17f8e07-1ad3-4f2f-b50a-0c8807f86ccb" />


MySQL Workbench: Products Table
<img width="316" height="412" alt="Screenshot 2026-03-04 at 10 20 23 AM" src="https://github.com/user-attachments/assets/d85aefc8-671f-4846-ab89-c6d39f6075e8" />


## Collaborators
Coding Temple Bootcamp

Microsoft Copilot
