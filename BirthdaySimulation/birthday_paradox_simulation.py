"""
A program which simulates groups of people, choosing randomly their members' birthday dates (day and month)
and calculating which nth person will happen to have their birthday the same day as any other group member.

The simulation estimates how many people is enough to ensure that 2 of them will have their birthday the same day.

The results are provided as the following figures:
    - the median of a given number of groups (which means 50% probability that 2 people out of the result number have
        birthdays the same day)
    - the mean of a given number of groups
    - the smallest number resulting from the simulation
    - the highest number resulting from the simulation

The details of the results are written into a log file.
"""

import datetime
import logging
import os
import statistics
from random import randrange
from typing import Tuple


def draw_date() -> Tuple[int, int]:
    """
    Draw a month and a day. It is assumed that February is 28 days long
    :return: day and month
    """

    months_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    month = randrange(1, 13)
    day = randrange(1, months_days[month] + 1)
    return day, month


def simulate_one_group(iteration: int) -> int:
    """
    Simulate a group of people by adding new members until any two of them have their birthday on the same day
    :param iteration: group's number
    :return: number of group members
    """

    birthdays = set()
    while True:
        birthday = draw_date()
        if birthday in birthdays:
            group_length = len(birthdays) + 1
            logging.debug(f'\nGroup {iteration}'
                          f'\n\tTwo people have birthday on the same day when the number of people in the group is:'
                          f'\n\t{group_length}')
            logging.debug(f'\tDates are written in (day, month) format.'
                          f'\n\t{birthday} - {sorted(birthdays, key=lambda d: (d[1], d[0]))}')
            return group_length
        birthdays.add(birthday)


def main(n: int) -> None:
    """
    Run simulations the provided number of times
    :param n: number of simulations
    """

    set_logger()

    results = [simulate_one_group(i) for i in range(1, n + 1)]
    results = sorted(results)

    average = sum(results) / len(results)
    median = statistics.median(results)
    min_result = min(enumerate(results), key=lambda x: x[1])
    max_result = max(enumerate(results), key=lambda x: x[1])
    logging.info(
        f'\nResults for {n} groups'
        f'\n\tMedian: {median}\n\t\t- the group composed of this number of people has 50% chance that any two members'
        f'have their birthdays the same day'
        f'\n\tMean: {average}'
        f'\n\tMin: {min_result[1]} - group {min_result[0]}'
        f'\n\tMax: {max_result[1]} - group {max_result[0]}'
    )
    close_logger()


def set_logger() -> None:
    """
    Set log file
    :return: None
    """

    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = 'birthday_simulation_logs'
    path = os.path.join(folder, f'birthdays_{date}.logs')
    os.makedirs(folder, exist_ok=True)
    logging.basicConfig(filename=path, level=logging.DEBUG, format='%(message)s')
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    logging.getLogger('').addHandler(stream)
    print(f'\nLog file was created in {path}. The details of the simulation can be found there.')


def close_logger():
    logging.shutdown()


if __name__ == "__main__":
    simulated_groups = 1000000
    main(simulated_groups)
