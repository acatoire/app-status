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

        :return: None
        """
        # Needed in case of first execution
        self.blynk.run()

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

    def __init__(self, blink_key):
        super().__init__(blink_key)

        self.test_runs = []
        for _ in range(self.MAX_RUN):
            self.test_runs.append(RunElements())

    def start(self, run_id: int, total: int, name: str = None):
        """
        Method to sync test run information with the phone application at startup

        :param run_id: test run id to be affected
        :param total: total number of test for this run
        :param name: name of test run
        :return: None
        """

        # Clean the run
        self.test_runs[run_id] = RunElements()

        if name is not None:
            self.test_runs[run_id].name = name

        self.test_runs[run_id].total = total

        # Init the start run date
        from datetime import datetime
        self.test_runs[run_id].date = datetime.now().strftime("%d-%m-%Y (%H:%M)")

        self.__send_all(run_id)

    def update(self, run_id: int, succeed: int = None, failed: int = None, blocked: int = None):
        """
        Method to sync test run information values with the phone application

        :param run_id: test run id to be updated
        :param succeed: (optional) updated succeed before send
        :param failed: (optional) updated failed before send
        :param blocked: (optional) updated blocked before send
        :return: None
        """

        if self.test_runs[run_id].total == 0:
            raise ValueError("The total value has not been setup, run init() first.")

        # Update givens values
        if succeed is not None:
            self.test_runs[run_id].succeed = succeed

        if failed is not None:
            self.test_runs[run_id].failed = failed

        if blocked is not None:
            self.test_runs[run_id].blocked = blocked

        self.test_runs[run_id].actual = (self.test_runs[run_id].succeed
                                         + self.test_runs[run_id].failed
                                         + self.test_runs[run_id].blocked)

        self.__send_update(run_id)

    def add_blocked(self, run_id, value: int = None):
        """
        Increment the blocked value
        :param run_id: test run id to be updated
        :param value: (optional) increment other than 1
        :return: None
        """

        if value is None:
            self.test_runs[run_id].actual += 1
            self.test_runs[run_id].blocked += 1
        else:
            self.test_runs[run_id].actual += value
            self.test_runs[run_id].blocked += value

        self.__send_update(run_id)

    def add_succeed(self, run_id, value: int = None):
        """
        Increment the succeed value
        :param run_id: test run id to be updated
        :param value: (optional) increment other than 1
        :return: None
        """

        if value is None:
            self.test_runs[run_id].actual += 1
            self.test_runs[run_id].succeed += 1
        else:
            self.test_runs[run_id].actual += value
            self.test_runs[run_id].succeed += value

        self.__send_update(run_id)

    def add_failed(self, run_id, value: int = None):
        """
        Increment the failed value
        :param run_id: test run id to be updated
        :param value: (optional) increment other than 1
        :return: None
        """

        if value is None:
            self.test_runs[run_id].actual += 1
            self.test_runs[run_id].failed += 1
        else:
            self.test_runs[run_id].actual += value
            self.test_runs[run_id].failed += value

        self.__send_update(run_id)

    def stop(self, run_id):
        """
        Sent a stop information to the blynk phone application
        :param run_id: test run id to be updated
        :return: None
        """

        print("Status sent: stop")


        offset = run_id * 10

        status_dict = {}
        # Test run led
        status_dict[offset + self.PIN_LED] = 0

        self.post_dict(status_dict)

    def __send_all(self, run_id):
        """
        Send all info of a test run
        :param run_id: test run id to be updated
        :return: None
        """

        offset = run_id * 10

        print("Start run {} - {} @ {} with {} tests".format(run_id,
                                                            self.test_runs[run_id].name,
                                                            self.test_runs[run_id].date,
                                                            self.test_runs[run_id].total))

        status_dict = {}
        # Test run name
        status_dict[offset + self.PIN_NAME] = self.test_runs[run_id].name
        # Test run start datetime
        status_dict[offset + self.PIN_DATE] = self.test_runs[run_id].date
        # Test run advance status string
        status_dict[offset + self.PIN_STATUS_TEXT] = "{}/{}".format(self.test_runs[run_id].actual,
                                                                    self.test_runs[run_id].total)
        # Test run advance status percent
        percent = self.test_runs[run_id].actual / self.test_runs[run_id].total * 100
        status_dict[offset + self.PIN_STATUS_GRAPH] = percent
        # Test run result type numbers
        status_dict[offset + self.PIN_TYPES] = "S{} F{} B{}".format(self.test_runs[run_id].succeed,
                                                                    self.test_runs[run_id].failed,
                                                                    self.test_runs[run_id].blocked)
        # Test run led TODO manage color
        status_dict[offset + self.PIN_LED] = 255

        self.post_dict(status_dict)

    def __send_update(self, run_id):
        """
        Send updated info of a test run
        :param run_id: test run id to be updated
        :return: None
        """

        offset = run_id * 10

        # TODO set number of leading zero depending on max value
        print("Update run {}: {} {}/{} with {}S - {}F - {}B".format(run_id,
                                                                    self.test_runs[run_id].date,
                                                                    self.test_runs[run_id].actual,
                                                                    self.test_runs[run_id].total,
                                                                    self.test_runs[run_id].succeed,
                                                                    self.test_runs[run_id].failed,
                                                                    self.test_runs[run_id].blocked))

        status_dict = {}
        # Test run advance status string
        status_dict[offset + self.PIN_STATUS_TEXT] = "{}/{}".format(self.test_runs[run_id].actual,
                                                                    self.test_runs[run_id].total)
        # Test run advance status percent
        percent = self.test_runs[run_id].actual / self.test_runs[run_id].total * 100
        status_dict[offset + self.PIN_STATUS_GRAPH] = percent
        # Test run result type number
        status_dict[offset + self.PIN_TYPES] = "S{} F{} B{}".format(self.test_runs[run_id].succeed,
                                                                    self.test_runs[run_id].failed,
                                                                    self.test_runs[run_id].blocked)
        # Test run led TODO manage color
        status_dict[offset + self.PIN_LED] = 255

        self.post_dict(status_dict)
