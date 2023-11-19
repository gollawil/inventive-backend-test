from datetime import datetime, timedelta

import unittest

from src.models.looker_alert import LookerAlert
from src.models.customer_c2 import CustomerC2


class TestLookerAlert(unittest.TestCase):

    def setUp(self):
        self.customer_c2 = CustomerC2(
            name="Test Customer",
            notifications_email="test@example.com",
        )
        self.alert = LookerAlert(
            customer_c2=self.customer_c2,
            query_settings={
                "model": "thelook_partner",
                "view": "order_items",
                "fields": [
                    "order_items.sale_price",
                    "products.category",
                    "products.item_name"
                ],
                "filters": {
                    "order_items.sale_price": ">200",
                    "products.category": "Pants",
                },
            },
            alert_settings={
                "frequency": "daily",
            },
        )

    def test_request_body(self):
        expected_body = {
            "model": "thelook_partner",
            "view": "order_items",
            "fields": [
                "order_items.sale_price",
                "products.category",
                "products.item_name",
            ],
            "filters": {
                "order_items.sale_price": ">200",
                "products.category": "Pants",
            },
        }
        self.assertEqual(self.alert.request_body(), expected_body)

    def test_should_check_when_last_checked_is_none(self):
        self.assertTrue(self.alert.should_check())

    def test_should_check_when_last_checked_is_more_than_frequency_ago_daily(self): # noqa
        self.alert.last_checked = datetime.now() - timedelta(days=2)
        self.assertTrue(self.alert.should_check())

    def test_should_check_when_last_checked_is_more_than_frequency_ago_weekly(self): # noqa
        self.alert.frequency = "weekly"
        self.alert.last_checked = datetime.now() - timedelta(days=10)
        self.assertTrue(self.alert.should_check())

    def test_should_check_when_last_checked_is_more_than_frequency_ago_monthly(self): # noqa
        self.alert.frequency = "monthly"
        self.alert.last_checked = datetime.now() - timedelta(days=35)
        self.assertTrue(self.alert.should_check())

    def test_should_check_when_last_checked_is_less_than_frequency_ago_daily(self): # noqa
        self.alert.last_checked = datetime.now() - timedelta(hours=6)
        self.assertFalse(self.alert.should_check())

    def test_should_check_when_last_checked_is_less_than_frequency_ago_weekly(self): # noqa
        self.alert.frequency = "weekly"
        self.alert.last_checked = datetime.now() - timedelta(days=5)
        self.assertFalse(self.alert.should_check())

    def test_should_check_when_last_checked_is_less_than_frequency_ago_monthly(self): # noqa
        self.alert.frequency = "monthly"
        self.alert.last_checked = datetime.now() - timedelta(days=24)
        self.assertFalse(self.alert.should_check())

    def test_update_last_checked(self):
        self.assertIsNone(self.alert.last_checked)
        self.alert.update_last_checked()
        self.assertIsNotNone(self.alert.last_checked)
