import unittest

from pydantic_core import ValidationError

from acheron.disk.disk_trigger import DiskTrigger
from acheron.calc_process.types import LimitType, Trigger


class TestDiskTrigger(unittest.TestCase):
    def test_disktrigger_deactivate_polarity(self):
        base_values = {
            "serial": "WMR1234",
            "id": "test",
            "channel_id": 1,
            "subchannel_index": 0,
        }

        for limit_type in (LimitType.MEAN_HIGH_LIMIT,
                           LimitType.STD_HIGH_LIMIT):
            with self.assertRaises(ValidationError):
                DiskTrigger(limit_type=limit_type, activate_limit=5,
                            deactivate_limit=6, **base_values)
            DiskTrigger(limit_type=limit_type, activate_limit=5,
                        deactivate_limit=4, **base_values)

        for limit_type in (LimitType.MEAN_LOW_LIMIT, LimitType.STD_LOW_LIMIT):
            with self.assertRaises(ValidationError):
                DiskTrigger(limit_type=limit_type, activate_limit=5,
                            deactivate_limit=4, **base_values)
            DiskTrigger(limit_type=limit_type, activate_limit=5,
                        deactivate_limit=6, **base_values)

    def test_disktrigger_comparison(self):
        values = {
            "id": "test",
            "channel_id": 1,
            "subchannel_index": 0,
            "limit_type": LimitType.MEAN_HIGH_LIMIT,
            "activate_limit": 5,
            "deactivate_limit": 4,
        }
        disk_trigger = DiskTrigger(serial=("WMR1234",), **values)
        trigger = Trigger(**values)

        self.assertEqual(disk_trigger.convert(), trigger)

        d = disk_trigger.model_dump()
        self.assertNotIn("hysteresis", d)

    def test_disktrigger_hysteresis(self):
        base_values = {
            "serial": "WMR1234",
            "id": "test",
            "channel_id": 1,
            "subchannel_index": 0,
            "activate_limit": 5,
            "hysteresis": 1,
        }

        for limit_type in (LimitType.MEAN_HIGH_LIMIT,
                           LimitType.STD_HIGH_LIMIT):
            disk_trigger = DiskTrigger(limit_type=limit_type, **base_values)
            self.assertEqual(disk_trigger.deactivate_limit, 4)

        for limit_type in (LimitType.MEAN_LOW_LIMIT, LimitType.STD_LOW_LIMIT):
            disk_trigger = DiskTrigger(limit_type=limit_type, **base_values)
            self.assertEqual(disk_trigger.deactivate_limit, 6)

    def test_disktrigger_missing_hysteresis(self):
        values = {
            "serial": "WMR1234",
            "id": "test",
            "channel_id": 1,
            "subchannel_index": 0,
            "limit_type": LimitType.MEAN_HIGH_LIMIT,
            "activate_limit": 5,
        }

        with self.assertRaises(ValidationError):
            DiskTrigger(**values)

    def test_disktrigger_json(self):
        disk_trigger = DiskTrigger(
            serial=("WMR1234",),
            id="test",
            channel_id=1,
            subchannel_index=0,
            limit_type=LimitType.MEAN_HIGH_LIMIT,
            activate_limit=10,
            deactivate_limit=9)

        json_str = ('{"serial":"WMR1234","id":"test","channel_id":1,'
                    '"subchannel_index":"0","limit_type":"mean high",'
                    '"activate_limit":10,"deactivate_limit":9.0}')
        json_disk_trigger = DiskTrigger.model_validate_json(json_str)

        self.assertEqual(disk_trigger, json_disk_trigger)

    def test_disktrigger_serial_tuple(self):
        disk_trigger = DiskTrigger(
            serial=("WMR1234", "WM2345"),
            id="test",
            channel_id=1,
            subchannel_index=0,
            limit_type=LimitType.MEAN_HIGH_LIMIT,
            activate_limit=10,
            deactivate_limit=9)

        json_str = ('{"serial":["WMR1234","WM2345"],"id":"test",'
                    '"channel_id":1,"subchannel_index":"0",'
                    '"limit_type":"mean high","activate_limit":10,'
                    '"deactivate_limit":9.0}')
        json_disk_trigger = DiskTrigger.model_validate_json(json_str)

        self.assertEqual(disk_trigger, json_disk_trigger)
