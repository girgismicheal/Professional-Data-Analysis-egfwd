import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities_options = ['chicago', 'new york city', 'washington']
month_choices = ["january", "february", "march", "april", "may", "june", "all"]
day_filter_options = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]


def check_var(var, choices):
    return var in choices


def check_input(input_string, choices):
    var = input(input_string).lower()
    while var not in choices:
        var = input("enter valid input from the list " + str(choices) + "\n").lower()
    return var


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # take inputs and validate it
    go = 'no'
    while go == "no":
        print('Hello! Let\'s explore some US bikeshare data!')

        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        print("""
            please enter your order as following:"
            City, Month filter, Day filter
            ---------------------------------------
            input choices:
            1- (City) could be one of the three cities: "chicago", "new york city", "washington"
            2- (Month filter) can be on of those: "January", "February", "March", "April", "May", "June", "all"
            3- (Day filter) can be: "Monday", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday", "all"
            ----------------------------------------
            Input example:
            new York city, February, SaturDay
            """)

        city, month, day = list(map(str.strip, input().lower().split(',')))[:3]

        while not check_var(city, cities_options) or not check_var(month, month_choices) or not check_var(day,
                                                                                                          day_filter_options):

            if not check_var(city, cities_options):
                print("invalid input for city choose one of the three cities")
            if not check_var(month, month_choices):
                print("invalid input for month filter choose one of the seven options of the Month filter")
            if not check_var(day, day_filter_options):
                print("invalid input for Day filter choose one of the eight options of Day filter")
            city, month, day = list(map(str.strip, input("enter the order again !\n").lower().split(',')))[:3]

        ", Month filter: " + month + ", and days filter: " + day
        print(f"""we received a valid input order
            you need to explore the data of city :{city}
            month filter: {month}
            Day filter: {day}  
            """)
        go = check_input("to continue with this inputs Enter 'yes' to update it enter with anther order enter 'no'\n"
                         , ["yes", "no"])

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = month_choices[:-1].index(month) + 1
        print(str(month) + "-*--*-*-*-**-*-*-*-*-*-*-*-**-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-")
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['Start Time'].dt.month_name().nunique() > 1:
        print("Most common month is: " + df['Start Time'].dt.month_name().mode()[0])
    # display the most common day of week
    if df['Start Time'].dt.day_name().nunique() > 1:
        print("Most common day is: " + df['Start Time'].dt.day_name().mode()[0])
    # display the most common start hour
    print("Most common hour is: " + str(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most frequent Start Station:" + df['Start Station'].mode()[0])
    # display most commonly used end station
    print("most frequent End Station:" + df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    df['star_end'] = df['Start Station'] + ' ' + df['End Station']
    print("most frequent trip: ", df['star_end'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("total time: {0} and AVG time: {1}".format(total_travel_time, mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("user types\n", user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts().to_dict()
        print("Gender", gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("earliest year", earliest)
        print("most recent year", most_recent)
        print("common year", common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        explore = "yes"
        next_row = 0
        while explore == "yes":
            explore = check_input("Would you like to explore more data? Enter yes or no\n"
                                  , ["yes", "no"])
            if next_row + 5 > len(df.index):
                print("Sorry ! No more data to display")
                break
            if explore == "yes":
                print(df[next_row:next_row + 5])
                next_row += 5

        restart = check_input('\nWould you like to restart? Enter yes or no.\n'
                              , ["yes", "no"])

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
