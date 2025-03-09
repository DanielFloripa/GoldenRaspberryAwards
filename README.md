# Python RESTful API for Movie Data

This project is a RESTful API built with Flask that reads movie data from a CSV file and populates an in-memory SQLite database. It provides endpoints to retrieve movie information.

## Project Structure

```
python-rest-api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── data
│   └── Movielist.csv
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd python-rest-api
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
   python app/main.py
   ```

## Usage

Once the application is running, you can access the API endpoints:

- **Get all movies:**
  ```
  GET /movies
  ```

- **Get a movie by title:**
  ```
  GET /movies/<title>
  ```

## Dependencies

The project requires the following Python packages:

- Flask
- Flask-SQLAlchemy

Make sure to install them using the `requirements.txt` file.

## License

This project is licensed under the MIT License.