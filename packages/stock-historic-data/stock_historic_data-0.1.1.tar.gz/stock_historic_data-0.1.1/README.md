# Stock Historic Data

This project is designed to fetch and store historic and live stock data using the Yahoo Finance API. The data is stored in SQLite databases and can be accessed via a Flask web application.

## Functionality

For a detailed walkthrough of the project's functionality, you can watch the following YouTube video:

[![Stock Historic Data Functionality](https://img.youtube.com/vi/4hRqNl2Iyz8/0.jpg)](https://www.youtube.com/watch?v=4hRqNl2Iyz8)

### Route: /
- Stock Historic Data Visualization Chart
- Data from Historic Database

![Historic Data Chart](https://github.com/abhiwer/stock_historic_data/blob/main/src/images/HistoricDataChart.png?raw=true)

### Route: /live
- Stock Live Data Visualization and sending data to live_database

![Live Data Chart](https://github.com/abhiwer/stock_historic_data/blob/main/src/images/LiveDataChart.png?raw=true)

### Route: /onlylive
- Only Tick per second Data for Data Visualization 

![Only Live Data Chart](https://github.com/abhiwer/stock_historic_data/blob/main/src/images/OnlyDataLive.png?raw=true)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/abhiwer/stock_historic_data.git
    cd stock_historic_data
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    flask run
    ```

2. Open your browser and navigate to:
    - `http://127.0.0.1:5000/` for Stock Historic Data Visualization Chart
    - `http://127.0.0.1:5000/live` for Stock Live Data Visualization
    - `http://127.0.0.1:5000/onlylive` for Only Tick per second Data Visualization

## Endpoints

- `/`: Main page to view historic data.
- `/live`: Page to view live data.
- `/onlylive`: Page to view only live data.
- `/get_dates`: API to get a range of dates.
- `/get_currencies`: API to get the list of supported currencies.
- `/get_updatetheliveDB`: API to update the live database.
- `/get_updatethehistoricDB`: API to update the historic database.

## License

This project is licensed under the MIT License.

![Alt text](https://github.com/abhiwer/stock_historic_data/blob/main/src/images/OnlyDataLive.png?raw=true)