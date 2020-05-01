"""
A simple blynk application status screen manager

It allows to post application status in an easy to build blynk app
"""

import blynklib


class AppStatus:
    """
    Master class to
        - manage a blynk connection
        - send a dict of values to it
    """

    def __init__(self, blink_key):
        """
        Class init
        :param blink_key: the blynk auth key to be use
        """
        # initialize Blynk
        self.blynk = blynklib.Blynk(blink_key)

    def post_dict(self, status_dict: dict):
        """
        Method to sent to the blynk app information formatted in a dictionary
        :param status_dict: dict of values with pair of id : value
                            the id is the virtual pin number to be use
                            the value can be a string or a int/float

        :return: none
        """
        # Needed in case of first execution
        self.blynk.run()

        for key, value in status_dict.items():
            self.blynk.virtual_write(key, value)

        # Sync the request
        self.blynk.run()


class TestRunStatus(AppStatus):
    """
    Sub class to manage the status of a test run application

    """

    def __init__(self, blink_key):
        super().__init__(blink_key)

        self.name = "no name"
        self.date = "--/--/---- (--:--)"
        self.total = 0
        self.failed = 0
        self.blocked = 0
        self.actual = 0
        self.succeed = 0

    # TODO init_datetime

    def update(self):
        """
        Method to sync test run information values with the blynk phone application

        :return: none
        """

        # TODO set number of leading zero depending on max value
        print(
            "Status sent: {} {}/{} with {}S - {}F - {}B".format(self.date,
                                                                self.actual,
                                                                self.total,
                                                                self.succeed,
                                                                self.failed,
                                                                self.blocked))

        status_dict = {}
        # Test run name
        status_dict[0] = self.name
        # Test run start datetime
        status_dict[1] = self.date
        # Test run advance status string
        status_dict[2] = "{}/{}".format(self.actual, self.total)
        # Test run advance status percent
        status_dict[3] = self.actual / self.total * 100
        # Test run result type numbers
        status_dict[4] = "S{} F{} B{}".format(self.succeed, self.failed, self.blocked)
        # Test run led TODO manage color
        status_dict[5] = 255

        self.post_dict(status_dict)

    def stop(self):
        """
        Sent a stop information to the blynk phone application
        :return:
        """

        print("Status sent: stop")

        status_dict = {}
        # Test run led
        status_dict[5] = 0

        self.post_dict(status_dict)
