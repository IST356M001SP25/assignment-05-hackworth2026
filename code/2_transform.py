import pandas as pd
import pandaslib as pl
import streamlit as st

# Load survey data from cache
survey_data = pd.read_csv('cache/survey.csv')

# Load states data from cache
states_data = pd.read_csv('cache/states.csv')

# Handle NaN values in 'year' column and filter out rows with NaN years
survey_data = survey_data[survey_data['year'].notna()]

# Load list of col data from cache for each unique year
cols = []
for year in survey_data['year'].unique():
    try:
        col = pd.read_csv(f'cache/col_{year}.csv')
        cols.append(col)
    except FileNotFoundError:
        st.warning(f"File for year {year} not found, skipping.")
        continue

# Combine all col data into one dataframe
if cols:
    col_data = pd.concat(cols, ignore_index=True)
else:
    st.error("No cost of living data found.")
    col_data = pd.DataFrame()  # Empty dataframe to continue the process

# Clean the country column
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

# Lookup the state code from the state name
survey_states_combined = survey_data.merge(states_data, left_on="If you're in the U.S., what state do you work in?", right_on='State', how='inner')

# Create full city by combining city, state, and country
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']

# Merge the survey data with the col data
combined = survey_states_combined.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')

# Clean the salary column
combined["_annual_salary_cleaned"] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)

# Adjust the salary based on the cost of living
combined['_annual_salary_adjusted'] = combined.apply(lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']), axis=1)

# Save the combined data to a csv file
combined.to_csv('cache/survey_dataset.csv', index=False)

# Annual Salary adjusted by location and age
annual_salary_adjusted_by_location_and_age = combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean')
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

# Annual Salary adjusted by location and education
annual_salary_adjusted_by_location_and_education = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_annual_salary_adjusted', aggfunc='mean')
annual_salary_adjusted_by_location_and_education.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')

# Display the education-based report in Streamlit
st.write(annual_salary_adjusted_by_location_and_education)
