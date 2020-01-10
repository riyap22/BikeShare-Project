import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nWhich city do you want to analyze?\n")
    while True:
        city = input("new york city? \nchicago? \nwashington?\n")
        city = city.lower()
        if city not in ('new york city', 'chicago', 'washington'):
            print("Sorry there was an error! Please try again\n")
            continue
        else:
            break

    print("\nWhich month would you like to filter the data by")
    while True:
        month = input("january? \nfebruary? \nmarch? \napril? \nmay? \njune? \ntype 'all' to view the data for all the months\n")
        month = month.lower()
        if month not in ('january','february','march','april','may','june','all'):
            print("Sorry there was an error! Please try again\n")
            continue
        else:
            break

    print("\nWhich day of the week would you like to filter the data by?\n")
    while True:
        day = input("monday? \ntuesday? \nwednesday? \nthursday? \nfriday? \nsaturday \nsunday \ntype 'all' to view the data for all the weeks?\n")
        day = day.lower()
        if day not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'):
            print("Sorry there was an error! Please try again\n")
            continue
        else:
            break

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
  
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['week'] == day.title()]
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("The most common month is: {}".format(str(df['month'].mode()[0])))
   
    print("The most common day of the week is: {}".format(str(df['week'].mode()[0])))
    
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is: {}".format(str(df['hour'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    st_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station:', st_station)

    ed_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station:', ed_station)

    routes = df['Start Station']+ " " + df['End Station'].mode()[0]
    print('\nThe most Commonly used combination of start station and end station trip:',routes)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    T_time = sum(df['Trip Duration'])
    print('\nThe total travel time is:',T_time)

    M_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is:',M_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    u_types = df['User Type'].count()
    print('The count of user types:\n',u_types)

    print()
    if 'Gender' not in df:
        print('Sorry an error occured!')    
    else:
      g_types = df['Gender'].count()
      print('\nThe counts of gender: \n',g_types)
 
    print()
    if 'Birth Year' not in df:
        print('Sorry an error occurred!')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Earliest year of birth was {}.'.format(int(birth['Birth Year'].min())))
        print('Most recent year of birth was {}.'.format(int(birth['Birth Year'].max())))
        print("The most common birth year is: {}.".format(str(int(df['Birth Year'].mode()[0]))))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_input(df):
    r = 0
    while True:
        usr_input = input("Would you like to see 5 lines of raw data from the dataframe, yes or no?\n")
        usr_input = usr_input.lower()
        if usr_input not in ('yes', 'no'):
            print("Sorry an error occured! Please try again")
            continue
        elif usr_input == 'yes':
            print(df[r : r+5])
            r = r + 5
        elif usr_input == 'no':
            break
                       
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_input(df)               
   

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
