"""
A program (experiment) which takes two approaches to simulate the birthday paradox
(https://en.wikipedia.org/wiki/Birthday_problem) which states that 23 people are enough in order to achieve
an above 50% probability of at least two of them sharing their birthdays.

Approach 1

The first approach simulates a provided number of groups, choosing randomly their members' birthday dates and
calculating which nth person will happen to have their birthday the same day as any other group member.
The result of the simulation is represented by the median of the groups sizes.
It is accompanied by the following figures: the mean, the smallest, and the biggest number of the group sizes.

Approach 2

The second approach takes a provided number of groups and their members. For each group, it is checked if there
are at least any two members who happen to have their birthday the same day.

Both approaches of the problem simulations show that it takes approximately 23 people to get 50% probability of
the problem in question.
"""

import statistics
from random import randrange
from typing import List


def draw_date() -> int:
    """
    Draw one day out of a 365 days long year
    :return: drawn day of a year
    """

    days = 365
    return randrange(days)


def simulate_one_group() -> int:
    """
    Simulate a group of people by adding new members until any two of them have their birthday on the same day
    :return: number of group members
    """

    birthdays = set()
    while True:
        birthday = draw_date()
        if birthday in birthdays:
            group_length = len(birthdays) + 1
            return group_length
        birthdays.add(birthday)


def run_n_simulations(n: int) -> List[int]:
    """
    Run simulations the provided number of times
    :param n: number of simulations
    :return: scores for a given number of groups
    """

    return [simulate_one_group() for i in range(1, n + 1)]


def get_simulation_details(results: List[int]) -> None:
    """
    Print median, mean, min, and max, of the results of the Approach 1
    :param results: scores for a given number of groups
    :return: None
    """

    average = sum(results) / len(results)
    median = statistics.median(results)
    min_result = min(enumerate(results), key=lambda x: x[1])
    max_result = max(enumerate(results), key=lambda x: x[1])
    print(
        f'Median: {median} - the group composed of this number of people has 50% chance that any two members'
        f'have their birthdays the same day'
        f'\nMean: {average}'
        f'\nMin: {min_result[1]} - group {min_result[0]}'
        f'\nMax: {max_result[1]} - group {max_result[0]}\n'
    )


def simulate_n_people_group(people: int) -> bool:
    """
    Simulate a group of n people and check if there are at least two of them who have their birthdays the same day
    :param people: number of people in a group
    :return: boolean value indicating if the condition is satisfied
    """

    birthdays = set()
    birthday = draw_date()
    while birthday not in birthdays and len(birthdays) < people:
        birthdays.add(birthday)
        birthday = draw_date()
    return birthday in birthdays


def get_probability_for_n_people(people: int, n_groups: int) -> float:
    """
    Calculate the probability of at least two group members having their birthdays the same day. The estimation is done
     for a given number of groups, each of them having a specified number of members
    :param people: number of people in a group
    :param n_groups: number of groups
    :return: probability calculated for given conditions
    """

    results = [simulate_n_people_group(people) for _ in range(n_groups)]
    return len([x for x in results if x]) / n_groups


if __name__ == "__main__":
    # Approach 1
    print('Approach 1')
    simulated_groups = 1000000
    simulation_results = run_n_simulations(simulated_groups)
    get_simulation_details(simulation_results)

    # Approach 2
    print('Approach 2')
    simulated_groups = 1000000
    group_members = 23
    probability = get_probability_for_n_people(group_members, simulated_groups)
    print(
        f'For given conditions:\n\tNumber of groups: {simulated_groups}'
        f'\n\tNumber of group members: {group_members}'
        f'\nThe probability of at least two members having their birthdays the same day is: {probability}'
    )
