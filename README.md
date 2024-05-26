# Weather Analysis and API Service

This project performs a detailed analysis of weather data from Hawaii and provides an API service to access this data. The analysis is conducted using Python and various libraries such as SQLAlchemy, Pandas, and Matplotlib. The API service is built using Flask.

## Table of Contents
- [Installation](#Installation)
- [Project Structure](#Porject-Structure)
- [Usage](#Usage)
- [API Endpoints](#API-Endpoints)

## Installation
1. Clone the repository:
git clone https://github.com/Bnrobertson/sqlalchemy-challenge.git
cd sqlalchemy-challenge
2. Create and activate a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the required packages:
pip install -r requirements.txt

## Project Structure
- `Resources/hawaii.sqlite`: The SQLite database containing the weather data.
- `app.py`: The Flask application file that sets up the API endpoints.
- `analysis.ipynb`: Jupyter Notebook containing the data analysis and visualizations.

## Usage
### Data Analysis
1. Open the Jupyter Notebook:
jupyter notebook climate_starter.ipynb
2. Run the cells to execute the data analysis and visualizations.

## API Service
1. Run the Flask application:
python app.py
2. Open your browser and navigate to http://127.0.0.1:5000/ to access the API.

## API Endpoints
- `/api/v1.0/precipitation`: Returns the last 12 months of precipitation data.
- `/api/v1.0/stations`: Returns a list of weather stations.
- `/api/v1.0/tobs`: Returns the temperature observations of the most active station for the last 12 months.
- `/api/v1.0/temp/<start>`: Returns the minimum, average, and maximum temperature for all dates greater than or equal to the start date (format: MMDDYYYY).
- `/api/v1.0/temp/<start>/<end>`: Returns the minimum, average, and maximum temperature for dates between the start and end date inclusive (format: MMDDYYYY).
