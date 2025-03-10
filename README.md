# Python RESTful API for GoldenRaspberryAwards

This project is a RESTful API built with Flask that reads movie data from a CSV file and populates an in-memory SQLite database. It provides endpoints to retrieve movie information.

## Project Structure

```
GoldenRaspberryAwards
├── app
│   ├── controller.py
│   ├── main.py
│   ├── models.py
│   └── extensions.py
├── data
│   └── Movielist.csv
├── tests
│   └── test_app.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd GoldenRaspberryAwards
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python -m app.main
   ```

## Usage

Once the application is running, you can access the API endpoints:

- **Get all movies:**
  ```
  GET /movies
  ```

- **Get a movie by ID:**
  ```
  GET /movies/<int:movie_id>
  ```

- **Get all nominees:**
  ```
  GET /nominees
  ```

- **Get all winners:**
  ```
  GET /winners
  ```

- **Get interval of awards:**
  ```
  GET /get_interval
  ```

- **Add a new movie:**
  ```
  POST /movies
  ```
  Example request body:
  ```json
  {
    "year": 2021,
    "title": "New Movie",
    "studios": "New Studio",
    "producers": "New Producer",
    "winner": true
  }
  ```

- **Update a movie by ID:**
  ```
  PATCH /movies/<int:movie_id>
  ```
  Example request body:
  ```json
  {
    "title": "Updated Movie Title"
  }
  ```

- **Delete a movie by ID:**
  ```
  DELETE /movies/<int:movie_id>
  ```

## Tests
Integration tests is achieved by running:

```
python -m unittest discover -s tests
```

## Note about tests:

The expected results in documentation "FORMATO DA API" is not reached because `max.producer == "Producer 1"` has interval value equals to 109,
based in years `{"previousWin": 1900 and "followingWin": 2009}`

## Dependencies

The in-memory database used is SQLite, so require the instalation of sqlite sources [SQLite Download Page](https://www.sqlite.org/download.html).

The project requires the following Python packages:

- Flask
- Flask-SQLAlchemy

Make sure to install them using the `requirements.txt` file.

## License

This project is licensed under the GPL License.