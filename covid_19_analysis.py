"""
COVID-19 Case Study & Exploratory Data Analysis
Author: AYUSH BOHRA
Tech Stack: Python, Pandas, Matplotlib
"""

# Q.1. Data Loading
import pandas as pd
import matplotlib.pyplot as plt

# Q.1.1 Load all relevant datasets
confirmed_cases = pd.read_csv("Downloads//covid_19_confirmed_v1.csv")
death_cases = pd.read_csv("Downloads//covid_19_deaths_v1.csv", header=1)
recovered_cases = pd.read_csv("Downloads//covid_19_recovered_v1.csv", header=1)

# Q.2. Data Exploration
# Q.2.1 Understand structure of datasets
confirmed_cases.info()
death_cases.info()
recovered_cases.info()

# Q.2.2 Generate plots of confirmed cases over time for top countries
top_countries = confirmed_cases.groupby('Country/Region').sum().nlargest(3, confirmed_cases.columns[-1]).index

plt.figure(figsize=(12, 6))
for country in top_countries:
    data = confirmed_cases[confirmed_cases['Country/Region'] == country].iloc[:, 4:].sum()
    plt.plot(data.index, data.values, label=country)

plt.xticks(rotation=45)
plt.legend()
plt.title("Total Confirmed Cases Over Time for Top 3 Countries")
plt.xlabel("Date")
plt.ylabel("Cumulative Confirmed Cases")
plt.show()

# Q.2.3 Generate plots for confirmed cases for China
china_data = confirmed_cases[confirmed_cases['Country/Region'] == "China"]
china_data.set_index('Province/State').iloc[:, 3:].T.plot()

plt.figure(figsize=(12, 6))
plt.title("Covid-19 Confirmed Cases Over Time for China")
plt.xlabel("Date")
plt.ylabel("Cumulative Confirmed Cases")
plt.legend(title="Province")
plt.xticks(rotation=45)
plt.show()

# Q.3. Handling Missing Data
# Q.3.1 Find missing values in the dataset and impute them using suitable methods
death_cases.replace("", pd.NA, inplace=True)
confirmed_cases.replace("", pd.NA, inplace=True)
recovered_cases.replace("", pd.NA, inplace=True)

mode_value = death_cases['Province/State'].mode()[0]
death_cases['Province/State'].fillna(mode_value, inplace=True)
death_cases.fillna(method='ffill', inplace=True)

mode_value_recovered = recovered_cases['Province/State'].mode()[0]
recovered_cases['Province/State'].fillna(mode_value_recovered, inplace=True)

def impute_with_moving_average(df):
    columns_to_impute = ['Lat', 'Long', '4/20/20']
    for col in columns_to_impute:
        df[col] = df[col].fillna(df[col].rolling(window=3, min_periods=1, center=True).mean())
    return df

deaths = impute_with_moving_average(death_cases)
recovered = impute_with_moving_average(recovered_cases)

# Q.4. Data Cleaning and Preparation
# Q.4.1 Replace blank values in Province / State column with All Provinces
confirmed_cases['Province/State'].fillna("All Province", inplace=True)
recovered_cases['Province/State'].fillna("All Province", inplace=True)
death_cases['Province/State'].fillna("All Province", inplace=True)

# Q.5. Independent Dataset Analysis
# Q.5.1 Peak daily new cases in Germany, France, and Italy
countries = ['Germany', 'France', 'Italy']
daily_new_cases = {}

for country in countries:
    country_data = confirmed_cases[confirmed_cases['Country/Region'] == country]
    summed_daily_cases = country_data.iloc[:, 4:].sum(axis=0).diff().fillna(0)
    daily_new_cases[country] = summed_daily_cases

peaks = {}
for country, data in daily_new_cases.items():
    peak_date = data.idxmax()
    peak_cases = data.max()
    peaks[country] = (peak_cases, peak_date)

print(peaks)

plt.figure(figsize=(12, 6))
for country, data in daily_new_cases.items():
    plt.plot(data.index, data.values, label=country)

plt.legend()
plt.title("Daily New Covid-19 Cases")
plt.xlabel("Date")
plt.ylabel("Number of New Cases")
plt.xticks(rotation=45)
plt.show()

# Q.5.2 Compare recovery rates between Canada and Australia
recovery_rates = {}
for country in ['Canada', 'Australia']:
    country_cases = confirmed_cases[confirmed_cases['Country/Region'] == country].iloc[:, 4:].sum(axis=0)
    country_recoveries = recovered_cases[recovered_cases['Country/Region'] == country].iloc[:, 4:].sum(axis=0)
    recovery_rate = country_recoveries['12/31/20'] / country_cases['12/31/20']
    recovery_rates[country] = recovery_rate

print(recovery_rates)

plt.bar(recovery_rates.keys(), recovery_rates.values(), color=['blue', 'green'])
plt.title("Recovery Rates comparison on 12/31/20")
plt.ylabel("Recovery Rate")
plt.show()

# Q.5.3 Distribution of death rates across Canada provinces
canada_cases = confirmed_cases[confirmed_cases['Country/Region'] == "Canada"].drop(columns=['Country/Region', 'Lat', 'Long'])
canada_deaths = death_cases[death_cases['Country/Region'] == "Canada"].drop(columns=['Country/Region', 'Lat', 'Long'])

canada_cases = canada_cases.groupby('Province/State').sum().iloc[:, -1]
canada_deaths = canada_deaths.groupby('Province/State').sum().iloc[:, -1]

death_rates = pd.Series(0, index=canada_cases.index)
death_rates[canada_cases != 0] = canada_deaths.div(canada_cases[canada_cases != 0])

max_death_rate = death_rates.idxmax()
min_death_rate = death_rates.idxmin()

print(f"Highest death rate in Canada: {max_death_rate}")
print(f"Lowest death rate in Canada: {min_death_rate}")

death_rates.plot(kind='bar')
plt.title("Death Rates by Provinces in Canada")
plt.ylabel("Death Rate")
plt.xlabel("Province")
plt.show()
