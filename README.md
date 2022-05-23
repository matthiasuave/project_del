# project_del
Project Del extracts Covid data from https://healthdata.gov/ and provides the following metrics:
    - The total number of PCR tests performed as of a particular day (total_pcr_date) in the United States.
    - The n-day (window) rolling average number of new cases per day for the last k (rolling_averages_days) days.
    - The top n (top_states) states with the highest test positivity rate (positive tests / tests performed) for tests performed in the last k (positivity_rates_days) days.

    Parameters:
        - total_pcr_date: (date) Date up until when total pcr tests should calculated to. Default = current date - 1 day.
        - window: (int) Number of days for the rolling average window. Defaul = 7.
        - rolling_averages_days: (int) Number of days to be caculated for the rolling average. Default = 30.
        - positivity_rates_days: (int) Number of days from when the rolling average window should start. Defaul = 30.
        - top_states: (int) Number of top states with highest positivity rates. Default = 10.

# Required Libraries
To install the required libraries for the project run `pip install -r requirements.txt` from the `project_del` directory. This will install all dependencies for the application to run.

# Running the Application
The driver to run the application in this project can be found in `main.py` in the `project_del` directory.
To run the models and view the results, run `python main.py` from the `TermProject` directory.
All the parameters have been set to the asked questions as default values. To edit the parameters like dates, etc, include the parameter(s) to be edited while instatiating the DataWrngler class in the main.py file (`data_wrangler_object = DataWrangler(...)`) together with their desired values.