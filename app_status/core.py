"""
A simple blynk application status screen manager

It allows to post application status in an easy to build blynk phone application

"""

import blynklib


class AppStatus:
    """
    Master class to
        - manage a blynk connection
        - send a dict of values to it
    """

    def __init__(self, blink_key, app_id=0):
        """
        Class init
        :param blink_key: the blynk auth key to be use
        """
        # initialize Blynk
        self.app_id = app_id
        self.blynk = blynklib.Blynk(blink_key)

        # Needed to create the connection
        self.blynk.run()

    def post_dict(self, status_dict: dict):
        """
        Method to sent to the blynk app information formatted in a dictionary
        :param status_dict: dict of values with pair of id : value
                            the id is the virtual pin number to be use
                            the value can be a string or a int/float

        :return: None
        """

        for key, value in status_dict.items():
            self.blynk.virtual_write(key, value)

        # Sync the request
        self.blynk.run()


class RunElements:
    """
    Sub class to manage the test run information

    """

    name = "no name"
    date = "--/--/---- (--:--)"
    total = 0
    failed = 0
    blocked = 0
    actual = 0
    succeed = 0


class RunStatus(AppStatus):
    """
    Sub class to manage the status of a test run application

    """

    # Maximum number of managed test runs
    MAX_RUN = 4

    # Pin definition
    PIN_NAME = 0
    PIN_DATE = 1
    PIN_STATUS_TEXT = 2
    PIN_STATUS_GRAPH = 3
    PIN_TYPES = 4
    PIN_LED = 5

    def __init__(self, blink_key, app_id=0):
        super().__init__(blink_key, app_id)

        self.test_run = RunElements()

    def start(self, total: int, name: str = None):
        """
        Method to sync test run information with the phone application at startup

        :param total: total number of test for this run
        :param name: name of test run
        :return: None
        """

        # Clean the run
        self.test_run = RunElements()

        if name is not None:
            self.test_run.name = name

        self.test_run.total = total

        # Init the start run date
        from datetime import datetime
        self.test_run.date = datetime.now().strftime("%d-%m-%Y (%H:%M)")

        self.__send_all()

    def update(self, succeed: int = None, failed: int = None, blocked: int = None):
        """
        Method to sync test run information values with the phone application

        :param succeed: (optional) updated succeed before send
        :param failed: (optional) updated failed before send
        :param blocked: (optional) updated blocked before send
        :return: None
        """

        if self.test_run.total == 0:
            raise ValueError("The total value has not been setup, run init() first.")

        # Update givens values
        if succeed is not None:
            self.test_run.succeed = succeed

        if failed is not None:
            self.test_run.failed = failed

        if blocked is not None:
            self.test_run.blocked = blocked

        self.test_run.actual = (self.test_run.succeed
                                + self.test_run.failed
                                + self.test_run.blocked)

        self.__send_update()

    def add_blocked(self, value: int = None):
        """
        Increment the blocked value
        :param value: (optional) increment other than 1
        :return: None
        """

        if value == 0:
            raise ValueError("You really want to increment of 0?")

        if value is None:
            self.test_run.actual += 1
            self.test_run.blocked += 1
        else:
            self.test_run.actual += value
            self.test_run.blocked += value

        self.__send_update()

    def add_succeed(self, value: int = None):
        """
        Increment the succeed value
        :param value: (optional) increment other than 1
        :return: None
        """

        if value == 0:
            raise ValueError("You really want to increment of 0?")

        if value is None:
            self.test_run.actual += 1
            self.test_run.succeed += 1
        else:
            self.test_run.actual += value
            self.test_run.succeed += value

        self.__send_update()

    def add_failed(self, value: int = None):
        """
        Increment the failed value
        :param value: (optional) increment other than 1
        :return: None
        """

        if value == 0:
            raise ValueError("You really want to increment of 0?")

        if value is None:
            self.test_run.actual += 1
            self.test_run.failed += 1
        else:
            self.test_run.actual += value
            self.test_run.failed += value

        self.__send_update()

    def stop(self):
        """
        Sent a stop information to the blynk phone application
        :return: None
        """

        print("Status sent: stop")

        offset = self.app_id * 10

        status_dict = {}
        # Test run led
        status_dict[offset + self.PIN_LED] = 0

        self.post_dict(status_dict)

    def __send_all(self):
        """
        Send all info of a test run
        :return: None
        """

        offset = self.app_id * 10

        print("Start run {} - {} @ {} with {} tests".format(self.app_id,
                                                            self.test_run.name,
                                                            self.test_run.date,
                                                            self.test_run.total))

        status_dict = {}
        # Test run name
        status_dict[offset + self.PIN_NAME] = self.test_run.name
        # Test run start datetime
        status_dict[offset + self.PIN_DATE] = self.test_run.date
        # Test run advance status string
        status_dict[offset + self.PIN_STATUS_TEXT] = "{}/{}".format(self.test_run.actual,
                                                                    self.test_run.total)
        # Test run advance status percent
        percent = self.test_run.actual / self.test_run.total * 100
        status_dict[offset + self.PIN_STATUS_GRAPH] = percent
        # Test run result type numbers
        status_dict[offset + self.PIN_TYPES] = "S{} F{} B{}".format(self.test_run.succeed,
                                                                    self.test_run.failed,
                                                                    self.test_run.blocked)
        # Test run led TODO manage color
        status_dict[offset + self.PIN_LED] = 255

        self.post_dict(status_dict)

    def __send_update(self):
        """
        Send updated info of a test run
        :return: None
        """

        offset = self.app_id * 10

        # TODO set number of leading zero depending on max value
        print("Update run {}: {} {}/{} with {}S - {}F - {}B".format(self.app_id,
                                                                    self.test_run.date,
                                                                    self.test_run.actual,
                                                                    self.test_run.total,
                                                                    self.test_run.succeed,
                                                                    self.test_run.failed,
                                                                    self.test_run.blocked))

        status_dict = {}
        # Test run advance status string
        status_dict[offset + self.PIN_STATUS_TEXT] = "{}/{}".format(self.test_run.actual,
                                                                    self.test_run.total)
        # Test run advance status percent
        percent = self.test_run.actual / self.test_run.total * 100
        status_dict[offset + self.PIN_STATUS_GRAPH] = percent
        # Test run result type number
        status_dict[offset + self.PIN_TYPES] = "S{} F{} B{}".format(self.test_run.succeed,
                                                                    self.test_run.failed,
                                                                    self.test_run.blocked)
        # Test run led TODO manage color
        status_dict[offset + self.PIN_LED] = 255

        self.post_dict(status_dict)
