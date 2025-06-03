# Web App Python Project

Here you can see the code for my Streamlit application. It contains some data about the car sales base.
You can look closely at the various charts and get your idea of the car market.

You can run the app.py file locally on your computer (streamlit run app.py) or see the results here:
https://sdt-project-feklina.onrender.com

The app provides interactive visualizations to analyze the condition, price, popularity, and other features of vehicles by year, manufacturer, drive type, and color.

## 📊 Features

- Displays raw data in an interactive table.
- Handles missing values using appropriate imputation methods (median by model/year/type/condition).
- Allows filtering by:
  - model year range
  - transmission type
  - all-wheel drive
  - car type (sedan, SUV, etc.)
  - manufacturer
- Interactive histograms for:
  - number of cars by manufacturer and type
  - condition of cars over the years
  - average price by model year
  - color preferences by manufacturer
  - average prices of selected cars
- Bubble chart of price trends by manufacturer and decade.

## 🧰 Technologies

- python
- pandas
- streamlit
- plotly

## 📁 Files

- `app.py` — main app script
- `vehicles_us.csv` — dataset used in the app
- `EDA_new.ipynb` — some drafts and data research

## 🚀 Run Locally

```bash
pip install streamlit pandas plotly
streamlit run app.py
