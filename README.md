# Backend Coding Challenge: Scalable and Testable API

## **Project Overview**
This project is a RESTful API built using FastAPI and MongoEngine, designed to manage items. It demonstrates scalability, reusability, and modularity, suitable for a large-scale application. Key features include a Pub/Sub system, integration with external APIs, and token-based authentication.

---

## **Features**
1. **Item Management**:
   - Create, retrieve, update, and delete items.
   - Auto-update geolocation and direction based on the postcode.

2. **Authentication**:
   - Simulated authentication using Bearer tokens.
   - All endpoints require a valid token.

3. **Pub/Sub Event System**:
   - Handles asynchronous tasks independently of API requests using `pyee`.

4. **Integration with External API**:
   - Fetches geolocation data from [Zippopotam](https://api.zippopotam.us).
   - Calculates direction relative to New York (10001).

5. **Code Structure**:
   - Modular and scalable design to easily add new features or endpoints.

6. **Testing**:
   - Comprehensive unit tests with `pytest` for edge cases and core functionality.

---

## **Project Structure**
```
backend_coding_challenge/
├── app/
│   ├── main.py                 # Entry point of the API
│   ├── models.py               # Item model definition
│   ├── database.py             # MongoDB connection logic
│   ├── routes/
│   │   └── items.py            # Routes for item-related operations
│   ├── utils/
│   │   ├── auth.py             # Authentication middleware
│   │   ├── validation.py       # Validation utilities
│   │   ├── pubsub.py           # Pub/Sub event system
│   └── tests/
│       ├── test_items.py       # Unit tests for item routes
│       └── test_auth.py        # Unit tests for authentication
├── requirements.txt            # Pip dependencies
├── environment.yml             # Conda environment configuration
├── Makefile                    # Centralized commands for development
├── README.md                   # Project documentation
└── pytest.ini                  # pytest configuration
```

---

## **Setup Instructions**

### **1. Environment Setup**
#### Using Conda:
1. Create a Conda environment:
   ```bash
   conda env create -f environment.yml
   ```
2. Activate the environment:
   ```bash
   conda activate backend_challenge
   ```

#### Using Pip:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### **2. Run the Server**
Start the FastAPI server:
```bash
make start
```
The API will be available at `http://127.0.0.1:8000`.

### **3. Run Tests**
Run the test suite:
```bash
make test
```

---

## **API Endpoints**
### **Base URL**: `http://127.0.0.1:8000`

1. **POST /items**
   - Create a new item.
   - Payload (example):
     ```json
     {
       "name": "Sample Item",
       "postcode": "10001",
       "users": ["Sample Item", "John Doe"],
       "startDate": "2025-01-24"
     }
     ```

2. **GET /items**
   - Retrieve a list of all items.

3. **GET /items/{id}**
   - Retrieve details of a specific item by ID.

4. **PATCH /items/{id}**
   - Update mutable fields of an item (e.g., `name`, `title`, `users`, `startDate`).

5. **DELETE /items/{id}**
   - Delete an item by ID.

---

## **Testing**
- Ensure the server is not running when running tests.
- Run all tests:
  ```bash
  pytest --cov=app tests/
  ```
- Coverage reports are generated for all tested files.

---

## **Development Workflow**
Use the `Makefile` for common commands:
- Start the server:
  ```bash
  make start
  ```
- Run tests:
  ```bash
  make test
  ```
- Install dependencies:
  ```bash
  make install
  ```

---

## **Design Considerations**
1. **Scalability**:
   - Modular architecture ensures ease of adding new features or endpoints.
   - Pub/Sub system decouples asynchronous tasks from the main API logic.

2. **Reusability**:
   - Generic utilities for validation, authentication, and database operations.

3. **Extensibility**:
   - Easily extendable to add new models or services.

---

## **Future Improvements**
- Add rate limiting and caching for performance optimization.
- Implement role-based authentication for more secure access control.
- Use Docker for containerization and deployment.
- Extend logging to include trace IDs for better debugging in distributed systems.

---

## **Author**
- Developed for InsightWise Backend Coding Challenge.
- Contact: matt@insightwise.ai for feedback or queries.

# directions_from_new_york
# directions_from_new_york
