"""
Test application for app status library
The app is simulating a test run anf post the result on a remote screen.

"""

import time
import random
from app_status import RunStatus


BLYNK_AUTH = 'xz7QdnPAfTMVm4247CGRb0jVjgXF1byY'

CHANCE = [0, 0, 0, 0, 1]


def main():
    """
    Main method for the multiple test run simulation app

    :return: None
    """

    # init steps timing
    last_event = 0
    event_period_s = 3
    total = 10

    # create blynk status object
    status = RunStatus(BLYNK_AUTH)

    # fill up test run base info
    status.start(total, "Test run name")

    last_event = time.time()

    actual = 0
    failed = 0
    blocked = 0

    # Generate test steps
    while actual < total:

        now = time.time()
        if now - last_event > event_period_s:
            last_event = now

            actual += 1
            failed += random.choice(CHANCE)
            blocked += random.choice(CHANCE)
            succeed = actual - failed - blocked

            status.update(succeed=succeed, failed=failed, blocked=blocked)

    status.stop()


if __name__ == "__main__":
    main()
