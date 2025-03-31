import pandas as pd
import streamlit as st
import pandaslib as pl

def load_data():
    states_data = pd.read_csv('cache/states.csv')
    survey_data = pd.read_csv('cache/survey.csv')
    col_data_frames = []
    for year in survey_data['year'].unique():
        col_data_frames.append(pd.read_csv(f'cache/col_{year}.csv'))
    col_data = pd.concat(col_data_frames, ignore_index=True)
    return states_data, survey_data, col_data

def merge_data(states_data, survey_data, col_data):
    survey_data['_country'] = survey_data['Which country do you work in?'].apply(pl.clean_country_usa)
    survey_states_combined = pd.merge(survey_data, states_data, left_on='If you\'re in the U.S., what state do you work in?', 
                                      right_on='State', how='inner')
    survey_states_combined['_full_city'] = survey_states_combined['City'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']
    combined = pd.merge(survey_states_combined, col_data, how='inner', left_on=['year', '_full_city'], right_on=['year', 'City'])
    return combined

def normalize_salary(combined):
    combined['__annual_salary_cleaned'] = combined['Annual salary'].apply(pl.clean_currency)
    combined['_annual_salary_adjusted'] = (combined['__annual_salary_cleaned'] / combined['Cost of Living']) * 100
    return combined

def generate_reports(combined):
    report1 = pd.pivot_table(combined, values='_annual_salary_adjusted', 
                             index='_full_city', columns='How old are you?', aggfunc='mean')
    report1.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')
    
    report2 = pd.pivot_table(combined, values='_annual_salary_adjusted', 
                             index='_full_city', columns='What is your highest level of education?', aggfunc='mean')
    report2.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')

def transform_data():
    states_data, survey_data, col_data = load_data()
    combined = merge_data(states_data, survey_data, col_data)
    normalized_data = normalize_salary(combined)
    generate_reports(normalized_data)

if __name__ == "__main__":
    transform_data()

