import pandas as pd
from os.path import join as oj


def load_dates_data(path='data'):
    ''' 
    Load the dates data

    Parameters
    ----------
    path : str
        The path to the data directory

    Returns
    -------
    df : pd.DataFrame
        Dataframe containing the epoch information with three columns: 
        'epoch number', 'date', 'day'
    '''
    epoch_nums = pd.read_csv(
        oj(path, 'sonoma-dates-epochNums.txt'), sep=' ', header=None
    ).T
    epoch_nums.columns = ['number']

    epoch_dates = pd.read_csv(
        oj(path, 'sonoma-dates-epochDates.txt'), sep="'\\s+", header=None, engine='python'
    ).T
    epoch_dates.columns = ['date']
    epoch_dates['date'] = epoch_dates['date'].str.replace("'", "")
    
    epoch_days = pd.read_csv(
        oj(path, 'sonoma-dates-epochDays.txt'), sep=' ', header=None
    ).T
    epoch_days.columns = ['day']
    
    epoch_data = pd.concat([epoch_nums, epoch_dates, epoch_days], axis=1)
    return epoch_data


def load_redwood_data(path='data', source='all'):
    ''' 
    Load the redwood data

    Parameters
    ----------
    path : str
        The path to the data directory
    source : str
        The source of the data. Can be 'all', 'log', or 'net'

    Returns
    -------
    df : pd.DataFrame
        Dataframe containing the redwood data
    '''
    assert source in ['all', 'log', 'net'], 'source must be one of "all", "log", or "net"'
    redwood_data = pd.read_csv(oj(path, f'sonoma-data-{source}.csv'))
    redwood_data.columns = redwood_data.columns.str.strip()  # Remove any leading/trailing spaces
    return redwood_data


def load_mote_location_data(path='data'):
    ''' 
    Load the mote location data

    Parameters
    ----------
    path : str
        The path to the data directory

    Returns
    -------
    df : pd.DataFrame
        Dataframe containing the mote location data
    '''
    # TODO: LOAD MOTE LOCATION DATA
    return