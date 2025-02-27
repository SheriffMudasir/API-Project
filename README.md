# Little Lemon Restaurant API

## Project Overview
This is the backend API for Little Lemon Restaurant, developed as a capstone project for Meta's API Development course on Coursera. The API provides functionality for menu management, user authentication, order processing, and delivery management.

## Features
- User Authentication and Authorization
- Role-based access control (Manager, Delivery Crew, Customer)
- Menu Items Management
- Shopping Cart Functionality
- Order Processing
- Category Management
- API Throttling
- Pagination
- Filtering and Searching

## Tech Stack
- Django 5.1.5
- Django REST Framework
- SQLite3
- Djoser (Authentication)
- Django-filter

## API Endpoints

### Authentication Endpoints
- `/auth/users/` - User registration
- `/auth/users/me/` - Retrieve/update user information
- `/auth/token/login/` - Obtain authentication token
- `/auth/token/logout/` - Logout (invalidate token)

### Menu Endpoints
- `/api/menu-items/` - List, create, update, delete menu items
- `/api/category/` - Manage menu categories

### Cart Endpoints
- `/api/cart/menu-items/` - Shopping cart management

### Order Endpoints
- `/api/orders/` - Order management
- `/api/order-items/` - Order items management

### User Management Endpoints
- `/api/groups/manager/users/` - Manager user management
- `/api/users