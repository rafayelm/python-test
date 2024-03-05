
## **[python-test](https://github.com/rafayelm/python-test)**

**A Python project for storing and querying data with aggregation**

**Description:**

This project provides Python APIs to interact with a PostgreSQL database for storing and retrieving data with aggregation capabilities. It leverages Docker Compose for deployment of both the database and the Python application.

**Features:**

-   Exposes two RESTful APIs:
    -   **POST /event:**  Stores data in the database.
    -   **GET /analytics/query:**  Queries data with aggregation, filtering by various criteria.
-   Utilizes PostgreSQL as the primary data storage.
-   Employs Docker Compose for simplified deployment.

**Prerequisites:**

-   Docker and Docker Compose installed on your system.

**Installation:**

1.  Clone this repository:

    Bash

    ```
    git clone https://github.com/rafayelm/python-test.git
    ```

2.  Navigate to the project directory:

    Bash

    ```
    cd <your-project-name>
    ```

3.  Start the application and database using Docker Compose:

    Bash

    ```
    cd docker-compose
    docker-compose up -d
    ```

**Improvements:**

-   **Security:**  Currently database connection details are stored in plain text. This practice is discouraged. To enhance security, consider:
    -   Reading sensitive information from environment variables or a local configuration file.
-   **Testing:**  Integration tests are missing, consider:
    -   Adding integration tests to check logic with DB


**Usage:**

**1. Storing Data:**

You can use cURL commands to interact with the API endpoints. Here's an example for storing data:

Bash

```
curl -X POST http://localhost:5000/event \
-H 'Content-Type: application/json' \
-d '{
  "id": 1,
  "event_date": "2024-03-04T13:16:05.483Z",
  "attribute1": 198772,
  "attribute2": 198772,
  "attribute3": 198772,
  "attribute4": "some string",
  "attribute5": "12345",
  "attribute6": true,
  "metric1": 198772,
  "metric2": 1.2
}'
```

```
curl -X POST http://localhost:5000/event \
-H 'Content-Type: application/json' \
-d '{
  "id": 2,
  "event_date": "2024-03-04T14:16:05.483Z",
  "attribute1": 198772,
  "attribute2": 198772,
  "attribute3": 198772,
  "attribute4": "some string",
  "attribute5": "12345",
  "attribute6": true,
  "metric1": 198772,
  "metric2": 1.2
}'
```



**2. Querying Data:**

Use a cURL command with URL-encoded parameters to query data:

Bash

```
curl -X GET 'http://localhost:5000/analytics/query' \
-H 'Accept: application/json' \
-G \
--data-urlencode 'groupBy=attribute1,attribute4' \
--data-urlencode 'metrics=metric1,metric2' \
--data-urlencode 'granularity=hourly' \
--data-urlencode 'startDate=2023-01-01T08:00:00' \
--data-urlencode 'endDate=2025-01-01T09:00:00'
```

```
curl -X GET 'http://localhost:5000/analytics/query' \
-H 'Accept: application/json' \
-G \
--data-urlencode 'groupBy=attribute1,attribute4' \
--data-urlencode 'metrics=metric1,metric2' \
--data-urlencode 'granularity=daily' \
--data-urlencode 'startDate=2023-01-01T08:00:00' \
--data-urlencode 'endDate=2025-01-01T09:00:00'
```
