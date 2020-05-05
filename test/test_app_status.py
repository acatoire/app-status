
from unittest import TestCase
from unittest.mock import Mock, call

import blynklib

from app_status import AppStatus, RunStatus


BLYNK_AUTH = 'fake_auth'


class FakeBlink:
    def virtual_write(self):
        pass

    def run(self):
        pass


class TestAppStatus(TestCase):

    def test_post_dict(self):

        blynklib.Blynk = Mock(return_value=FakeBlink())
        status = AppStatus(BLYNK_AUTH)

        blynklib.Blynk.assert_called_once_with(BLYNK_AUTH)

        status.blynk.virtual_write = Mock(return_value=None)
        status.blynk.run = Mock(return_value=None)
        post_dict = {1: "1", 2: "2"}
        calls = [call(1, "1"), call(2, "2")]

        status.post_dict(post_dict)

        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()


class TestRunStatus(TestCase):

    def test_start(self):

        blynklib.Blynk = Mock(return_value=FakeBlink())
        status = RunStatus(BLYNK_AUTH)

        blynklib.Blynk.assert_called_once_with(BLYNK_AUTH)

        status.blynk.virtual_write = Mock(return_value=None)
        status.blynk.run = Mock(return_value=None)

        from datetime import datetime
        start_dict = {0: "name",                                         # Test run name
                      1: datetime.now().strftime("%d-%m-%Y (%H:%M)"),    # Test run start datetime
                      2: "{}/{}".format(0, 10),                          # Test run advance status string
                      3: 0,                                              # Test run advance status percent
                      4: "S{} F{} B{}".format(0, 0, 0),                  # Test run result type numbers
                      5: 255}                                            # Test run led - may evolve

        calls = []
        for key, value in start_dict.items():
            calls.append(call(key, value))

        status.start(0, 10, "name")

        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

    def test_stop(self):

        blynklib.Blynk = Mock(return_value=FakeBlink())
        status = RunStatus(BLYNK_AUTH)

        blynklib.Blynk.assert_called_once_with(BLYNK_AUTH)

        status.blynk.virtual_write = Mock(return_value=None)
        status.blynk.run = Mock(return_value=None)

        calls = [call(5, 0)]  # Test run led - may evolve

        status.start(0, 10, "name")
        status.blynk.virtual_write.reset_mock()
        status.blynk.run.reset_mock()

        status.stop(0)

        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

    def test_increment(self):

        blynklib.Blynk = Mock(return_value=FakeBlink())
        status = RunStatus(BLYNK_AUTH)

        blynklib.Blynk.assert_called_once_with(BLYNK_AUTH)

        status.blynk.virtual_write = Mock(return_value=None)
        status.blynk.run = Mock(return_value=None)

        status.start(0, 10, "name")

        # ######################

        update_dict = {2: "{}/{}".format(1, 10),  # Test run advance status string
                       3: 10,  # Test run advance status percent
                       4: "S{} F{} B{}".format(1, 0, 0),  # Test run result type numbers
                       5: 255}  # Test run led - may evolve

        calls = []
        for key, value in update_dict.items():
            calls.append(call(key, value))

        status.add_succeed(0)
        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

        # ######################
        status.blynk.virtual_write.reset_mock()
        status.blynk.run.reset_mock()

        update_dict = {2: "{}/{}".format(2, 10),  # Test run advance status string
                       3: 20,  # Test run advance status percent
                       4: "S{} F{} B{}".format(1, 1, 0),  # Test run result type numbers
                       5: 255}  # Test run led - may evolve

        calls = []
        for key, value in update_dict.items():
            calls.append(call(key, value))

        status.add_failed(0)
        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

        # ######################
        status.blynk.virtual_write.reset_mock()
        status.blynk.run.reset_mock()

        update_dict = {2: "{}/{}".format(3, 10),  # Test run advance status string
                       3: 30,  # Test run advance status percent
                       4: "S{} F{} B{}".format(1, 1, 1),  # Test run result type numbers
                       5: 255}  # Test run led - may evolve

        calls = []
        for key, value in update_dict.items():
            calls.append(call(key, value))

        status.add_blocked(0)
        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

        # ######################

    def test_increment_x(self):

        blynklib.Blynk = Mock(return_value=FakeBlink())
        status = RunStatus(BLYNK_AUTH)

        blynklib.Blynk.assert_called_once_with(BLYNK_AUTH)

        status.blynk.virtual_write = Mock(return_value=None)
        status.blynk.run = Mock(return_value=None)

        status.start(0, 10, "name")

        # ######################

        update_dict = {2: "{}/{}".format(2, 10),  # Test run advance status string
                       3: 20,  # Test run advance status percent
                       4: "S{} F{} B{}".format(2, 0, 0),  # Test run result type numbers
                       5: 255}  # Test run led - may evolve

        calls = []
        for key, value in update_dict.items():
            calls.append(call(key, value))

        status.add_succeed(0, 2)
        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

        # ######################
        status.blynk.virtual_write.reset_mock()
        status.blynk.run.reset_mock()

        update_dict = {2: "{}/{}".format(5, 10),  # Test run advance status string
                       3: 50,  # Test run advance status percent
                       4: "S{} F{} B{}".format(2, 3, 0),  # Test run result type numbers
                       5: 255}  # Test run led - may evolve

        calls = []
        for key, value in update_dict.items():
            calls.append(call(key, value))

        status.add_failed(0, 3)
        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

        # ######################
        status.blynk.virtual_write.reset_mock()
        status.blynk.run.reset_mock()

        update_dict = {2: "{}/{}".format(9, 10),  # Test run advance status string
                       3: 90,  # Test run advance status percent
                       4: "S{} F{} B{}".format(2, 3, 4),  # Test run result type numbers
                       5: 255}  # Test run led - may evolve

        calls = []
        for key, value in update_dict.items():
            calls.append(call(key, value))

        status.add_blocked(0, 4)
        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()

        # ######################

    def test_update(self):

        blynklib.Blynk = Mock(return_value=FakeBlink())
        status = RunStatus(BLYNK_AUTH)

        blynklib.Blynk.assert_called_once_with(BLYNK_AUTH)

        status.blynk.virtual_write = Mock(return_value=None)
        status.blynk.run = Mock(return_value=None)

        from datetime import datetime
        date = datetime.now().strftime("%d-%m-%Y (%H:%M)")
        status.start(0, 10, "name")
        status.blynk.virtual_write.reset_mock()
        status.blynk.run.reset_mock()

        update_dict = {2: "{}/{}".format(6, 10),                          # Test run advance status string
                       3: 60,                                              # Test run advance status percent
                       4: "S{} F{} B{}".format(3, 2, 1),                  # Test run result type numbers
                       5: 255}                                            # Test run led - may evolve

        calls = []
        for key, value in update_dict.items():
            calls.append(call(key, value))

        status.start(0, 10, "name")
        status.blynk.virtual_write.reset_mock()
        status.blynk.run.reset_mock()

        status.update(0, 3, 2, 1)

        status.blynk.virtual_write.assert_has_calls(calls)
        status.blynk.run.assert_called()
