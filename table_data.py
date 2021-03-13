"""Module for generating data"""

import datetime
import random


# Constants for the class TableData.
CAR_COUNT_LIMIT = 1000
CAR_PRICE_LOW_BOUND = 30000.00
CAR_PRICE_HIGH_BOUND = 135000.70


class TableData:
    """Class for generating random data of table."""

    def __init__(self, models_names: tuple, headings: tuple):
        self._models_names = models_names
        self._headings = headings

        self.__start_date = datetime.date(2012, 1, 1)
        self.__end_date = datetime.date.today()

    def __get_random_model_name(self):
        return self._models_names[random.randrange(len(self._models_names))]

    def __get_random_date(self):
        time_between_dates = self.__end_date - self.__start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = self.__start_date + datetime.timedelta(days=random_number_of_days)

        return random_date

    def __get_random_count_auto(self, limit=1000):
        return random.randrange(limit)

    def __get_random_price(self, low_price: float, high_price: float):
        return round(random.uniform(low_price, high_price), 2)

    def get_random_data(self, number_of_records):
        random_data = set()

        for i in range(number_of_records):
            random_data.add(
                (
                    self.__get_random_model_name(),
                    self.__get_random_date().strftime("%d/%m/%Y"),
                    self.__get_random_count_auto(CAR_COUNT_LIMIT),
                    self.__get_random_price(CAR_PRICE_LOW_BOUND, CAR_PRICE_HIGH_BOUND)
                )
            )

        return random_data
