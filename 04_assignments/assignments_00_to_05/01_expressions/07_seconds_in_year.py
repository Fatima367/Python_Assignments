
DAYS_IN_A_YEAR :int = 365
HOURS_IN_A_DAY : int = 24
MINUTES_IN_AN_HOUR : int = 60
SECONDS_IN_A_MIN : int = 60


def main():
    print("There are " + str(DAYS_IN_A_YEAR * HOURS_IN_A_DAY * MINUTES_IN_AN_HOUR * SECONDS_IN_A_MIN) + " seconds in a year!")


if __name__ == '__main__':
    main()