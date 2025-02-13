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
    # Rename columns
    redwood_data = redwood_data.rename(columns={
        'humid_temp': 'temp',
        'hamatop': 'iPAR',
        'hamabot': 'rPAR'
    })
    
    # Drop irrelevant column and remove NA rows and duplicate rows
    redwood_data = redwood_data.drop(columns=['humid_adj']).dropna().drop_duplicates()
    
    # Plus any other cleaning steps...
    
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
    return mote_data


def merge_redwood_data(dates_data, motes_data, redwood_net_data, redwood_log_data):
    '''
    Merge the redwood data with the dates and motes data

    Parameters
    ----------
    dates_data : pd.DataFrame
        Dataframe containing the cleaned epoch information
    motes_data : pd.DataFrame
        Dataframe containing the cleaned mote location data
    redwood_net_data : pd.DataFrame
        Dataframe containing the cleaned network data
    redwood_log_data : pd.DataFrame
        Dataframe containing the cleaned log data

    Returns
    -------
    redwood_data : pd.DataFrame
        Dataframe containing the merged redwood data
    '''
    # Combine log and net data
    redwood_log_data['source'] = 'log'
    redwood_net_data['source'] = 'net'
    redwood_data = pd.concat([redwood_log_data, redwood_net_data], ignore_index=True)
    
    # Remove duplicates
    redwood_data = redwood_data.drop_duplicates(subset=['epoch', 'nodeid', 'humidity', 'temp', 'iPAR', 'rPAR'])
    
    # Sort by epoch and nodeid
    redwood_data = redwood_data.sort_values(by=['epoch', 'nodeid'])
    
    # Merge with dates data and mote location data
    redwood_data = (
        redwood_data
        .merge(dates_data, left_on='epoch', right_on='number', how='left')
        .merge(motes_data, left_on='nodeid', right_on='ID', how='left')
    )
    
    return redwood_data


def clean_merged_data(merged_data):
    '''
    Clean the merged redwood data

    Parameters
    ----------
    merged_data : pd.DataFrame
        Dataframe containing the merged redwood data

    Returns
    -------
    merged_data : pd.DataFrame
        Dataframe containing the cleaned merged data
    '''
    
    # Keep only interior trees
    merged_data = merged_data[merged_data['Tree'] == 'interior']

    # Remove observations without mote information
    merged_data = merged_data[~merged_data['Height'].isna()]

    # Remove observations outside of study dates
    merged_data = merged_data[merged_data["epoch"] <= 12635]
    
    # Remove observations where iPAR < rPAR
    merged_data = merged_data[merged_data['iPAR'] >= merged_data['rPAR']]

    # voltages from network and log are measured on different scales
    # so let's transform voltage from network data to match log data
    # using estimated coefficients from a previously learned linear regression
    merged_data['voltage'] = np.where(
        merged_data['source'] == 'net',
        -4.347e-07 + 5.939e+02 * 1 / merged_data['voltage'],
        merged_data['voltage']
    )
    
    return merged_data


def remove_battery_failure(merged_data):
    '''
    Remove anomalies in redwood data due to battery failure

    Parameters
    ----------
    merged_data : pd.DataFrame
        Dataframe containing the merged redwood data

    Returns
    -------
    merged_data : pd.DataFrame
        Dataframe containing the cleaned merged redwood data
    '''
    merged_data = merged_data[(merged_data['voltage'] >= 2.4) & (merged_data['voltage'] <= 3)]
    return merged_data
