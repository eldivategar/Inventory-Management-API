# Inventory Management API

## Project Overview
This is a simple RESTful API for managing inventory in a retail store. The API allows users to perform CRUD operations on products and categories. The project is built using pure Python with SQLite as the database.

## Setup Instructions

### Prerequisites
- Python 3.x
- SQLite3
- `curl` or `Postman` or `Insomnia` for testing endpoints

### Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/eldivategar/Inventory-Management-API.git
   cd inventory-management-api

2. **Setup Virtual Environment**
    ```bash
    python -m venv venv
    source venv\Script\activate

4. **Install Requirements**
    ```bash
    pip install -r requirements.txt

5. **Create .env File**
    ```bash
    DATABASE_PATH=path/to/database (e.g. database/ima.db)

6. **Run the Server**
    ```bash
    python main.py

7. **Run the unittest**
    ```bash
    pytest
    # The test runs automatically

## API Documentation

### Endpoints

#### 1. **Get All Items**
   - **Endpoint:** `/items`
   - **Method:** `GET`
   - **Description:** Fetches a list of all items.
   - **Response Example:**
     ```json
     {
      "items": [
          {
              "id": 1,
              "category": {
                  "id": 1,
                  "name": "Electronics"
              },
              "name": "Air Conditioner",
              "description": "",
              "price": 10000.0,
              "created_at": "2024-10-18 01:00:11"
          }
      ]
     }
     ```

#### 2. **Create New Items**
   - **Endpoint:** `/items`
   - **Method:** `POST`
   - **Description:** Creates a new item.
   - **Request Body Example:**
     ```json
     {
        "category_id": 1,
        "name": "Air Conditioner",
        "description": "",
        "price": 10000
     }  
     ```
   - **Response Example:**
     ```json
      {
        "item": {
            "id": 1,
            "category": {
                "id": 1,
                "name": "Electronics"
            },
            "name": "Air Conditioner",
            "description": "",
            "price": 10000.0,
            "created_at": "2024-10-18 01:00:11"
        }
      }
     ```

#### 3. **Get Single Item**
   - **Endpoint:** `/items/<id>`
   - **Method:** `GET`
   - **Description:** Fetches details of a item by ID.
   - **Response Example:**
     ```json
      {
        "item": {
            "id": 1,
            "category": {
                "id": 1,
                "name": "Electronics"
            },
            "name": "Air Conditioner",
            "description": "",
            "price": 10000.0,
            "created_at": "2024-10-18 01:00:11"
        }
      }
     ```

#### 4. **Update Item**
   - **Endpoint:** `/items/<id>`
   - **Method:** `PUT`
   - **Description:** Updates the details of an existing item.
   - **Request Body Example:**
     ```json
     {
        "category_id": 1,
        "name": "Fan",
        "description": "",
        "price": 5000
     }
     ```
   - **Response Example:**
     ```json
      {
        "item": {
            "id": 2,
            "category": {
                "id": 1,
                "name": "Electronics"
            },
            "name": "Fan",
            "description": "",
            "price": 5000.0,
            "created_at": "2024-10-17 11:45:17"
        }
      }
     ```

#### 5. **Delete Product**
   - **Endpoint:** `/items/<id>`
   - **Method:** `DELETE`
   - **Description:** Deletes a item by ID.
   - **Response Example:**
     ```json
     {
       "message": "Item deleted successfully."
     }
     ```

#### 6. **Get All Categories**
   - **Endpoint:** `/categories`
   - **Method:** `GET`
   - **Description:** Fetches a list of all categories.
   - **Response Example:**
     ```json
     {
        "categories": [
            {
                "id": 1,
                "name": "Electronics"
            },
            {
                "id": 2,
                "name": "Smart Home"
            }
        ]
     }
     ```
#### 7. **Create New Category**
   - **Endpoint:** `/categories`
   - **Method:** `POST`
   - **Description:** Creates a new category.
   - **Request Body Example:**
     ```json
     {
        "name": "Electronics",
     }  
     ```
   - **Response Example:**
     ```json
      {
        "category": {
          "id": 1,
          "name": "Electronics"
        }
      }
     ```

## Debugging Part 
Documentation for debugging is in the `debug/` folder.
