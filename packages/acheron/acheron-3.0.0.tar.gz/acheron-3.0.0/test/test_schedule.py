import datetime
import unittest

from acheron.device_process.schedule import (RemoteSchedule, Schedule,
                                             ScheduleItem)


class TestSchedule(unittest.TestCase):

    def setUp(self):
        now = datetime.datetime.now(datetime.timezone.utc)

        self.item1 = ScheduleItem(
            id="Item1",
            start_time=None,  # asap
            collection_time=None,
            stop_time=None,
            duration=None,
            failure_time=None,
            output_config=None,
        )

        self.item2 = ScheduleItem(
            id="Item2",
            start_time=now + datetime.timedelta(seconds=10),  # future
            collection_time=None,
            stop_time=None,
            duration=None,
            failure_time=None,
            output_config=None,
        )

        self.item3 = ScheduleItem(
            id="Item3",
            start_time=now - datetime.timedelta(seconds=10),  # past
            collection_time=None,
            stop_time=None,
            duration=None,
            failure_time=None,
            output_config=None,
        )

    def test_schedule_get_ready_items(self):
        schedule = Schedule([self.item1, self.item2, self.item3], frozenset())

        ready, _next = schedule.get_ready_items()
        self.assertSetEqual(ready, {self.item1, self.item3})

    def test_schedule_item_comparison(self):
        def check_self_comparison(item):
            self.assertEqual(item < item, False)
            self.assertEqual(item <= item, True)
            self.assertEqual(item > item, False)
            self.assertEqual(item >= item, True)
            self.assertEqual(item == item, True)
            self.assertEqual(item != item, False)

        def check_other_comparison(lesser, greater):
            self.assertEqual(lesser < greater, True)
            self.assertEqual(lesser <= greater, True)
            self.assertEqual(lesser > greater, False)
            self.assertEqual(lesser >= greater, False)
            self.assertEqual(lesser == greater, False)
            self.assertEqual(lesser != greater, True)

        check_self_comparison(self.item1)
        check_self_comparison(self.item2)
        check_self_comparison(self.item3)

        check_other_comparison(self.item1, self.item2)
        check_other_comparison(self.item1, self.item3)
        check_other_comparison(self.item3, self.item2)

    def test_schedule_remote(self):
        schedule = Schedule([self.item1, self.item2], frozenset())

        ready, _next = schedule.get_ready_items()
        self.assertSetEqual(ready, {self.item1})

        remote_schedule = RemoteSchedule(schedule, 1234, False, [self.item3])

        ready, _next = schedule.get_ready_items()
        self.assertEqual(len(ready), 2)

        ready, _next = remote_schedule.get_ready_items()
        self.assertSetEqual(ready, {self.item3})
