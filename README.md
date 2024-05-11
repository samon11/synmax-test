# SynMax Python Test May 10, 2024 - Michael Samon

## Project Structure

The project is structured as follows:

- [`src/`](src/): Contains the source code of the project.
- [`POLYGON_RESULTS.csv`](POLYGON_RESULTS.csv): Contains the results of the polygon endpoint test.

## Project files

- [`src/scraper.py`](src/scraper.py): Logic and driver code for the scraper.
- [`src/db.py`](src/db.py): All database related operations.
- [`src/api.py`](src/api.py): Flask API server.
- [`src/wells.db`](src/wells.db): SQLite database file containing the `api_well_data` table.

## Dependencies

Python 3.10
- `requests`
- `beautifulsoup4`
- `Flask`
- `shapely`

## API Spec

The API has the following endpoints:

- `GET /well`: Returns all data for a single well. 
  - URL param: `api` (str): Required - API number of the well.

- `GET /polygon`: Returns a list of API numbers for wells within a polygon.
  - Request JSON body param: `polygon` (list): Required - Polygon coordinates in the form `[[x1, y1], [x2, y2], ..., [xn, yn]]`.