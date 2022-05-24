import pandas as pd
from datetime import date, timedelta

class DataWrangler:
    """
    DataWrangler extracts Covid data from https://healthdata.gov/ and provides the following metrics:
        - The total number of PCR tests performed as of a particular day (total_pcr_date) in the United States.
        - The n-day (window) rolling average number of new cases per day for the last k (rolling_averages_days) days.
        - The top n (top_states) states with the highest test positivity rate (positive tests / tests performed) for tests performed in the last k (positivity_rates_days) days.

    Parameters:
        total_pcr_date: date. Date up until when total pcr tests should calculated to. Default = current date - 1 day.
        window: int. Number of days for the rolling average window. Defaul = 7.
        rolling_averages_days: int. Number of days to be caculated for the rolling average. Default = 30.
        positivity_rates_days: int. Number of days from when the rolling average window should start. Defaul = 30.
        top_states: int. Number of top states with highest positivity rates. Default = 10.
    """

    def __init__(self,
            total_pcr_date=(date.today()-timedelta(days=1)).strftime('%Y-%m-%d'),
            window=7,
            rolling_averages_days=30,
            positivity_rates_days=30,
            top_states=10):
        
        url = 'https://healthdata.gov/resource/j8mb-icvb.json?$limit=300000'

        self.covid_data = pd.read_json(url)
        self.total_pcr_date = total_pcr_date
        self.window = window
        self.rolling_averages_days = rolling_averages_days
        self.positivity_rates_days = positivity_rates_days
        self.positivity_rates_date = (date.today()-timedelta(days=positivity_rates_days)).strftime('%Y-%m-%d')
        self.top_states = top_states

    def total_pcr_test(self):
        """
        Calculates the total number PCR tests done as at a particular day
        :return: total number of PCR test as at a given day
        """
        return self.covid_data[self.covid_data['date']<=self.total_pcr_date]['total_results_reported'].sum()

    def rolling_average(self):
        """
        Calulates the n-day rolling average of new positive cases in the last k days
        :return: rolling averages
        """
        # new cases includes only positive cases
        new_cases_sum = self.covid_data[self.covid_data['overall_outcome']=='Positive'].groupby(['date'])['new_results_reported'].sum()
        new_cases_sum.sort_index()
        
        windows = new_cases_sum.rolling(self.window)
        rolling_averages = windows.mean()
        return rolling_averages[-self.rolling_averages_days:]

    def top_n_states(self):
        """
        Calculates positivity rate by states. First gets total tests and total positive tests then divide
        :return: top n states with highest positivity rates
        """
        total_test_df = pd.DataFrame(self.covid_data[self.covid_data['date']>=self.positivity_rates_date]\
            .groupby(['state_name'])['total_results_reported'].sum())

        positive_test_df = pd.DataFrame(self.covid_data[(self.covid_data['overall_outcome']=='Positive') \
            & (self.covid_data['date']>=self.positivity_rates_date)].groupby(['state_name'])['total_results_reported'].sum())

        positive_test_df.rename(columns={'total_results_reported': 'positive_results'}, inplace=True)

        joined_df = total_test_df.join(positive_test_df)
        joined_df['positivity_rate'] = round(joined_df['positive_results'] / joined_df['total_results_reported'],3)
        
        return joined_df[['positivity_rate']].sort_values(by=['positivity_rate'], ascending=False).head(self.top_states)

    def main(self):
        print(f'\n1. The total number of PCR tests performed as at {self.total_pcr_date} in the United State is {self.total_pcr_test()}\n')

        print(f'2. The {self.window}-day rolling average number of new cases per day for the last {self.rolling_averages_days} days is \n{self.rolling_average()}\n')

        print(f'3. The {self.top_states} states with the highest test positivity rate (positive tests / tests performed) for tests performed in the last {self.positivity_rates_days} days is \n{self.top_n_states()}')
