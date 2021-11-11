#  Adding import lines
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

## FUNCTIONS
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ["chicago", "new york city", "washington"]
    city_prompt = "Would you like to see data for Chicago, New York City, or Washington? "
    city = input(city_prompt).lower()
    while city not in city_list:
        print("Not a valid selection, please try again.")
        city = input(city_prompt).lower()

    # get user input for month (all, january, february, ... , june)
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "All"]
    month_prompt = "Which month would you like to see data for "+city+"? Enter 'All' to see data for all months. "
    month_name = input(month_prompt).title()
    while month_name not in month_list:
        print("Not a valid selection, please try again.")
        month_name = input(month_prompt).title()
    month_digit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    month_list = dict(zip(month_list, month_digit))
    month = month_list[month_name]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "All"]
    day_prompt = "Which day of the week would you like to see data for "+city.title()+" during "+month_name+"? Enter 'All' to see data for all days. "
    day_name = input(day_prompt).title()
    while day_name not in day_list:
        print("Not a valid selection, please try again.")
        day_name = input(day_prompt).title()
    day_digit = [1, 2, 3, 4, 5, 6, 7, 8]
    day_list = dict(zip(day_list, day_digit))
    day = day_list[day_name]

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
    # add underscores to file name if new york city selected
    if city == "new york city":
        city = "new_york_city"

    # Loading full dataset depending on city selected
    csvfile = city+".csv" 
    df = pd.read_csv(csvfile)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Adding Month, Dayofweek, and Hour columns
    df['Month'] = df['Start Time'].dt.month
    df['Dayofweek'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour

    ## FILTERING DATA
    # If user selected 'All for Months
    if month == 13:
        # If user selected specific day of the week
        if day <= 7:            
            df = df[df['Dayofweek'] == day]
            return df
        # If user selected 'All' weekdays
        else:
            return df
    # If user selected specific month
    if month <= 12:
        df = df[df['Month'] == month]
        # If user selected specific day of the week
        if day <= 7:
            df = df[df['Dayofweek'] == day]
            return df
        # If user selected 'All' weekdays
        else:
            return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    popular_month = df['Month'].mode()[0]
    month_digit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    month_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_list = dict(zip(month_digit, month_name))
    print('Most Popular Month:', month_list[popular_month])

    # display the most common day of week
    df['Dayofweek'] = df['Start Time'].dt.dayofweek
    popular_dayofweek = df['Dayofweek'].mode()[0]
    dayofweek_digit = [1, 2, 3, 4, 5, 6, 7]
    dayofweek_name = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    dayofweek_list = dict(zip(dayofweek_digit, dayofweek_name))
    print('Most Popular Day of the Week:', dayofweek_list[popular_dayofweek])

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    if popular_hour == 0:
        print('Most Popular Start Time Hour: 12am')
    elif popular_hour >= 13:
        popular_hour = popular_hour - 12
        print('Most Popular Start Time Hour:', popular_hour, 'PM')
    else:
        print('Most Popular Start Time Hour:', popular_hour, 'AM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print('Most common Start Station:', popular_startstation)

    # display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print('Most common End Station:', popular_endstation)

    # display most frequent combination of start station and end station trip
    popular_startend = df['Start Station'] + " to " + df['End Station']
    popular_trip = popular_startend.mode()[0]
    print('Most common trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total Trip Duration:', total_trip_duration)


    # display mean travel time
    avg_trip_duration = df['Trip Duration'].mean()
    print('Average Trip Duration:', avg_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print(df['Gender'].value_counts())
    except KeyError:
        print('\nNo Gender Data available')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = df['Birth Year'].min()
        latest_yob = df['Birth Year'].max()
        popular_yob = df['Birth Year'].mode()[0]     
        print('Earliest Year of Birth:', earliest_yob)
        print('Latest Year of Birth:', latest_yob)
        print('Most Common Year of Birth:', popular_yob)
    except KeyError:
        print('No Birth Year Data available')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """Shows 5 Lines of Data upon user's request"""

    data_prompt = "Would you like to see 5 lines of raw data? Enter yes or no.\n"
    data_answer = input(data_prompt).lower()
    a = 0
    b = 5
    while data_answer == "yes":
        print(df.iloc[a:b])
        data_prompt2 = "Here's more data, would you like to see more? Enter yes or no\n"
        data_answer = input(data_prompt2).lower()
        a += 5
        b += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
