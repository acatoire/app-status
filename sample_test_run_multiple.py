"""
Test application for app status library
The app is simulating a test run anf post the result on a remote screen.

"""

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
    event_period_s = 3

    total = [20, 15, 30, 10]

    # create blynk status object
    status = TestRunStatus(BLYNK_AUTH)

    # fill up test run start info
    for i in range(4):
        status.start(i, total[i], "Run {}".format(i))

    last_event = time.time()

    actual = [0, 0, 0, 0]
    failed = [0, 0, 0, 0]
    blocked = [0, 0, 0, 0]
    succeed = [0, 0, 0, 0]

    # Generate test steps
    while max(actual) < max(total):

        now = time.time()
        if now - last_event > event_period_s:
            last_event = now

            for i in range(4):
                if actual[i] < total[i]:
                    actual[i] += 1
                    failed[i] += random.choice(CHANCE)
                    blocked[i] += random.choice(CHANCE)
                    succeed[i] = actual[i] - failed[i] - blocked[i]

                    status.update(run_id=i, actual=actual[i],
                                  succeed=succeed[i], failed=failed[i], blocked=blocked[i])

    for i in range(4):
        status.stop(i)


if __name__ == "__main__":
    main()
