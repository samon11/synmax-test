# SynMax Python Test - Michael Samon

This project provides a Python-based solution for scraping well data, storing it in a SQLite database, and exposing it via a Flask API. The API allows users to retrieve well data by API number or by a geographic polygon.

## Setup and Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/samon11/synmax-test.git
    cd synmax-test
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

### 1. Populate the Database (Scraper)

The scraper (`src/scraper.py`) is responsible for fetching well data and populating the `wells.db` SQLite database. Run it once to initialize your database:

```bash
python src/scraper.py
```
This will create `src/wells.db` with the scraped data.

### 2. Start the API Server

The Flask API server (`src/api.py`) exposes the well data. To start the server:

```bash
python src/api.py
```
The API server will typically run on `http://127.0.0.1:59488`.

## Project Structure

The project is structured as follows:

- [`src/`](src/): Contains the source code of the project.
- [`POLYGON_RESULTS.csv`](POLYGON_RESULTS.csv): This file is generated after running the polygon endpoint test and contains the API numbers of wells found within a specified polygon.

### Key Files:

- [`src/scraper.py`](src/scraper.py): Logic and driver code for the scraper.
- [`src/db.py`](src/db.py): All database related operations.
- [`src/api.py`](src/api.py): Flask API server.
- [`src/wells.db`](src/wells.db): SQLite database file containing the `api_well_data` table.

## Dependencies

The project uses Python 3.10. The required libraries are listed in `requirements.txt`:

-   `requests`: Used for making HTTP requests to fetch data from web sources.
-   `beautifulsoup4`: A library for parsing HTML and XML documents, used in the scraper for data extraction.
-   `Flask`: A micro web framework used to build the API server.
-   `shapely`: A library for manipulation and analysis of geometric objects, used for polygon operations in the API.

## API Spec

The API has the following endpoints:

### `GET /well`
-   **Description:** Returns all data for a single well.
-   **URL Parameters:**
    -   `api` (string): **Required** - The API number of the well.
-   **Example Request:**
    ```
    GET /well?api=12345
    ```
-   **Example Response (JSON):**
    ```json
    {
        "api": "12345",
        "well_name": "Example Well 1",
        "latitude": 34.567,
        "longitude": -101.234,
        "status": "Active"
    }
    ```

### `GET /polygon`

-   **Description:** Returns a list of API numbers for wells whose geographical coordinates fall within a specified polygon.
-   **Request Body (JSON):**
    -   `polygon` (list of lists): **Required** - A list of coordinate pairs representing the vertices of the polygon. The format is `[[longitude1, latitude1], [longitude2, latitude2], ..., [longitudeN, latitudeN]]`. The polygon should be closed (first and last point can be the same, but not strictly required by `shapely`).
-   **Example Request:**
    ```json
    POST /polygon
    Content-Type: application/json

    {
        "polygon": [
            [-102.0, 35.0],
            [-102.0, 36.0],
            [-101.0, 36.0],
            [-101.0, 35.0],
            [-102.0, 35.0]
        ]
    }
    ```
-   **Example Response (JSON):**
    ```json
    {
        "well_apis_in_polygon": ["12345", "67890"]
    }
    ```

### `GET /hello`
-   **Description:** Returns a simple "Hello, World!" message.
-   **Example Request:**
    ```
    GET /hello
    ```
-   **Example Response (Plain Text):**
    ```
    Hello, World!
    ```
