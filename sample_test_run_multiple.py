"""
Test application for app status library
The app is simulating a test run anf post the result on a remote screen.

"""

import time
import random
from app_status import RunStatus


BLYNK_AUTH = 'xz7QdnPAfTMVm4247CGRb0jVjgXF1byY'

CHANCE_FAILED = [0, 1]
CHANCE_SUCCESS = [1, 1, 0]


def main():
    """
    Main method for the test run simulation app

    :return: None
    """

    # init steps timing
    event_period_s = 3

    total = [20, 15, 30, 10]

    # create status object table
    status = []

    # fill up test run start info
    for i in range(4):
        status.append(RunStatus(BLYNK_AUTH, i))
        status[i].start(total[i], "Run {}".format(i))

    # TODO random progress
    # Generate test steps
    for actual in range(max(total)):

        print("Loop {}".format(actual))
        time.sleep(event_period_s)

        for i in range(4):
            if actual < status[i].test_run.total:

                if random.choice(CHANCE_SUCCESS):
                    status[i].add_succeed()
                elif random.choice(CHANCE_FAILED):
                    status[i].add_failed()
                else:
                    status[i].add_blocked()

    time.sleep(event_period_s)
    for i in range(4):
        status[i].stop()


if __name__ == "__main__":
    main()
