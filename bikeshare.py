#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: bikeshare.py
Description: This script does something related to sharing bikes in big cities.
Author: Mark Ray
Date: 2025-05-10
Version: 1.0
"""


import time
import pandas as pd
import numpy as np
import datetime


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
#data is for Jan - Jun
month_list = ['January', 'February', 'March', 'April','May','June','All']
my_days = ['Sunday', 'Monday','Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'All']



def user_input(my_input):
    """
        Asks user for a command line input to be picked from a list.  Continues indefinitely until
        a command line input that matches an entry in the list is provided.

        Note that input is changed to title case to match the list entries (assumes the list is in title
        case.)

    Arguments: list of selectable choices

    Returns:
        (str?) whatever the command line input is
    
    """
    selection = ''
    while selection not in my_input:
        selection = input("Choose one of [%s]:" % ", ".join(my_input))
        selection = selection.title()
        if selection not in my_input:
            print(selection + ' is a bad selection!')
        else:
            print(selection + ' is a good selection!')
    return selection

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    city = user_input(CITY_DATA.keys())
    month = user_input(month_list)
    day = user_input(my_days)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city]) #load the data frame as directed
    filtered_df = df
    if month != 'All':
        filtered_df = filtered_df[pd.to_datetime(filtered_df['Start Time']).dt.month==month_list.index(month)]
    if day != 'All':
        filtered_df = filtered_df[pd.to_datetime(filtered_df['Start Time']).dt.day_of_week==my_days.index(day)]
    return filtered_df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_counts = pd.to_datetime(df['Start Time']).dt.month.value_counts()
    month_max = month_counts[month_counts==month_counts.max()].index[0]
    print('The most common month is {} with {} entries'.format(month_list[month_max], month_counts.max()))

    day_counts = pd.to_datetime(df['Start Time']).dt.day_of_week.value_counts()
    day_max = day_counts[day_counts==day_counts.max()].index[0]
    print('The most common day is {} with {} entries'.format(my_days[day_max], day_counts.max()))

    hour_counts = pd.to_datetime(df['Start Time']).dt.hour.value_counts()
    hour_max = hour_counts[hour_counts==hour_counts.max()].index[0]
    print('The most common hour is {} with {} entries'.format(hour_max+1, hour_counts.max()))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    print('Most commonly used start station is ' + df['Start Station'].describe().top)

    print('Most commonly used end station is ' + df['End Station'].describe().top)

    print('Most common combination of start and stop station is {} and {}'.format(df.groupby(['Start Station','End Station']).size().idxmax()[0],df.groupby(['Start Station','End Station']).size().idxmax()[1]))
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total time traveled is {} seconds'.format(df['Trip Duration'].sum()))

    print('Mean Travel time is {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    for idx, user_type in enumerate(df['User Type'].unique()):
        try:
            print('{} of the users are {}'.format(df['User Type'].value_counts()[user_type], df['User Type'].unique()[idx]))
        except KeyError:
            print('User type for some entries were not specified')
    print('')
    try:
        for idx2, gender in enumerate(df['Gender'].unique()):
            try:
                print('{} of the users are {}'.format(df['Gender'].value_counts()[gender], df['Gender'].unique()[idx2]))
            except KeyError:
                print('NOTE:  Gender for {} entries were not specified'.format(df['Gender'].isna().sum()))
    except:
        print('dataset does not include gender')
    print('')
    try:
        print('Earliest birth year is {}'.format(int(df['Birth Year'].min())))
        print('Most recent birth year is {}'.format(int(df['Birth Year'].max())))
        print('Most common birth year is {}'.format(int(df['Birth Year'].median())))
    except:
        print('dataset does not include birth year')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        my_df = load_data(city, month, day)

        #view raw data
        idx = 0
        selection = input('would you like to see 5 rows of raw data? (yes/no)').lower()
        while selection != 'no':
            print(my_df.iloc[idx:idx+5])
            selection = input('would you like to see next five rows of data? (yes/no)').lower()
            idx +=6

        time_stats(my_df)
        station_stats(my_df)
        trip_duration_stats(my_df)
        user_stats(my_df)

        restart = input('Would you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes':
            return True
        elif restart.lower() == 'no':
            return False
        else:
            print('your input was malformed, program will terminate.')
            return False

if __name__ == "__main__":
	main()
