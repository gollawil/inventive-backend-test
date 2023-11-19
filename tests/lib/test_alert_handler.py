from datetime import datetime

import unittest
from unittest.mock import MagicMock

from src.lib import AlertHandler
from src.models import (
    CustomerC2,
    LookerAlert,
)


class TestAlertHandler(unittest.TestCase):

    def setUp(self):
        self.alert_handler = AlertHandler()

        self.customer_c2 = CustomerC2(
            name="Test Customer",
            notifications_email="test@example.com",
        )
        self.looker_alert = LookerAlert(
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

        self.other_alert = {}

    def test_execute_with_no_alerts(self):
        results = self.alert_handler.execute([])
        expected = []

        self.assertEqual(results, expected)

    def test_execute_with_alert_that_should_run_and_has_results(self):
        looker_results = [1, 2, 3]

        mock_looker = MagicMock()
        mock_looker.query.return_value = looker_results
        self.alert_handler.looker = mock_looker

        results = self.alert_handler.execute(
            [self.looker_alert],
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["body"], looker_results)

    def test_execute_with_alert_that_should_run_but_has_no_results(self):
        results = self.alert_handler.execute(
            [self.looker_alert],
        )

        send_alert_mock = MagicMock()
        self.alert_handler._send_alert = send_alert_mock
        send_alert_mock.assert_not_called()

        self.assertEqual(len(results), 0)

    def test_execute_with_alert_that_should_not_run(self):
        self.looker_alert.last_checked = datetime.now()
        results = self.alert_handler.execute(
            [self.looker_alert],
        )

        self.assertEqual(len(results), 0)
