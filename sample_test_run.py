"""
Test application for app status library
The app is simulating a test run anf post the result on a remote screen.

"""


import datetime
import time
import random
from app_status import TestRunStatus


BLYNK_AUTH = 'xz7QdnPAfTMVm4247CGRb0jVjgXF1byY'

CHANCE = [0, 0, 0, 0, 1]


def main():
    """
    Main method for the test run simulation app
    :return: None
    """

    # init steps timing
    last_event = 0
    event_period_s = 3

    # create blynk status object
    status = TestRunStatus(BLYNK_AUTH)

    # fill up test run base info
    status.name = "Test run name"
    status.date = datetime.datetime.now().strftime("%d-%m-%Y (%H:%M)")
    status.actual = 0
    status.total = 10

    # Generate test steps
    while status.actual < status.total:

        now = time.time()
        if now - last_event > event_period_s:
            last_event = now

            status.actual += 1
            status.failed += random.choice(CHANCE)
            status.blocked += random.choice(CHANCE)
            status.succeed = status.actual - status.failed - status.blocked

            status.update()

            # TODO generate sub steps

    status.stop()


if __name__ == "__main__":
    main()
