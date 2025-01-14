# CrossDBAccess

**CrossDBAccess** is a simple application designed to manage and retrieve data from multiple databases. This project serves as a personal tool to efficiently work with both static and dynamic databases and streamline data synchronization.

## Features

- Secure data retrieval from multiple databases.
- Synchronization of data from different sources.
- Simplified integration of static and dynamic databases.
- RESTful API for managing users, authentication, and devices.

---

## Installation

Follow the steps below to set up the project:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd CrossDBAccess



## API Endpoints

### **Authentication**

1. **Get CSRF Token**
    - **Endpoint:** `GET /api/auth/csrf/`
    - **Description:** Retrieve a CSRF token for secure requests.

2. **Login**
    - **Endpoint:** `POST /api/auth/login/`
    - **Body:**
      ```json
      {
        "email": "user@example.com",
        "password": "password123"
      }
      ```
    - **Response:**
      ```json
      {
        "access_token": "your-jwt-token"
      }
      ```

3. **Logout**
    - **Endpoint:** `GET /api/auth/logout/`
    - **Description:** Log out the user and invalidate the session.

---

### **Users**

1. **Get Current User Information**
    - **Endpoint:** `GET /api/users/current/`
    - **Headers:**
      ```json
      {
        "Authorization": "Bearer your-jwt-token"
      }
      ```
    - **Response:**
      ```json
      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
      }
      ```

---

### **Devices**

1. **Get All Devices**
    - **Endpoint:** `GET /api/devices/`
    - **Query Parameters:**
        - `page` - Page number (default: 1)
        - `page_size` - Number of items per page (default: 10)
    - **Response:**
      ```json
      {
        "count": 2,
        "page_count": 1,
        "page_size": 10,
        "results": [
          {
            "id": 1,
            "serial_number": "ABC123",
            "item": "Heater",
            "category": "Electronics",
            "is_external": false
          }
        ]
      }
      ```

2. **Get Device by ID**
    - **Endpoint:** `GET /api/devices/<device_id>/`
    - **Response:**
      ```json
      {
        "id": 1,
        "serial_number": "ABC123",
        "item": "Heater",
        "category_type": "Electronics"
      }
      ```

3. **Add New Device**
    - **Endpoint:** `POST /api/devices/add/`
    - **Body:**
      ```json
      {
        "serial_number": "DEF456",
        "item_id": 1,
        "category_type": "Electronics"
      }
      ```
    - **Response:**
      ```json
      {
        "message": "Device added successfully"
      }
      ```

4. **Delete Device**
    - **Endpoint:** `DELETE /api/devices/delete/<device_id>/`
    - **Response:**
      ```json
      {
        "message": "Device deleted successfully"
      }
      ```

---

## Configuration

Update the configuration file in `config/config.py` to set up:
- Local database
- Remote database
- Mail server
- JWT secret keys
