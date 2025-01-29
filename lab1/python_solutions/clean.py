import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf

def clean_dates_data(dates_data):
    '''
    Clean the dates data

    Parameters
    ----------
    dates_data : pd.DataFrame
        Dataframe containing the epoch information with three columns: 
        'epoch number', 'date', 'day'

    Returns
    -------
    dates_data : pd.DataFrame
        Dataframe containing the cleaned epoch information
    '''

    # Extract day of the week
    dates_data['day_of_week'] = dates_data['date'].str.extract(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)')
    
    # Extract time
    dates_data['time_chr'] = dates_data['date'].str.extract(r'(\d{1,2}:\d{2}:\d{2})')
    dates_data['time'] = pd.to_datetime(dates_data['time_chr'], format='%H:%M:%S')
    
    # Extract and clean date
    dates_data['date_chr'] = dates_data['date'].str.replace(r'\d{1,2}:\d{2}:\d{2} ', '', regex=True)
    dates_data['date'] = pd.to_datetime(dates_data['date_chr'])
    
    # Combine date and time
    dates_data['datetime'] = pd.to_datetime(dates_data['date_chr'] + ' ' + dates_data['time_chr'])

    return dates_data


def clean_redwood_data(redwood_data):
    '''
    Clean the redwood data
    
    Parameters
    ----------
    redwood_data : pd.DataFrame
        Dataframe containing the redwood data

    Returns
    -------
    redwood_data : pd.DataFrame
        Dataframe containing the cleaned redwood data
    '''
    # TODO: ADD CLEANING CODE HERE
    return redwood_data


def clean_mote_location_data(mote_data):
    '''
    Clean the mote location data

    Parameters
    ----------
    mote_data : pd.DataFrame
        Dataframe containing the mote location data

    Returns
    -------
    mote_data : pd.DataFrame
        Dataframe containing the cleaned mote location data
    '''
    # TODO: ADD CLEANING CODE HERE
    return mote_data