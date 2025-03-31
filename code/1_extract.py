import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
def extract_year_mdy(date_str):
    return pd.to_datetime(date_str).year

def extract_states():
    states_url = 'https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv'
    states_data = pd.read_csv(states_url)
    states_data.to_csv('cache/states.csv', index=False)
    return states_data

def extract_survey():
    survey_url = 'https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv'
    survey_data = pd.read_csv(survey_url)
    survey_data['year'] = survey_data['Timestamp'].apply(extract_year_mdy)
    survey_data.to_csv('cache/survey.csv', index=False)
    return survey_data

def extract_col_data(year):
    col_url = f'https://www.example.com/col_{year}.csv'  # Replace with the actual URL
    col_data = pd.read_csv(col_url)
    col_data['year'] = year
    col_data.to_csv(f'cache/col_{year}.csv', index=False)
    return col_data

def extract_all_data():
    extract_states()
    survey_data = extract_survey()
    years = survey_data['year'].unique()
    for year in years:
        extract_col_data(year)

if __name__ == "__main__":
    extract_all_data()

